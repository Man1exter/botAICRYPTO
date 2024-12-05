import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import json
import time

# Konfiguracja strony Streamlit
st.set_page_config(page_title="Trading Bot Panel", layout="wide")

# Inicjalizacja stanu sesji
if 'bot_active' not in st.session_state:
    st.session_state.bot_active = False
if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now()

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
        "Para tradingowa",
        ["XDC/USDT", "BTC/USDT", "ETH/USDT"]
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

# Górne metryki
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Balans", "$10,234.56", "+$123.45")
with col2:
    st.metric("Otwarte pozycje", "3", "+1")
with col3:
    st.metric("Dzienny P/L", "+$45.67", "+2.3%")
with col4:
    st.metric("Win Rate", "67%", "+5%")

# Wykres
st.header("Wykres i Analiza")
# Przykładowe dane
dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
prices = np.random.normal(100, 10, len(dates)).cumsum()
volumes = np.random.randint(1000, 10000, len(dates))

# Tworzenie wykresu
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                    vertical_spacing=0.03, row_heights=[0.7, 0.3])

# Candlestick
fig.add_trace(go.Scatter(x=dates, y=prices, name="Price"), row=1, col=1)

# Volume
fig.add_trace(go.Bar(x=dates, y=volumes, name="Volume"), row=2, col=1)

fig.update_layout(height=600, title_text=f"{trading_pair}")
st.plotly_chart(fig, use_container_width=True)

# Pozycje i Orders
col1, col2 = st.columns(2)
with col1:
    st.subheader("Aktywne Pozycje")
    positions_data = {
        'Para': ['XDC/USDT', 'BTC/USDT'],
        'Typ': ['Long', 'Short'],
        'Wejście': [0.07429, 42150],
        'Aktualnie': [0.07450, 42100],
        'P/L': ['+2.3%', '-0.5%']
    }
    st.dataframe(pd.DataFrame(positions_data))

with col2:
    st.subheader("Aktywne Zlecenia")
    orders_data = {
        'Para': ['XDC/USDT'],
        'Typ': ['Limit Buy'],
        'Cena': [0.07200],
        'Ilość': [1000],
        'Status': ['Oczekujące']
    }
    st.dataframe(pd.DataFrame(orders_data))

# Tabs
tab1, tab2, tab3 = st.tabs(["Analiza Techniczna", "Analiza Ryzyka", "Statystyki"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Wskaźniki")
        indicators = {
            'RSI': '45.67',
            'MACD': 'Sell',
            'MA Cross': 'Buy',
            'BB Position': 'Middle'
        }
        for indicator, value in indicators.items():
            st.metric(indicator, value)
    
    with col2:
        st.subheader("Sygnały")
        signals = {
            'Trend': 'Uptrend',
            'Momentum': 'Strong',
            'Volatility': 'Medium',
            'Volume': 'Above Avg'
        }
        for signal, value in signals.items():
            st.metric(signal, value)
    

with tab2:
    st.subheader("Metryki Ryzyka")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Max Drawdown", "-15.3%")
        st.metric("Sharpe Ratio", "1.87")
    with col2:
        st.metric("Daily VaR", "$123.45")
        st.metric("Risk/Reward", "1.5")
    with col3:
        st.metric("Exposure", "45%")
        st.metric("Beta", "0.85")

with tab3:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Trading Stats")
        stats = {
            'Total Trades': '156',
            'Win Rate': '67%',
            'Avg Profit': '$34.56',
            'Avg Loss': '$23.45'
        }
        for stat, value in stats.items():
            st.metric(stat, value)
    
    with col2:
        st.subheader("Performance")
        performance = {
            'Monthly Return': '+5.67%',
            'YTD Return': '+23.45%',
            'Best Trade': '+$345.67',
            'Worst Trade': '-$123.45'
        }
        for metric, value in performance.items():
            st.metric(metric, value)
            
with tab4:
    st.subheader("Dane Historyczne i Prognoza AI")

    # Sekcja danych historycznych
    st.markdown("### Dane Historyczne Ceny")
    historical_data = {
        '01-12-2024': '$120.34',
        '02-12-2024': '$121.45',
        '03-12-2024': '$119.67',
        '04-12-2024': '$122.34',
    }
    for date, price in historical_data.items():
        st.write(f"{date}: {price}")

    # Sekcja prognozy AI
    st.markdown("### Prognoza AI")
    forecast = {
        '05-12-2024': '$123.45',
        '06-12-2024': '$124.67',
        '07-12-2024': '$125.34',
        '08-12-2024': '$126.78',
    }
    for date, predicted_price in forecast.items():
        st.write(f"{date}: {predicted_price}")
        
# streamlit run closure.py