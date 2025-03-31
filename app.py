from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/nav')
def navigation():
    return render_template('nav.html')

@app.route('/scan_qr', methods=['GET', 'POST'])
def scan_qr():
    if 'image' not in request.files:
        return jsonify({"error": "Файл изображения не найден"}), 400

    file = request.files['image']
    img_np = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

    # Распознаём QR-код
    decoded_objects = pyzbar.decode(img)
    if decoded_objects:
        qr_data = decoded_objects[0].data.decode("utf-8")
        return jsonify({"hall": f"Вы находитесь в зале: {qr_data}"})
    else:
        return jsonify({"hall": "QR-код не найден"}), 400


if __name__ == '__main__':
    app.run(debug=True)