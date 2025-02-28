from flask import Flask, request, render_template, redirect, url_for
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os
from config import settings  # Optional config

app = Flask(__name__)

# Google Sheets Setup
SCOPE = ['https://www.googleapis.com/auth/spreadsheets']
CREDS = ServiceAccountCredentials.from_json_keyfile_name(
    'config/credentials.json', SCOPE
)
CLIENT = gspread.authorize(CREDS)
SHEET = CLIENT.open(settings.SPREADSHEET_NAME).sheet1  # Using config

@app.route('/')
def home():
    return "QR Attendance System - Use /attend?lecture_id=ID"

@app.route('/attend')
def attendance_form():
    lecture_id = request.args.get('lecture_id')
    return render_template('attendance.html', lecture_id=lecture_id)

@app.route('/submit', methods=['POST'])
def submit_attendance():
    lecture_id = request.form['lecture_id']
    student_id = request.form['student_id'].strip()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Check for duplicates
    records = SHEET.get_all_records()
    existing = any(
        str(row['Student ID']) == student_id and
        row['Lecture ID'] == lecture_id
        for row in records
    )

    if not existing and student_id:
        SHEET.append_row([lecture_id, student_id, timestamp])
        return redirect(url_for('success'))
    return "Attendance already recorded or invalid ID!", 400

@app.route('/success')
def success():
    return "Attendance recorded successfully!"

if __name__ == '__main__':
    os.makedirs('static/qrcodes', exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
