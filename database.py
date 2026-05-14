# pyrefly: ignore [missing-import]
import aiosqlite
import datetime

DB_PATH = "chat_memory.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                role TEXT,
                content TEXT,
                timestamp DATETIME
            )
        ''')
        await db.commit()

async def add_message(chat_id: int, role: str, content: str):
    """Menambahkan pesan ke database."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO messages (chat_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
            (chat_id, role, content, datetime.datetime.now())
        )
        await db.commit()

async def get_history(chat_id: int, limit: int = 20) -> list:
    """Mengambil riwayat percakapan untuk chat_id tertentu."""
    async with aiosqlite.connect(DB_PATH) as db:
        # Kita ambil X pesan terakhir, lalu urutkan secara kronologis (ascending)
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT role, content FROM (SELECT * FROM messages WHERE chat_id = ? ORDER BY timestamp DESC LIMIT ?) ORDER BY timestamp ASC",
            (chat_id, limit)
        ) as cursor:
            rows = await cursor.fetchall()
            return [{"role": row["role"], "content": row["content"]} for row in rows]

async def clear_history(chat_id: int):
    """Menghapus riwayat percakapan untuk chat_id tertentu."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM messages WHERE chat_id = ?", (chat_id,))
        await db.commit()
