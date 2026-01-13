import qrcode
from PIL import Image, ImageDraw, ImageFilter
import os
import uuid
import glob
import time

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "static", "image")
os.makedirs(OUTPUT_DIR, exist_ok=True)
BG_IMAGE_DEFAULT = os.path.join(OUTPUT_DIR, "elka_u_kamina_1.jpg")  # фон по умолчанию

def qr_genirating(url, foreground_color="#000000", background_color=None,
                  bg_image=None, shadow_enabled=True, shadow_color="#000000"):

    # --- удаляем старые QR ---
    for f in glob.glob(os.path.join(OUTPUT_DIR, "qr_*.png")):
        if os.path.getmtime(f) < time.time() - 30:  # 1 час
            os.remove(f)

    # --- уникальное имя ---
    filename = f"qr_{uuid.uuid4().hex}.png"
    filepath = os.path.join(OUTPUT_DIR, filename)

    # --- создаём QR ---
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )
    qr.add_data(url)
    qr.make(fit=True)
    matrix = qr.get_matrix()
    size = len(matrix)
    scale = 20  # масштаб одного квадратика
    qr_pixel_size = size * scale

    # --- создаём фон ---
    if background_color:
        bg = Image.new('RGBA', (qr_pixel_size, qr_pixel_size), background_color)
    else:
        if bg_image:
            bg = bg_image.resize((qr_pixel_size, qr_pixel_size))
        else:
            raise ValueError("Нет цвета фона и нет картинки!")


    # --- прозрачный слой для QR ---
    qr_image = Image.new('RGBA', (qr_pixel_size, qr_pixel_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(qr_image)
    for y in range(size):
        for x in range(size):
            if matrix[y][x]:
                x0, y0 = x * scale, y * scale
                x1, y1 = x0 + scale, y0 + scale
                draw.rectangle([x0, y0, x1, y1], fill=foreground_color)

    # --- создаём тень (опционально) ---
    if shadow_enabled:
        mask = Image.new("L", qr_image.size, 0)
        mask_draw = ImageDraw.Draw(mask)
        for y in range(size):
            for x in range(size):
                if matrix[y][x]:
                    expand = scale // 2
                    x0 = max(0, x*scale - expand)
                    y0 = max(0, y*scale - expand)
                    x1 = min(qr_image.width, (x+1)*scale + expand)
                    y1 = min(qr_image.height, (y+1)*scale + expand)
                    mask_draw.rectangle([x0, y0, x1, y1], fill=255)

        mask = mask.filter(ImageFilter.GaussianBlur(scale * 0.5))
        dark_overlay = Image.new("RGBA", qr_image.size, shadow_color + '80')  # прозрачность ~50%
        dark_overlay.putalpha(mask)
        bg_with_shadow = Image.alpha_composite(bg, dark_overlay)
    else:
        bg_with_shadow = bg

    # --- накладываем QR на фон (с тенью или без) ---
    result = Image.alpha_composite(bg_with_shadow, qr_image)

    # --- сохраняем ---
    result.save(filepath)
    print(f'QR-код создан: {filename}')

    return f"/static/image/{filename}"
