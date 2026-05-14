import logging
import os
import asyncio
from aiogram import Router, F, Bot
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from states import ConvertPDFStates
from utils.pdf_converter import convert_image_to_pdf, convert_images_to_pdf, convert_text_to_pdf

logger = logging.getLogger(__name__)
router = Router()

# Delay briefly so Telegram can finish delivering all messages that belong to the same media group.
ALBUM_COLLECTION_DELAY_SECONDS = 2.0
ALBUM_DATA = {}

async def process_album(media_group_id: str, chat_id: int, bot: Bot, state: FSMContext, status_msg: Message):
    await asyncio.sleep(ALBUM_COLLECTION_DELAY_SECONDS)  # Wait for other images in the album to arrive
    
    data = ALBUM_DATA.pop(media_group_id, None)
    if not data:
        return
        
    messages = data["messages"]
    
    # Download all images
    file_paths = []
    for msg in messages:
        if msg.photo:
            photo = msg.photo[-1]
            file_path = f"temp_image_{chat_id}_{photo.file_id}.jpg"
            await bot.download(photo, destination=file_path)
            file_paths.append(file_path)
        elif msg.document:
            document = msg.document
            file_path = f"temp_image_{chat_id}_{document.file_id}.jpg"
            await bot.download(document, destination=file_path)
            file_paths.append(file_path)
            
    output_pdf_path = f"output_{chat_id}_{media_group_id}.pdf"
    
    try:
        await convert_images_to_pdf(file_paths, output_pdf_path)
        pdf_file = FSInputFile(output_pdf_path, filename="Converted_Group.pdf")
        await bot.send_document(chat_id, pdf_file, caption="Ini adalah file PDF dari grup gambar Anda!")
        try:
            await status_msg.delete()
        except Exception:
            logger.debug("Tidak dapat menghapus pesan status album untuk chat %s", chat_id, exc_info=True)
    except Exception:
        logger.exception("Terjadi kesalahan saat konversi album untuk chat %s", chat_id)
        await bot.send_message(chat_id, "Terjadi kesalahan saat konversi album. Silakan coba lagi.")
    finally:
        for p in file_paths:
            if os.path.exists(p):
                os.remove(p)
        if os.path.exists(output_pdf_path):
            os.remove(output_pdf_path)
            
    await state.clear()

@router.message(ConvertPDFStates.waiting_for_file, F.photo)
async def handle_photo_to_pdf(message: Message, state: FSMContext, bot: Bot):
    """Menangani kiriman foto untuk dikonversi ke PDF."""
    if message.media_group_id:
        group_id = message.media_group_id
        if group_id not in ALBUM_DATA:
            status_msg = await message.answer("Sedang memproses grup gambar, mohon tunggu...")
            ALBUM_DATA[group_id] = {"messages": [], "status_msg": status_msg}
            asyncio.create_task(process_album(group_id, message.chat.id, bot, state, status_msg))
            
        ALBUM_DATA[group_id]["messages"].append(message)
        return

    await message.answer("Sedang memproses gambar, mohon tunggu...")
    
    # Ambil resolusi tertinggi dari foto
    photo = message.photo[-1]
    file_id = photo.file_id
    
    # Download file sementara
    file_path = f"temp_image_{message.chat.id}.jpg"
    await bot.download(photo, destination=file_path)
    
    output_pdf_path = f"output_{message.chat.id}.pdf"
    
    try:
        await convert_image_to_pdf(file_path, output_pdf_path)
        pdf_file = FSInputFile(output_pdf_path, filename="Converted_Image.pdf")
        await message.answer_document(pdf_file, caption="Ini adalah file PDF Anda!")
    except Exception:
        logger.exception("Terjadi kesalahan saat konversi foto untuk chat %s", message.chat.id)
        await message.answer("Terjadi kesalahan saat konversi. Silakan coba lagi.")
    finally:
        # Bersihkan file sementara
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(output_pdf_path):
            os.remove(output_pdf_path)
            
    # Hapus state
    await state.clear()

@router.message(ConvertPDFStates.waiting_for_file, F.document)
async def handle_document_to_pdf(message: Message, state: FSMContext, bot: Bot):
    """Menangani kiriman dokumen (teks atau gambar sebagai file) untuk dikonversi."""
    document = message.document
    file_name = document.file_name.lower()
    
    if file_name.endswith(('.jpg', '.jpeg', '.png')):
        if message.media_group_id:
            group_id = message.media_group_id
            if group_id not in ALBUM_DATA:
                status_msg = await message.answer("Sedang memproses grup dokumen gambar, mohon tunggu...")
                ALBUM_DATA[group_id] = {"messages": [], "status_msg": status_msg}
                asyncio.create_task(process_album(group_id, message.chat.id, bot, state, status_msg))
                
            ALBUM_DATA[group_id]["messages"].append(message)
            return

        file_path = f"temp_image_{message.chat.id}_{document.file_name}"
        output_pdf_path = f"output_{message.chat.id}.pdf"
        
        await message.answer("Sedang memproses dokumen gambar, mohon tunggu...")
        await bot.download(document, destination=file_path)
        
        try:
            await convert_image_to_pdf(file_path, output_pdf_path)
            pdf_file = FSInputFile(output_pdf_path, filename="Converted_Image.pdf")
            await message.answer_document(pdf_file, caption="Ini adalah file PDF Anda!")
        except Exception:
            logger.exception("Terjadi kesalahan saat konversi dokumen gambar untuk chat %s", message.chat.id)
            await message.answer("Terjadi kesalahan saat konversi. Silakan coba lagi.")
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)
            if os.path.exists(output_pdf_path):
                os.remove(output_pdf_path)
            
        await state.clear()
        
    elif file_name.endswith('.txt'):
        file_path = f"temp_text_{message.chat.id}.txt"
        output_pdf_path = f"output_{message.chat.id}.pdf"
        
        await message.answer("Sedang memproses file teks, mohon tunggu...")
        await bot.download(document, destination=file_path)
        
        try:
            await convert_text_to_pdf(file_path, output_pdf_path)
            pdf_file = FSInputFile(output_pdf_path, filename="Converted_Text.pdf")
            await message.answer_document(pdf_file, caption="Ini adalah file PDF Anda!")
        except Exception:
            logger.exception("Terjadi kesalahan saat konversi teks untuk chat %s", message.chat.id)
            await message.answer("Terjadi kesalahan saat konversi teks. Silakan coba lagi.")
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)
            if os.path.exists(output_pdf_path):
                os.remove(output_pdf_path)
            
        await state.clear()
    else:
        await message.answer(
            "Maaf, format file tersebut belum didukung.\n"
            "Harap kirimkan file teks (.txt) atau gambar (JPG/PNG)."
        )
        # Jangan clear state, agar user bisa mengirim file yang benar
