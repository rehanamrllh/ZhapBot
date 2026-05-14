# EchoBot

EchoBot adalah bot Telegram berbasis `aiogram` yang memakai Gemini untuk percakapan AI, menyimpan riwayat chat ke SQLite, dan menyediakan fitur konversi file ke PDF.

## Fitur

- Chat AI dengan konteks percakapan sebelumnya.
- Simpan dan hapus riwayat percakapan per chat.
- Ringkas percakapan lewat tombol inline.
- Konversi gambar JPG/PNG ke PDF.
- Konversi file teks `.txt` ke PDF.
- Dukungan album gambar agar beberapa foto bisa digabung menjadi satu PDF.

## Perintah Bot

- `/start` - Memulai percakapan dan menampilkan tombol utama.
- `/help` - Menampilkan bantuan.
- `/clear` - Menghapus memori percakapan.
- `/convertpdf` - Masuk ke mode konversi PDF.
- `/cancel` - Membatalkan mode aktif.

## Kebutuhan

- Python 3.10 atau lebih baru.
- Token bot Telegram dari [BotFather](https://t.me/BotFather).
- API key Gemini dari Google AI Studio.

## Instalasi

1. Buat virtual environment dan aktifkan:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

2. Install dependency:

```powershell
pip install -r requirements.txt
```

3. Buat file `.env` di root project lalu isi:

```env
TELEGRAM_BOT_TOKEN=isi_token_telegram_anda
GEMINI_API_KEY=isi_api_key_gemini_anda
```

## Menjalankan Bot

```powershell
python bot.py
```

Setelah bot berjalan, buka Telegram dan kirim `/start` ke bot Anda.

## Struktur Project

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

## Catatan

- Database SQLite dibuat otomatis sebagai `chat_memory.db` saat bot pertama kali dijalankan.
- File PDF dan file sementara dibuat saat proses konversi lalu dibersihkan setelah selesai.
- Model Gemini yang dipakai saat ini adalah `gemini-2.5-flash`.