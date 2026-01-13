from flask import Flask, render_template, request, jsonify, send_file
from qr_test import qr_genirating as make_qr_2
import os
from PIL import Image

app = Flask(__name__)

os.makedirs('uploads', exist_ok=True)





@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')
 

@app.route('/Qr_code')
def Qr():
    return render_template('Qr_generate.html')







@app.route("/make_qr", methods=["POST"])
def make_qr():
    try:
        # ----- текстовые данные -----
        url = request.form.get('url', '')
        foreground_color = request.form.get('foregroundColor', '#000000')
        background_color = request.form.get('backgroundColor')

                # --- тень ---
        shadow_enabled = request.form.get('shadowEnabled') == 'on'
        shadow_color = request.form.get('shadowColor') or "#000000"


        if not background_color or background_color.strip() == "":
            background_color = None   # означает "прозрачный"

        print("URL:", url)
        print("FG:", foreground_color)
        print("BG:", background_color)

        # ----- файл (если есть) -----
        bg_path = None
        bg_image = request.files.get('backgroundImage')
        bg_pil = None
        if bg_image and bg_image.filename:
            print("Картинка получена:", bg_image.filename)
            bg_pil = Image.open(bg_image.stream).convert("RGBA")
            # сохраняем загруженную картинку


        # ----- генерация QR -----
        resultt = make_qr_2(
            url,
            foreground_color,
            background_color,
            bg_image=bg_pil,
            shadow_enabled=shadow_enabled,
            shadow_color=shadow_color
        )


        return jsonify({
            "status": "done",
            "file": resultt
        })

    except Exception as e:
        print(f"Ошибка: {str(e)}")
        return jsonify({'status': False}), 500



 
@app.route('/download')
def download_qr():
    file_url = request.args.get('file')
    if not file_url:
        return 'Файл не указан', 400

    # убираем /static/ и делаем абсолютный путь
    safe_path = file_url.replace("/static/", "", 1)
    filepath = os.path.join(app.static_folder, safe_path)

    if not os.path.exists(filepath):
        return 'Файл не найден', 404

    return send_file(filepath, as_attachment=True, download_name='qr.png')



if __name__ == '__main__':
    app.run(debug=True)

