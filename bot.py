import os
import logging
from dotenv import load_dotenv

load_dotenv()
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import AsyncOpenAI

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Store conversation history per user
user_histories: dict[int, list] = {}

SYSTEM_PROMPT = """You are a helpful assistant in a Telegram bot. 
Be concise, friendly, and useful. Answer in the language the user writes in."""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_histories[user.id] = []
    await update.message.reply_text(
        f"👋 Hi, {user.first_name}! I'm an AI assistant powered by ChatGPT.\n\n"
        "Just send me a message and I'll respond!\n\n"
        "Commands:\n"
        "/start – restart\n"
        "/clear – clear conversation history\n"
        "/help – show help"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "🤖 *AI Assistant Bot*\n\n"
        "Just write me anything — I'll respond using ChatGPT.\n"
        "I remember the context of our conversation.\n\n"
        "Commands:\n"
        "/clear – clear conversation history\n"
        "/help – show this message",
        parse_mode="Markdown"
    )


async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user_histories[user_id] = []
    await update.message.reply_text("🧹 Conversation history cleared!")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user_text = update.message.text

    if user_id not in user_histories:
        user_histories[user_id] = []

    user_histories[user_id].append({"role": "user", "content": user_text})

    # Keep only last 20 messages to save tokens
    if len(user_histories[user_id]) > 20:
        user_histories[user_id] = user_histories[user_id][-20:]

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    try:
        response = await client.chat.completions.create(
            model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + user_histories[user_id],
            max_tokens=1000,
            temperature=0.7,
        )

        reply = response.choices[0].message.content
        user_histories[user_id].append({"role": "assistant", "content": reply})

        await update.message.reply_text(reply)

    except Exception as e:
        logger.error(f"OpenAI error: {e}")
        await update.message.reply_text(
            "⚠️ Something went wrong. Please try again later."
        )


def main() -> None:
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("clear", clear))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot started...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
