import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime

# Konfiguracja strony Streamlit
st.set_page_config(page_title="SZERMI & INCO FOUNDATION SP Z.O.O", layout="wide")

# Dodatkowy styl CSS
st.markdown(
    """
    <style>
        /* Stylizacja sidebar */
        [data-testid="stSidebar"] {
            background-color: #222222; /* Ciemniejsze tło */
        }
        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3, 
        [data-testid="stSidebar"] h4, 
        [data-testid="stSidebar"] h5, 
        [data-testid="stSidebar"] h6,
        [data-testid="stSidebar"] label, 
        [data-testid="stSidebar"] span, 
        [data-testid="stSidebar"] button {
            color: #FFFFFF; /* Jasny kolor tekstu */
        }
        [data-testid="stSidebar"] .stMetric {
            background-color: #333333; /* Tło metryk */
            color: #FFFFFF; /* Tekst metryk */
            border-radius: 10px; /* Zaokrąglone rogi */
        }
        [data-testid="stSidebar"] .stSelectbox div, 
        [data-testid="stSidebar"] .stSlider div,
        [data-testid="stSidebar"] .stButton {
            color: #FFFFFF; /* Kolor tekstu */
        }
        [data-testid="stSidebar"] .stButton button {
            background-color: #444444; /* Przyciski */
            border: 1px solid #555555; /* Obramowanie */
            color: #FFFFFF;
        }
        [data-testid="stSidebar"] .stButton button:hover {
            background-color: #555555; /* Efekt hover */
            color: #FFFFFF;
        }
        /* Poprawa slidera */
        [data-testid="stSidebar"] .stSlider>div {
            color: #FFFFFF;
        }
        /* Stylizacja głównego layoutu */
        .main {
            background-color: #FFFFFF; /* Tło główne */
            color: #000000; /* Tekst w głównym obszarze */
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Inicjalizacja stanu sesji
if 'bot_active' not in st.session_state:
    st.session_state.bot_active = False
if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now()

# Sidebar
with st.sidebar:
    st.title("SZERMI & INCO FOUNDATION SP Z.O.O")
    
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

            
            
#### streamlit run panel.py

