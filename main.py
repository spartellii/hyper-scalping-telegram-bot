import time
from scanner import get_klines
import requests

TOKEN = '7456761180:AAGJ1tbXIloB_P4RKdYc2e-frFOXaFLfidk'
CHAT_ID = '6156030658'

def send_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {'chat_id': CHAT_ID, 'text': message}
    requests.post(url, data=data)

def detect_qml(df):
    # Basit QML sinyal kontrolü (örnek mantık)
    # Son 10 mumdan low/high değerlerine bakar
    lows = df['low'].values[-10:]
    highs = df['high'].values[-10:]
    support = min(lows)
    resistance = max(highs)

    current_price = df['close'].values[-1]

    if current_price > resistance:
        return "BUY"
    elif current_price < support:
        return "SELL"
    else:
        return None

def main():
    coin_list = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT"]

    while True:
        for coin in coin_list:
            try:
                df = get_klines(coin, interval="3m", limit=100)
                signal = detect_qml(df)
                if signal:
                    send_message(f"📢 {signal} sinyali tespit edildi: {coin} (3m)")
                    print(f"{coin} için {signal} sinyali gönderildi.")
                time.sleep(2)
            except Exception as e:
                print(f"Hata: {e}")
                continue

        time.sleep(180)  # 3 dakikada bir tarama yap