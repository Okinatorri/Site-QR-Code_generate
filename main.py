from flask import Flask, render_template, request, jsonify, send_file
from qr_test import qr_genirating as make_qr_2
import os

app = Flask(__name__)





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
        data = request.json
        url = data.get('url', '')
        foreground_color = data.get('foregroundColor', '#000000')
        background_color = data.get('backgroundColor', '#FFFFFF')
        print('Yes')

        resultt = make_qr_2(url, foreground_color, background_color)

        return jsonify({
            "status": "done",
            'file': resultt
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

