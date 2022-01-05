from flask import Blueprint, render_template, jsonify
import json
from datetime import date, timedelta
import pdfkit
import os
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN')
chat_id = os.environ.get('chat_id')

gen_pdf = Blueprint('gen_pdf', __name__)

def send_pdf(dir, d):
    doc = open(f'{dir}/{d}-outt.pdf', 'rb')
    files = {'document': doc}
    requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendDocument?chat_id={chat_id}', files=files)


@gen_pdf.route('/read_file/', methods=['GET'])
def read_file():
    with open(file="test.json", mode='r') as data_file:
        data = json.load(data_file)

    length_of_file = len(data)

    today = date.today()
    yesterday = today - timedelta(days=1)
    dir = str(today)

    if not os.path.isdir(dir):
        os.mkdir(f'./{dir}')

    for d in range(0, length_of_file):
        html_data = render_template('template.html', json_data=data[d], today_date=today, yesterday_date=yesterday)
        pdfkit.from_string(html_data, f'./{dir}/{d}-outt.pdf')
        send_pdf(dir, d)
        
    
    return jsonify(msg="success")