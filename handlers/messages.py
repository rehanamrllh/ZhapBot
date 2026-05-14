from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from database import add_message, get_history
from ai_service import get_ai_response

router = Router()

@router.message(F.text)
async def handle_text_messages(message: Message):
    """Menangani pesan teks biasa dari pengguna."""
    chat_id = message.chat.id
    user_text = message.text

    # Beri tahu pengguna bahwa bot sedang mengetik
    await message.bot.send_chat_action(chat_id=chat_id, action="typing")

    try:
        # 1. Ambil riwayat obrolan (Context Retrieval)
        history = await get_history(chat_id, limit=20)

        # 2. Panggil AI dengan riwayat dan pesan baru (AI Processing)
        ai_reply = await get_ai_response(history, user_text)

        # 3. Simpan pesan user dan balasan AI ke database
        await add_message(chat_id, role="user", content=user_text)
        await add_message(chat_id, role="model", content=ai_reply)

        # 4. Kirim balasan ke pengguna (Response Dispatch)
        await message.answer(ai_reply)
        
    except Exception as e:
        print(f"Error handling message: {e}")
        await message.answer("Maaf, sistem mengalami gangguan saat memproses pesan Anda.")

@router.callback_query(lambda c: c.data == "summarize_chat")
async def process_callback_summarize(callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id
    
    await callback_query.answer("Meringkas percakapan...")
    await callback_query.message.bot.send_chat_action(chat_id=chat_id, action="typing")
    
    history = await get_history(chat_id, limit=30)
    if not history:
        await callback_query.message.answer("Belum ada percakapan untuk diringkas.")
        return
        
    prompt = "Tolong buatkan ringkasan singkat dari percakapan kita di atas dalam 2-3 kalimat."
    ai_reply = await get_ai_response(history, prompt)
    
    await callback_query.message.answer(f"**Ringkasan Percakapan:**\n\n{ai_reply}", parse_mode="Markdown")
