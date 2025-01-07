import streamlit as st
import pandas as pd
import numpy as np
import ccxt  # Do komunikacji z Binance
from datetime import datetime
from streamlit.components.v1 import html
from cryptography.hazmat.primitives import hashes

digest = hashes.Hash(hashes.SHA256())
digest.update(b"Test message")
print(digest.finalize())

# Konfiguracja strony Streamlit
st.set_page_config(page_title="Trading Bot Panel", layout="wide")

# Inicjalizacja stanu sesji
if 'bot_active' not in st.session_state:
    st.session_state.bot_active = False

# Funkcja do pobrania danych w czasie rzeczywistym z Binance
def get_binance_data(trading_pair):
    """Pobiera dane rynkowe z Binance."""
    exchange = ccxt.binance()
    try:
        ticker = exchange.fetch_ticker(trading_pair)
        return {
            "symbol": trading_pair,
            "price": ticker['last'],
            "high": ticker['high'],
            "low": ticker['low'],
            "volume": ticker['quoteVolume']
        }
    except Exception as e:
        st.error(f"Błąd pobierania danych z Binance: {e}")
        return None

# Funkcja do renderowania widgetu TradingView
def render_tradingview_chart(symbol):
    """Osadza wykres TradingView dla wybranego symbolu."""
    tradingview_widget = f"""
    <div class="tradingview-widget-container" style="height: 500px;">
        <div id="tradingview_{symbol}"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
        new TradingView.widget(
        {{
            "width": "100%",
            "height": "500",
            "symbol": "{symbol}",
            "interval": "60",
            "timezone": "Etc/UTC",
            "theme": "light",
            "style": "1",
            "locale": "en",
            "toolbar_bg": "#f1f3f6",
            "enable_publishing": false,
            "allow_symbol_change": true,
            "container_id": "tradingview_{symbol}"
        }});
        </script>
    </div>
    """
    html(tradingview_widget, height=500)

# Sidebar
with st.sidebar:
    st.title("Panel Kontrolny")
    
    # Status bota
    st.header("Status Bota")
    bot_status = "Aktywny" if st.session_state.bot_active else "Nieaktywny"
    st.metric("Status", bot_status)
    
    # Przyciski kontrolne
    if st.button("Start Bot" if not st.session_state.bot_active else "Stop Bot"):
        st.session_state.bot_active = not st.session_state.bot_active
    
    # Konfiguracja
    st.header("Konfiguracja")
    trading_pair = st.selectbox(
        "Para tradingowa (Binance format)",
        ["BTC/USDT", "ETH/USDT", "BNB/USDT"]
    )
    
    risk_per_trade = st.slider(
        "Ryzyko na trade (%)",
        min_value=0.1,
        max_value=5.0,
        value=2.0,
        step=0.1
    )
    
    timeframe = st.selectbox(
        "Timeframe",
        ["1m", "5m", "15m", "1h", "4h", "1d"]
    )

# Główny layout
st.title("Trading Bot Dashboard")

# Pobieranie danych w czasie rzeczywistym
binance_data = get_binance_data(trading_pair.replace("/", ""))

if binance_data:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Aktualna cena", f"${binance_data['price']:.2f}")
    with col2:
        st.metric("Najwyższa cena", f"${binance_data['high']:.2f}")
    with col3:
        st.metric("Najniższa cena", f"${binance_data['low']:.2f}")
    with col4:
        st.metric("Wolumen", f"{binance_data['volume']:.2f}")

# Wykres TradingView
st.header("Wykres TradingView")
render_tradingview_chart(f"BINANCE:{trading_pair.replace('/', '')}")

# Tabs dla dodatkowych funkcji
tab1, tab2 = st.tabs(["Analiza Ryzyka", "Dane Historyczne i Prognoza AI"])

with tab1:
    st.subheader("Metryki Ryzyka")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Max Drawdown", "-15.3%")
        st.metric("Sharpe Ratio", "1.87")
    with col2:
        st.metric("Daily VaR", "$123.45")
        st.metric("Risk/Reward", "1.5")

with tab2:
    st.subheader("Dane Historyczne i Prognoza AI")
    st.markdown("### Prognoza AI")
    forecast = {
        '05-12-2024': '$123.45',
        '06-12-2024': '$124.67',
        '07-12-2024': '$125.34',
        '08-12-2024': '$126.78',
    }
    for date, predicted_price in forecast.items():
        st.write(f"{date}: {predicted_price}")


# streamlit run binance_his.py