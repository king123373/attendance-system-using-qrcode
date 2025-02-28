import os
import time
import qrcode
from flask import Flask, render_template_string
from threading import Thread
from datetime import datetime

app = Flask(_name_)

# Google Form Base URL (Replace with your actual form URL)
GOOGLE_FORM_URL = "https://docs.google.com/forms/d/e/YOUR_FORM_ID/viewform"

# Subject Mapping for Each Lecture
LECTURE_SUBJECTS = {
    1: ("Mathematics", "9:00 AM - 10:00 AM"),
    2: ("Physics", "10:00 AM - 11:00 AM"),
    3: ("Chemistry", "11:00 AM - 12:00 PM"),
    4: ("Biology", "12:00 PM - 1:00 PM"),
    5: ("Computer Science", "2:00 PM - 3:00 PM"),
    6: ("English", "3:00 PM - 4:00 PM")
}

# HTML template to display the QR Code
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>QR Code Based Attendance System</title>
    <meta http-equiv="refresh" content="10"> <!-- Auto-refresh every 10 seconds -->
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            background-color: #f4f4f4;
            padding: 20px;
        }
        h1 {
            color: #222;
        }
        h2 {
            color: #333;
        }
        .container {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            display: inline-block;
        }
        img {
            margin-top: 20px;
            border: 5px solid #333;
            border-radius: 10px;
        }
    </style>
</head>
<body>
    <h1>QR Code Based Attendance System</h1>
    <div class="container">
        <h2>Scan the QR Code for Attendance</h2>
        <h3>Lecture {{ lecture_number }} - {{ subject_name }}</h3>
        <h4>Time: {{ lecture_time }}</h4>
        <img src="{{ url_for('static', filename='qr_code.png') }}" alt="QR Code" width="300" height="300"/>
        <p>QR Code refreshes every 10 seconds.</p>
        <p>Or click here to open the form: <a href="{{ form_url }}" target="_blank">Google Form</a></p>
    </div>
</body>
</html>
"""


# Function to generate QR code
def generate_qr_code(lecture_number):
    timestamp = int(time.time())  # Unique identifier for each QR code
    form_url = f"{GOOGLE_FORM_URL}?entry.987654321={timestamp}"  # Modify URL with timestamp

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(form_url)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")
    img_path = "static/qr_code.png"
    os.makedirs("static", exist_ok=True)
    img.save(img_path)  # Save QR code

    subject_name, lecture_time = LECTURE_SUBJECTS.get(lecture_number, ("Unknown Subject", "Unknown Time"))
    return img_path, form_url, subject_name, lecture_time


def auto_update_qr():
    while True:
        current_lecture = (int(time.time()) // 10) % 6 + 1  # Auto-cycle lectures every 10 sec
        generate_qr_code(current_lecture)
        time.sleep(10)


@app.route('/')
def home():
    current_lecture = (int(time.time()) // 10) % 6 + 1
    qr_code_path, form_url, subject_name, lecture_time = generate_qr_code(current_lecture)  # Generate a new QR code
    return render_template_string(HTML_TEMPLATE, form_url=form_url, lecture_number=current_lecture,
                                  subject_name=subject_name, lecture_time=lecture_time)


if _name_ == '_main_':
    Thread(target=auto_update_qr, daemon=True).start()  # Start auto-refreshing QR code in background
    app.run(debug=True)
