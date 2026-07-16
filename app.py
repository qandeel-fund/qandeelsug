from flask import Flask, request, jsonify, make_response, send_from_directory
from flask_cors import CORS
import requests
import csv
from datetime import datetime
import os
import webbrowser
from threading import Timer

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app, resources={r"/*": {"origins": "*"}})

TELEGRAM_TOKEN = "8451586120:AAEEaShsVb1GvLeyVNsTJ77bYsipM6IBbkk"
MY_CHAT_ID = "1999709827"
EXCEL_FILE = "suggestions_database.csv"


def save_to_excel(name, suggestion):
    try:
        file_exists = os.path.isfile(EXCEL_FILE)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(EXCEL_FILE, mode='a', newline='', encoding='utf-8-sig', errors='ignore') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["التاريخ والوقت", "اسم المرسل", "الاقتراح"])
            writer.writerow([current_time, name, suggestion])
        print("✅ تم الحفظ في ملف الإكسل بنجاح!")
        return True
    except Exception as e:
        print("⚠️ تنبيه: لم يتم الحفظ في الإكسل:", e)
        return False


def send_to_telegram(name, suggestion):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    message_text = f"📥 **وصلك اقتراح جديد!**\n\n👤 **المرسل:** {name}\n💡 **المحتوى:**\n{suggestion}"
    payload = {"chat_id": MY_CHAT_ID, "text": message_text, "parse_mode": "Markdown"}
    try:
        response = requests.post(url, json=payload, timeout=8)
        return response.status_code == 200
    except Exception as e:
        print("⚠️ خطأ اتصال أثناء الإرسال لتليجرام:", e)
        return False


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/submit-suggestion', methods=['POST', 'OPTIONS'])
def handle_suggestion():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
        return response

    data = request.json or {}
    name = data.get('name', 'مجهول')
    suggestion = data.get('suggestion', '')

    if not suggestion:
        return jsonify({"status": "fail", "message": "الاقتراح فارغ"}), 400

    print(f"📥 جاري معالجة اقتراح جديد من: {name}...")
    excel_status = save_to_excel(name, suggestion)
    telegram_status = send_to_telegram(name, suggestion)

    if excel_status or telegram_status:
        response = jsonify({"status": "success", "message": "تم الإرسال بنجاح"})
    else:
        response = jsonify({"status": "error", "message": "فشل الإرسال الكلي"})

    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, 200


# دالة لفتح المتصفح تلقائياً
def open_browser():
    webbrowser.open_new("http://localhost:8000/")


if __name__ == '__main__':
    # تأكدي من إيقاف الـ reloader وفتح الـ host لجميع الأجهزة
    Timer(1.2, open_browser).start()
    app.run(host='0.0.0.0', debug=True, port=8000, use_reloader=False)
