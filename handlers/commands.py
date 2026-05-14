from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from database import clear_history
from keyboards.inline import get_main_keyboard
from states import ConvertPDFStates

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    """Menangani perintah /start."""
    await message.answer(
        f"Halo {message.from_user.first_name}! 👋\n\n"
        "Saya adalah bot AI asisten Anda. Silakan ketikkan pesan, dan saya akan menjawabnya dengan mengingat konteks obrolan kita.\n\n"
        "Gunakan tombol di bawah ini atau perintah /help untuk opsi lainnya.",
        reply_markup=get_main_keyboard()
    )

@router.message(Command("help"))
async def cmd_help(message: Message):
    """Menangani perintah /help."""
    help_text = (
        "🤖 **Bantuan Bot AI**\n\n"
        "/start - Memulai percakapan\n"
        "/convertpdf - Mengkonversi file menjadi PDF\n"
        "/clear - Menghapus memori percakapan\n"
        "/help - Menampilkan pesan bantuan ini\n\n"
        "Anda bisa langsung mengetik pesan apa saja, dan AI akan merespons!"
    )
    await message.answer(help_text, parse_mode="Markdown")

@router.message(Command("clear"))
async def cmd_clear(message: Message):
    """Menangani perintah /clear."""
    await clear_history(message.chat.id)
    await message.answer("🧹 Memori obrolan telah dihapus! Mari mulai topik baru.")

@router.message(Command("convertpdf"))
async def cmd_convertpdf(message: Message, state: FSMContext):
    """Menangani perintah /convertpdf."""
    await state.set_state(ConvertPDFStates.waiting_for_file)
    info_text = (
        "📄 **Mode Konversi ke PDF Aktif**\n\n"
        "Saat ini format yang didukung adalah:\n"
        "1. **Gambar**: JPG, PNG, dll. *(Jika Anda mengirimkan grup gambar/album, bot otomatis menyatukannya menjadi 1 PDF)*.\n"
        "2. **Teks**: File berekstensi `.txt`\n\n"
        "Silakan kirimkan file yang ingin dikonversi sekarang.\n"
        "Ketik /cancel jika Anda ingin membatalkan."
    )
    await message.answer(info_text, parse_mode="Markdown")

@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    """Membatalkan proses FSM yang sedang berjalan."""
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer("Proses dibatalkan. Anda kembali ke mode percakapan normal AI.")

# --- Callback Handlers (Untuk tombol Inline) ---

@router.callback_query(lambda c: c.data == "clear_memory")
async def process_callback_clear(callback_query: CallbackQuery):
    await clear_history(callback_query.message.chat.id)
    await callback_query.answer("Memori obrolan dihapus!")
    await callback_query.message.answer("🧹 Memori obrolan telah dihapus! Mari mulai topik baru.")

@router.callback_query(lambda c: c.data == "help_menu")
async def process_callback_help(callback_query: CallbackQuery):
    await callback_query.answer()
    await cmd_help(callback_query.message)
