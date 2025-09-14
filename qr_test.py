import qrcode
from qrcode.image.pil import PilImage
import os
import uuid
import glob
import time
 
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "static", "image")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def qr_genirating(url, foreground_color, background_color):
   
    for f in glob.glob(os.path.join(OUTPUT_DIR, "qr_*.png")):
        if os.path.getmtime(f) < time.time() - 360:  
            os.remove(f)

    
    filename = f"qr_{uuid.uuid4().hex}.png"
    filepath = os.path.join(OUTPUT_DIR, filename)

    
    qr = qrcode.QRCode(
        version=5,
        box_size=40,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        border=5,
    )
    qr.add_data(url)
    image = qr.make_image(
        image_factory=PilImage,
        fill_color=foreground_color,  
        back_color=background_color   
    )
    image.save(filepath)
    print(f'QR-код создан: {filename}')

   
    return f"/static/image/{filename}"


