from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
from database import museum_database

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/nav')
def navigation():
    return render_template('nav.html')


@app.route('/scan_qr', methods=['POST'])
def scan_qr():
    print("Получен запрос на обработку QR-кода")

    if 'image' not in request.files:
        return jsonify({"error": "Файл изображения не найден"}), 400

    file = request.files['image']
    img_np = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

    decoded_objects = pyzbar.decode(img)
    if decoded_objects:
        qr_data = decoded_objects[0].data.decode("utf-8")
        print(f"QR-код распознан: {qr_data}")

        # Извлекаем hall_id из QR-кода
        try:
            hall_id = int(qr_data.split('=')[1])  # Предполагаем, что QR-код имеет формат hall_id=1
        except (IndexError, ValueError):
            return jsonify({"error": "Неверный формат QR-кода"}), 400

        # Получаем название зала по hall_id
        hall_name = museum_database.get_hall_name_by_id(hall_id)
        if hall_name:
            return jsonify({"hall": f"Вы находитесь в зале {hall_id} ({hall_name})"})
        else:
            return jsonify({"error": "Зал не найден"}), 404
    else:
        return jsonify({"error": "QR-код не найден"}), 400

@app.route('/get_halls', methods=['GET'])
def get_halls():
    halls = museum_database.get_all_halls()
    return jsonify(halls)

@app.route('/find_route', methods=['GET'])
def find_route():
    from_hall_id = request.args.get('from_hall_id', type=int)
    to_hall_id = request.args.get('to_hall_id', type=int)
    route_description = museum_database.find_route(from_hall_id, to_hall_id)  # Вызов метода
    return route_description


if __name__ == '__main__':
    app.run(debug=True)