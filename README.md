# 🤖 Telegram AI Bot

A Telegram bot powered by OpenAI (ChatGPT). Supports multi-turn conversations with context memory.

## Features

- 💬 Chat with GPT-4o-mini (or any OpenAI model)
- 🧠 Remembers conversation context (last 20 messages)
- 🌍 Responds in the user's language
- 🧹 `/clear` command to reset history

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/your-username/tg-ai-bot.git
cd tg-ai-bot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and fill in your keys:

```
TELEGRAM_BOT_TOKEN=...   # from @BotFather
OPENAI_API_KEY=...       # from platform.openai.com
OPENAI_MODEL=gpt-4o-mini
```

### 4. Run

```bash
python bot.py
```

## Getting API keys

- **Telegram token** — create a bot via [@BotFather](https://t.me/BotFather)
- **OpenAI key** — get it at [platform.openai.com/api-keys](https://platform.openai.com/api-keys)

## Commands

| Command  | Description              |
|----------|--------------------------|
| /start   | Start / restart the bot  |
| /help    | Show help message        |
| /clear   | Clear conversation history |

## Project structure

```
tg-ai-bot/
├── bot.py            # Main bot logic
├── requirements.txt  # Dependencies
├── .env.example      # Environment variables template
├── .gitignore
└── README.md
```

## License

MIT
