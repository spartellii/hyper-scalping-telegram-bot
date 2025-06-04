import time
import requests

TOKEN = '7456761180:AAGJ1tbXIloB_P4RKdYc2e-frFOXaFLfidk'
CHAT_ID = '6156030658'

def send_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {'chat_id': CHAT_ID, 'text': message}
    requests.post(url, data=data)

while True:
    send_message("✅ Bot Render'da çalışıyor! (Hyper Scalper takipte)")
    time.sleep(3600)