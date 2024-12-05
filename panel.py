import asyncio
from binance.client import Client
from binance.exceptions import BinanceAPIException
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Klucze API Binance (podmień na swoje klucze)
API_KEY = "your_api_key_here"
API_SECRET = "your_api_secret_here"

# Funkcja do inicjalizacji klienta Binance z obsługą asyncio
async def initialize_binance_client():
    try:
        client = Client(API_KEY, API_SECRET)
        server_time = client.get_server_time()
        return client, server_time
    except BinanceAPIException as e:
        st.error(f"Błąd API Binance: {e}")
        return None, None

# Funkcja synchronizująca dla Streamlit
def get_binance_client():
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        client, server_time = loop.run_until_complete(initialize_binance_client())
        return client, server_time
    except Exception as e:
        st.error(f"Błąd inicjalizacji klienta Binance: {e}")
        return None, None

# Funkcja wylogowania (zamyka aplikację)
def logout():
    st.stop()

# Konfiguracja strony Streamlit
st.set_page_config(page_title="Trading Bot Panel", layout="wide")

# Sidebar
with st.sidebar:
    st.title("Panel Kontrolny")
    
    # Status API
    client, server_time = get_binance_client()
    if client:
        st.success(f"Połączono z Binance! Serwerowy czas: {server_time}")
    else:
        st.error("Nie udało się połączyć z Binance.")
    
    # Wybór pary tradingowej
    if client:
        symbol = st.selectbox("Wybierz parę tradingową:", ["BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT"])
        st.write(f"Wybrana para: {symbol}")
    
    # Wybór interwału
    interval = st.selectbox("Wybierz interwał:", ["1m", "5m", "15m", "30m", "1h", "4h", "12h", "1d", "3d", "1w", "1M"])
    
    # Przyciski kontrolne
    if st.button("Wyloguj"):
        logout()

# Główna sekcja
st.title("Trading Bot Dashboard")
st.header("Aktualne dane rynkowe")

if client:
    try:
        # Pobieranie danych o tickerze
        ticker = client.get_ticker(symbol=symbol)
        
        # Wyświetlanie danych
        st.metric("Symbol", ticker['symbol'])
        st.metric("Ostatnia cena", f"${ticker['lastPrice']}")
        st.metric("Najwyższa cena (24h)", f"${ticker['highPrice']}")
        st.metric("Najniższa cena (24h)", f"${ticker['lowPrice']}")
        st.metric("Zmiana procentowa (24h)", f"{ticker['priceChangePercent']}%")
    except BinanceAPIException as e:
        st.error(f"Błąd podczas pobierania danych: {e}")
else:
    st.warning("Połączenie z Binance nie jest aktywne.")

# Pobieranie danych OHLC w zależności od wybranego interwału
st.header("Dane OHLC (z interwałem)")

if client:
    try:
        # Pobieranie danych OHLC
        klines = client.get_klines(symbol=symbol, interval=interval, limit=100)
        df = pd.DataFrame(klines, columns=[
            "timestamp", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "number_of_trades",
            "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
        ])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df["open"] = pd.to_numeric(df["open"])
        df["high"] = pd.to_numeric(df["high"])
        df["low"] = pd.to_numeric(df["low"])
        df["close"] = pd.to_numeric(df["close"])

        # Wyświetlanie DataFrame
        st.dataframe(df[["timestamp", "open", "high", "low", "close", "volume"]])

        # Tworzenie wykresu świecowego
        fig = go.Figure(data=[go.Candlestick(
            x=df["timestamp"],
            open=df["open"],
            high=df["high"],
            low=df["low"],
            close=df["close"],
            name="Candlesticks"
        )])
        fig.update_layout(title=f"Wykres cenowy {symbol} ({interval})", xaxis_title="Czas", yaxis_title="Cena (USDT)")
        st.plotly_chart(fig, use_container_width=True)

    except BinanceAPIException as e:
        st.error(f"Błąd podczas pobierania danych do wykresu: {e}")
    except Exception as e:
        st.error(f"Błąd: {e}")
else:
    st.warning("Wykres nie może zostać załadowany bez aktywnego połączenia z Binance.")


            
#### streamlit run panel.py

