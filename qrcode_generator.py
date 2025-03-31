import qrcode
import os
from database import museum_database  # Убедитесь, что вы импортируете правильный экземпляр класса

OUTPUT_DIR = "qr_codes"

def generate_qr_codes():
    """Генерирует QR-коды для каждого зала и сохраняет их в файлы."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)  # Создаем папку, если её нет

    # Получаем все залы из базы данных
    halls = museum_database.get_all_halls()
    if not halls:
        print("❌ В базе данных нет залов!")
        return

    # Генерация QR-кодов по hall_id
    for hall in halls:
        hall_id = hall['id']  # Извлекаем hall_id
        hall_name = hall['name']  # Извлекаем hall_name
        
        qr_data = f"hall_id={hall_id}"  # Формируем данные для QR-кода
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        file_path = os.path.join(OUTPUT_DIR, f"hall_{hall_id}.png")
        img.save(file_path)

        print(f"✅ QR-код для зала '{hall_name}' ({hall_id}) сохранен в {file_path}")

if __name__ == "__main__":
    generate_qr_codes()