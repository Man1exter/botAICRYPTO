import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import asyncio
from binance.client import Client
from datetime import datetime, timedelta
import time

# Ustawienia API Binance (wstaw swoje klucze)
api_key = 'twoj_api_key'
api_secret = 'twoj_api_secret'

# Funkcja asynchroniczna do inicjalizacji klienta Binance
async def initialize_binance_client():
    client = Client(api_key, api_secret)
    return client

# Funkcja do pobierania danych z Binance (świece)
def get_binance_data(symbol, interval, limit=200):
    """Pobieranie danych historycznych z Binance"""
    client = asyncio.run(initialize_binance_client())  # Inicjalizacja klienta Binance
    klines = client.get_historical_klines(symbol, interval, limit=limit)
    
    # Konwersja danych do DataFrame
    data = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    data['open'] = pd.to_numeric(data['open'])
    data['high'] = pd.to_numeric(data['high'])
    data['low'] = pd.to_numeric(data['low'])
    data['close'] = pd.to_numeric(data['close'])
    data['volume'] = pd.to_numeric(data['volume'])
    data.set_index('timestamp', inplace=True)
    return data

# Funkcja do dodania wskaźników technicznych (RSI, SMA)
def add_technical_indicators(df):
    """Dodanie wskaźników technicznych do DataFrame"""
    # Obliczanie RSI (Relative Strength Index)
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    avg_gain = gain.rolling(window=14, min_periods=1).mean()
    avg_loss = loss.rolling(window=14, min_periods=1).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # Obliczanie SMA (Simple Moving Average)
    df['SMA_50'] = df['close'].rolling(window=50).mean()
    df['SMA_200'] = df['close'].rolling(window=200).mean()
    
    return df

# Funkcja do generowania sygnałów handlowych (buy/sell)
def generate_signals(df):
    """Generowanie sygnałów kupna/sprzedaży na podstawie RSI i SMA"""
    buy_signal = []
    sell_signal = []
    
    for i in range(len(df)):
        if df['RSI'][i] < 30 and df['close'][i] > df['SMA_50'][i]:
            buy_signal.append(df['close'][i])  # Kupno, gdy RSI < 30 i cena powyżej SMA 50
            sell_signal.append(np.nan)
        elif df['RSI'][i] > 70 and df['close'][i] < df['SMA_50'][i]:
            sell_signal.append(df['close'][i])  # Sprzedaż, gdy RSI > 70 i cena poniżej SMA 50
            buy_signal.append(np.nan)
        else:
            buy_signal.append(np.nan)
            sell_signal.append(np.nan)
    
    df['Buy_Signal'] = buy_signal
    df['Sell_Signal'] = sell_signal
    return df

# Funkcja do rysowania wykresu świecowego z sygnałami
def plot_candlestick_with_signals(df, symbol, interval):
    """Rysowanie wykresu świecowego z punktami wejścia/wyjścia"""
    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        name="Candlesticks"
    )])
    
    # Dodanie sygnałów kupna i sprzedaży
    fig.add_trace(go.Scatter(
        x=df.index, 
        y=df['Buy_Signal'], 
        mode='markers', 
        marker=dict(symbol='triangle-up', color='green', size=10),
        name="Buy Signal"
    ))
    
    fig.add_trace(go.Scatter(
        x=df.index, 
        y=df['Sell_Signal'], 
        mode='markers', 
        marker=dict(symbol='triangle-down', color='red', size=10),
        name="Sell Signal"
    ))
    
    # Dodanie SMA do wykresu
    fig.add_trace(go.Scatter(x=df.index, y=df['SMA_50'], line=dict(color='blue', width=2), name="SMA 50"))
    fig.add_trace(go.Scatter(x=df.index, y=df['SMA_200'], line=dict(color='orange', width=2), name="SMA 200"))
    
    # Ustawienia wykresu
    fig.update_layout(
        title=f'{symbol} - Wykres świecowy ({interval})',
        xaxis_title='Czas',
        yaxis_title='Cena',
        xaxis_rangeslider_visible=False
    )
    
    return fig

# Streamlit App UI
st.title("Bot Handlowy AI - Wykres i Analiza")

# Wybór pary walutowej i interwału
symbol = st.selectbox("Wybierz parę walutową", ["BTCUSDT", "ETHUSDT", "XRPUSDT", "ADAUSDT"])
interval = st.selectbox("Wybierz interwał", ["1m", "5m", "15m", "1h", "1d", "1w", "1M"])

# Pobieranie danych rynkowych
st.write("Pobieranie danych...")
data = get_binance_data(symbol, interval, limit=200)

# Dodanie wskaźników technicznych
data = add_technical_indicators(data)

# Generowanie sygnałów kupna i sprzedaży
data = generate_signals(data)

# Rysowanie wykresu z sygnałami
st.write("Wykres świecowy z sygnałami:")
fig = plot_candlestick_with_signals(data, symbol, interval)
st.plotly_chart(fig)

# Wyświetlanie ostatnich sygnałów
buy_signals = data[data['Buy_Signal'].notna()]
sell_signals = data[data['Sell_Signal'].notna()]

st.write(f"Ostatni sygnał kupna: {buy_signals.tail(1)}")
st.write(f"Ostatni sygnał sprzedaży: {sell_signals.tail(1)}")

# Komentarze i rekomendacje
if len(buy_signals) > 0:
    st.write("Akcja: Kup!")
elif len(sell_signals) > 0:
    st.write("Akcja: Sprzedaj!")
else:
    st.write("Akcja: Trzymaj!")

# Pokazanie wartości RSI i SMA
st.write(f"RSI: {data['RSI'].iloc[-1]}")
st.write(f"SMA 50: {data['SMA_50'].iloc[-1]}")
st.write(f"SMA 200: {data['SMA_200'].iloc[-1]}")

# Uruchomienie bota (symulacja)
if st.button("Uruchom bota"):
    st.write("Bot rozpoczął działanie...")
    while True:
        data = get_binance_data(symbol, interval, limit=200)
        data = add_technical_indicators(data)
        data = generate_signals(data)
        
        buy_signals = data[data['Buy_Signal'].notna()]
        sell_signals = data[data['Sell_Signal'].notna()]
        
        if len(buy_signals) > 0:
            st.write("Akcja: Kup!")
        elif len(sell_signals) > 0:
            st.write("Akcja: Sprzedaj!")
        else:
            st.write("Akcja: Trzymaj!")
        
        # Czekaj 60 sekund przed kolejną aktualizacją
        time.sleep(60)


#### streamlit run panel.py

