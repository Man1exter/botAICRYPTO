import sys
import pandas as pd
import numpy as np
import ccxt
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QHBoxLayout
)
from PySide6.QtCharts import QChart, QChartView, QCandlestickSeries, QCandlestickSet, QLineSeries
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter

# Funkcja do pobrania danych z giełdy Binance
def get_binance_data(symbol, timeframe, limit=500):
    exchange = ccxt.binance()
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    data = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    return data

# Funkcja do obliczenia poziomów Fibonacciego
def calculate_fibonacci_levels(data):
    high = data['high'].max()
    low = data['low'].min()
    diff = high - low

    levels = {
        '0%': high,
        '23.6%': high - 0.236 * diff,
        '38.2%': high - 0.382 * diff,
        '50%': high - 0.5 * diff,
        '61.8%': high - 0.618 * diff,
        '76.4%': high - 0.764 * diff,
        '100%': low
    }
    return levels

# Główna klasa aplikacji
class CryptoFibonacciBot(QMainWindow):
    def __init__(self):
        super().__init__()

        # Ustawienia okna głównego
        self.setWindowTitle("Crypto Fibonacci Bot")
        self.setGeometry(100, 100, 1200, 800)

        # Główny widget
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        # Nagłówek
        self.header = QLabel("Crypto Fibonacci Bot", self)
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setStyleSheet("font-size: 24px; font-weight: bold; padding: 10px;")
        self.layout.addWidget(self.header)

        # Panel konfiguracji
        self.config_layout = QHBoxLayout()
        self.layout.addLayout(self.config_layout)

        self.symbol_label = QLabel("Wybierz parę:")
        self.config_layout.addWidget(self.symbol_label)

        self.symbol_select = QComboBox()
        self.symbol_select.addItems(["BTC/USDT", "ETH/USDT", "BNB/USDT"])
        self.config_layout.addWidget(self.symbol_select)

        self.timeframe_label = QLabel("Interwał:")
        self.config_layout.addWidget(self.timeframe_label)

        self.timeframe_select = QComboBox()
        self.timeframe_select.addItems(["1m", "5m", "15m", "1h", "4h", "1d"])
        self.config_layout.addWidget(self.timeframe_select)

        self.fetch_button = QPushButton("Pobierz dane")
        self.fetch_button.clicked.connect(self.fetch_data)
        self.config_layout.addWidget(self.fetch_button)

        # Obszar wykresu
        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.layout.addWidget(self.chart_view)

        # Wyniki Fibonacciego
        self.fib_levels_label = QLabel("Poziomy Fibonacciego:")
        self.fib_levels_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 10px;")
        self.layout.addWidget(self.fib_levels_label)

        self.fib_levels_info = QLabel()
        self.layout.addWidget(self.fib_levels_info)

    def fetch_data(self):
        # Pobierz dane z Binance
        symbol = self.symbol_select.currentText()
        timeframe = self.timeframe_select.currentText()

        try:
            data = get_binance_data(symbol, timeframe)
            fib_levels = calculate_fibonacci_levels(data)

            # Wyświetl poziomy Fibonacciego
            self.show_fibonacci_levels(fib_levels)

            # Renderuj wykres
            self.render_chart(data, fib_levels)

        except Exception as e:
            self.fib_levels_info.setText(f"Błąd pobierania danych: {str(e)}")

    def show_fibonacci_levels(self, fib_levels):
        levels_text = "\n".join([f"{key}: {value:.2f}" for key, value in fib_levels.items()])
        self.fib_levels_info.setText(levels_text)

    def render_chart(self, data, fib_levels):
        # Utwórz wykres
        chart = QChart()
        chart.setTitle("Wykres świecowy z poziomami Fibonacciego")

        # Dane świecowe
        candlestick_series = QCandlestickSeries()
        candlestick_series.setName("Candlestick")
        for i, row in data.iterrows():
            candlestick_set = QCandlestickSet(row['open'], row['high'], row['low'], row['close'], row['timestamp'].timestamp())
            candlestick_series.append(candlestick_set)
        chart.addSeries(candlestick_series)

        # Poziomy Fibonacciego
        for level_name, level_value in fib_levels.items():
            line_series = QLineSeries()
            line_series.setName(level_name)
            line_series.append(data['timestamp'].iloc[0].timestamp(), level_value)
            line_series.append(data['timestamp'].iloc[-1].timestamp(), level_value)
            chart.addSeries(line_series)

        # Oś czasu
        axis_x = chart.createDefaultAxes()[0]
        axis_x.setTitleText("Czas")
        chart.setAxisX(axis_x, candlestick_series)

        # Oś cenowa
        axis_y = chart.createDefaultAxes()[1]
        axis_y.setTitleText("Cena")
        chart.setAxisY(axis_y, candlestick_series)

        # Wyświetl wykres
        self.chart_view.setChart(chart)


# Uruchomienie aplikacji
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CryptoFibonacciBot()
    window.show()
    sys.exit(app.exec())
