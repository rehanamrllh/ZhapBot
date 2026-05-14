# ZhapBot

ZhapBot is a Telegram bot built with `aiogram` that uses Gemini for AI conversations, stores chat history in SQLite, and provides file-to-PDF conversion features.

## Features

- AI chat with previous conversation context.
- Save and clear conversation history per chat.
- Summarize conversations through inline buttons.
- Convert JPG/PNG images to PDF.
- Convert `.txt` text files to PDF.
- Support image albums so multiple photos can be merged into a single PDF.

## Bot Commands

- `/start` - Start a conversation and show the main buttons.
- `/help` - Show help information.
- `/clear` - Clear conversation memory.
- `/convertpdf` - Enter PDF conversion mode.
- `/cancel` - Cancel the active mode.

## Requirements

- Python 3.10 or newer.
- A Telegram bot token from [BotFather](https://t.me/BotFather).
- A Gemini API key from Google AI Studio.

## Installation

1. Create and activate a virtual environment:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

2. Install the dependencies:

```powershell
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and fill it with:

```env
TELEGRAM_BOT_TOKEN=isi_token_telegram_anda
GEMINI_API_KEY=isi_api_key_gemini_anda
```

## Running the Bot

```powershell
python bot.py
```

After the bot is running, open Telegram and send `/start` to your bot.

## Project Structure

```text
.
├── bot.py
├── ai_service.py
├── config.py
├── database.py
├── states.py
├── handlers/
│   ├── commands.py
│   ├── files.py
│   └── messages.py
├── keyboards/
│   └── inline.py
└── utils/
    └── pdf_converter.py
```

## Notes

- The SQLite database is created automatically as `chat_memory.db` when the bot is run for the first time.
- PDF files and temporary files are created during the conversion process and cleaned up afterward.
- The Gemini model currently used is `gemini-2.5-flash`.
