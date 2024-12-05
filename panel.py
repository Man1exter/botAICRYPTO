import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf
from binance.client import Client
import ta
from sklearn.preprocessing import MinMaxScaler

# Inicjalizacja klienta Binance API
api_key = 'your_api_key'  # Podaj swój klucz API
api_secret = 'your_api_secret'  # Podaj swój sekret API
client = Client(api_key, api_secret)

# Pobieranie danych OHLCV z Binance
def get_binance_data(symbol, interval, start_str):
    klines = client.get_historical_klines(symbol, interval, start_str)
    
    # Zamiana na DataFrame
    data = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    data['close'] = pd.to_numeric(data['close'])
    
    return data[['timestamp', 'close']]

# Przygotowanie danych do modelu AI
scaler = MinMaxScaler(feature_range=(0, 1))

def prepare_data(data, look_back=60):
    data_scaled = scaler.fit_transform(data[['close']].values)
    X, y = [], []
    
    for i in range(look_back, len(data)):
        X.append(data_scaled[i-look_back:i, 0])
        y.append(data_scaled[i, 0])
    
    X, y = np.array(X), np.array(y)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))
    
    return X, y

# Model LSTM do przewidywania ceny
def build_model(input_shape):
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.LSTM(units=50, return_sequences=True, input_shape=input_shape))
    model.add(tf.keras.layers.LSTM(units=50))
    model.add(tf.keras.layers.Dense(units=1))  # Prognoza ceny
    
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# Prosta strategia handlowa
def trading_strategy(row):
    if row['RSI'] < 30 and row['MACD'] > 0:  # Przykładowe warunki na zakup
        return 'buy'
    elif row['RSI'] > 70 and row['MACD'] < 0:  # Warunki na sprzedaż
        return 'sell'
    else:
        return 'hold'

# Tworzenie panelu użytkownika w Streamlit
st.set_page_config(page_title="AI Trading Dashboard", page_icon=":chart_with_upwards_trend:", layout="wide")

# Ciemny motyw dla całej aplikacji
st.markdown(
    """
    <style>
    body {
        background-color: #2E2E2E;
        color: white;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
    }
    .stSlider>div>div>div {
        background-color: #555555;
    }
    .stTextInput>div>div>input {
        background-color: #555555;
        color: white;
    }
    .stTextArea>div>div>textarea {
        background-color: #555555;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True
)

# Nagłówek
st.title("AI Trading Dashboard")

# Użytkownik wybiera saldo początkowe
initial_balance = st.number_input("Podaj początkowy stan konta:", min_value=1.0, value=1000.0, step=0.01)
st.write(f"Twoje saldo: ${initial_balance}")

# Wybór pary walutowej i interwału
symbol = st.selectbox("Wybierz parę walutową", ["BTC/USDT", "ETH/USDT", "BNB/USDT"])
interval = st.selectbox("Wybierz interwał czasowy", ["1h", "1d", "5m", "15m"])

# Pobranie danych historycznych
data = get_binance_data(symbol, interval, "30 days ago UTC")

# Obliczanie wskaźników technicznych
data['SMA'] = ta.trend.sma_indicator(data['close'], window=14)
data['RSI'] = ta.momentum.rsi(data['close'], window=14)
data['MACD'] = ta.trend.macd(data['close'])

# Tworzenie sygnałów handlowych
data['signal'] = data.apply(trading_strategy, axis=1)

# Wizualizacja wykresu ceny
st.subheader("Wykres cenowy")
st.line_chart(data[['timestamp', 'close']].set_index('timestamp'))

# Przygotowanie danych do modelu AI
X, y = prepare_data(data)

# Budowanie i trenowanie modelu
model = build_model((X.shape[1], 1))
model.fit(X, y, epochs=10, batch_size=32)

# Prognoza ceny
predicted_price = model.predict(X)
predicted_price = scaler.inverse_transform(predicted_price)
st.subheader("Prognoza ceny")
st.write(f"Przewidywana cena dla następnego punktu: ${predicted_price[-1][0]:.2f}")

# Wyświetlanie sygnałów i wskaźników
st.subheader("Sygnały handlowe")
st.write(data[['timestamp', 'close', 'RSI', 'MACD', 'signal']].tail())

# Testowanie wyników strategii (prosty backtest)
st.write("Testowanie wyników strategii (prosty backtest):")

# Przykładowy prosty backtest - sumowanie wyników
balance = initial_balance
for index, row in data.iterrows():
    if row['signal'] == 'buy' and balance > 0:
        buy_price = row['close']
        balance -= buy_price  # kupujemy po cenie zamknięcia
        st.write(f"Kupiono za {buy_price} na {row['timestamp']}")
    elif row['signal'] == 'sell' and balance < initial_balance:
        sell_price = row['close']
        balance += sell_price  # sprzedajemy po cenie zamknięcia
        st.write(f"Sprzedano za {sell_price} na {row['timestamp']}")

st.write(f"Końcowy stan konta po strategii: ${balance:.2f}")

#### import logging -- streamlit run panel.py

