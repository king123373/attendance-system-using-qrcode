import qrcode
from datetime import datetime
import os
from config import settings  # Optional config


def generate_qr():
    # Create output directory
    os.makedirs(settings.QR_SAVE_PATH, exist_ok=True)

    # Generate unique lecture ID
    lecture_id = datetime.now().strftime("%Y%m%d%H%M")
    url = f"http://localhost:5000/attend?lecture_id={lecture_id}"  # Update URL for production

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f"{settings.QR_SAVE_PATH}/lecture_{lecture_id}.png")
    print(f"QR generated: lecture_{lecture_id}.png")


if __name__ == '__main__':
    generate_qr()
