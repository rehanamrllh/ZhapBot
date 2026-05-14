import logging

from google import genai
from google.genai import types
from config import GEMINI_API_KEY

logger = logging.getLogger(__name__)
client = genai.Client(api_key=GEMINI_API_KEY)

async def get_ai_response(history: list, new_message: str) -> str:
    """
    Mengirimkan riwayat percakapan dan pesan baru ke Gemini, lalu mengembalikan respons.
    """
    contents = []
    
    # Masukkan system instruction sebagai pesan pertama atau gabungkan dengan histori
    system_instruction = "Kamu adalah asisten AI yang ramah, membantu, dan menggunakan bahasa Indonesia. Jawab dengan ringkas."
    
    # Bangun context history
    for msg in history:
        # Pengecekan role yang valid untuk Gemini (user, model)
        role = "user" if msg["role"] == "user" else "model"
        contents.append(
            types.Content(
                role=role,
                parts=[types.Part.from_text(text=msg["content"])]
            )
        )
    
    # Tambahkan pesan baru dari user
    contents.append(
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=new_message)]
        )
    )

    try:
        # Kita panggil Gemini secara asynchronous menggunakan aio
        response = await client.aio.models.generate_content(
            model='gemini-2.5-flash',
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7
            )
        )
        return response.text
    except Exception as e:
        logger.exception("Error AI: %s", e)
        return "Maaf, terjadi kesalahan saat memproses permintaanmu. Coba lagi nanti."
