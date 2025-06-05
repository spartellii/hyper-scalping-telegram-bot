import time
from scanner import get_klines
import requests
import pandas as pd

TOKEN = '7456761180:AAGJ1tbXIloB_P4RKdYc2e-frFOXaFLfidk'
CHAT_ID = '6156030658'

def send_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {'chat_id': CHAT_ID, 'text': message}
    requests.post(url, data=data)

def get_trend(df, short=20, long=50):
    df['ema_short'] = df['close'].ewm(span=short).mean()
    df['ema_long'] = df['close'].ewm(span=long).mean()
    if df['ema_short'].iloc[-1] > df['ema_long'].iloc[-1]:
        return "BULL"
    elif df['ema_short'].iloc[-1] < df['ema_long'].iloc[-1]:
        return "BEAR"
    return "NEUTRAL"

def macd_signal(df):
    df['ema12'] = df['close'].ewm(span=12).mean()
    df['ema26'] = df['close'].ewm(span=26).mean()
    df['macd'] = df['ema12'] - df['ema26']
    df['signal'] = df['macd'].ewm(span=9).mean()
    return df['macd'].iloc[-1] > df['signal'].iloc[-1]

def rsi_signal(df, period=14):
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1]

def atr_signal(df, period=14):
    df['high_low'] = df['high'] - df['low']
    df['high_close'] = abs(df['high'] - df['close'].shift())
    df['low_close'] = abs(df['low'] - df['close'].shift())
    df['tr'] = df[['high_low', 'high_close', 'low_close']].max(axis=1)
    df['atr'] = df['tr'].rolling(window=period).mean()
    return df['atr'].iloc[-1]

def detect_liquidity_spike(df):
    wick_threshold = 1.5
    body = abs(df['open'] - df['close'])
    wick = df['high'] - df[['open', 'close']].max(axis=1)
    signal = (wick > body * wick_threshold)
    return signal.iloc[-1]

coin_list = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", "DOGEUSDT", "ADAUSDT", "AVAXUSDT", "DOTUSDT", "SHIBUSDT",
    "LINKUSDT", "MATICUSDT", "OPUSDT", "ARBUSDT", "INJUSDT", "APTUSDT", "ATOMUSDT", "LTCUSDT", "PEPEUSDT", "RNDRUSDT",
    "SEIUSDT", "WIFUSDT", "TIAUSDT", "NEARUSDT", "SUIUSDT", "JUPUSDT", "BONKUSDT", "FTMUSDT", "TRXUSDT", "1000SATSUSDT",
    "PYTHUSDT", "STXUSDT", "COTIUSDT", "GALAUSDT", "IMXUSDT", "FETUSDT", "AGIXUSDT", "ROSEUSDT", "RUNEUSDT", "AAVEUSDT",
    "DYDXUSDT", "BLURUSDT", "LDOUSDT", "CKBUSDT", "GMXUSDT", "TWTUSDT", "DYMUSDT", "SKLUSDT", "ONEUSDT", "ENJUSDT"
]

def main():
    while True:
        for coin in coin_list:
            try:
                df_3m = get_klines(coin, interval="3m", limit=100)
                df_15m = get_klines(coin, interval="15m", limit=100)

                trend = get_trend(df_15m)
                macd_ok = macd_signal(df_3m)
                rsi = rsi_signal(df_3m)
                atr = atr_signal(df_3m)
                liq = detect_liquidity_spike(df_3m)

                if trend == "BULL" and macd_ok and rsi < 35 and liq:
                    send_message(f"📈 BUY sinyali - {coin}\nRSI: {int(rsi)} | ATR: {atr:.2f}")
                elif trend == "BEAR" and not macd_ok and rsi > 70 and liq:
                    send_message(f"📉 SELL sinyali - {coin}\nRSI: {int(rsi)} | ATR: {atr:.2f}")

                time.sleep(1)
            except Exception as e:
                print(f"{coin} - Hata: {e}")
                continue

        time.sleep(300)  # 5 dakika bekle