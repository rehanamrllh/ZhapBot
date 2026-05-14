import os
from PIL import Image
from fpdf import FPDF
import asyncio

async def convert_image_to_pdf(image_path: str, output_path: str) -> str:
    """Mengonversi file gambar ke PDF secara asinkron."""
    def _convert():
        image = Image.open(image_path)
        # Convert to RGB to prevent errors with RGBA images (like PNGs with transparency)
        rgb_im = image.convert('RGB')
        rgb_im.save(output_path, "PDF")
        return output_path
        
    return await asyncio.to_thread(_convert)

async def convert_images_to_pdf(image_paths: list[str], output_path: str) -> str:
    """Mengonversi banyak file gambar ke 1 PDF secara asinkron."""
    if not image_paths:
        raise ValueError("Daftar gambar kosong")
        
    def _convert():
        images = []
        for path in image_paths:
            img = Image.open(path).convert('RGB')
            images.append(img)
            
        # The first image is used to save the PDF, appending the rest
        if images:
            images[0].save(output_path, "PDF", save_all=True, append_images=images[1:])
        return output_path
        
    return await asyncio.to_thread(_convert)

async def convert_text_to_pdf(text_path: str, output_path: str) -> str:
    """Mengonversi file teks (.txt) ke PDF secara asinkron."""
    def _convert():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("helvetica", size=12)
        
        with open(text_path, "r", encoding="utf-8") as f:
            for line in f:
                # Menulis teks per baris ke PDF
                # encode-decode untuk menghindari karakter tidak dikenal di font dasar
                clean_line = line.encode('latin-1', 'replace').decode('latin-1')
                pdf.multi_cell(0, 10, text=clean_line)
                
        pdf.output(output_path)
        return output_path
        
    return await asyncio.to_thread(_convert)
