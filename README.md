# QR Code Based Classroom Attendance System

## Overview
This is a Flask-based QR Code attendance system designed for classroom use. The system generates dynamic QR codes that refresh every 10 seconds, ensuring secure and automated attendance marking. Students must be connected to a specific mobile hotspot to validate attendance via a Google Form.

## Features
- Generates dynamic QR codes that refresh every 10 seconds.
- Assigns subjects to lectures automatically.
- Restricts attendance marking to students connected to a specified WiFi network.
- Redirects students to a Google Form for attendance submission.
- Displays the current lecture, subject, and time on the web UI.
- Allows testing of user IP detection.

## Technologies Used
- Python
- Flask
- QR Code Generation (`qrcode` library)
- HTML & CSS
- Google Forms (for attendance collection)

## Project Structure
```
qr-attendance-system/
│
├── app.py                # Main Flask application
├── static/
│   ├── qr_code.png      # QR code image (auto-generated)
├── README.md             # Documentation
```

## Installation & Setup
### Prerequisites
Make sure you have Python installed. You also need Flask and QR Code libraries.

### Install Dependencies
```sh
pip install flask qrcode[pil]
```

### Run the Application
```sh
python app.py
```

### Access the System
- Open a browser and visit: `http://192.168.137.1:5000`
- To test IP detection: `http://192.168.137.1:5000/check_ip`
- QR Code will refresh every 10 seconds.

## How It Works
1. The system automatically detects the current lecture based on time.
2. A new QR code is generated and displayed on the webpage.
3. Students scan the QR code using their devices.
4. The system checks if the student is connected to the correct WiFi network.
5. If valid, the student is redirected to the Google Form for attendance submission.

## Configuration
### Modify Google Form Link
Replace the `GOOGLE_FORM_URL` in `app.py` with your actual Google Form link:
```python
GOOGLE_FORM_URL = "https://docs.google.com/forms/d/e/your-form-id/viewform?usp=dialog"
```

### Change Lecture Timings
Modify the `LECTURE_SUBJECTS` dictionary in `app.py` to match your schedule:
```python
LECTURE_SUBJECTS = {
    1: ("Mathematics", "9:00 AM - 10:00 AM"),
    2: ("Physics", "10:00 AM - 11:00 AM"),
    # Add more subjects as needed
}
```

### Update Hotspot IP Prefix
Modify `ALLOWED_IP_PREFIX` to match your mobile hotspot’s IP range:
```python
ALLOWED_IP_PREFIX = "192.168.137."
```

## Troubleshooting
- **QR Code Not Updating?** Restart the Flask app (`Ctrl + C`, then `python app.py`).
- **Cannot Access From Mobile?** Ensure your laptop is running the hotspot and your phone is connected.
- **IP Not Detected Correctly?** Visit `http://192.168.137.1:5000/check_ip` to check the detected IP.

## License
This project is for educational purposes only. Modify and use it as needed.

---
Developed for classroom automation and efficiency. 🚀

