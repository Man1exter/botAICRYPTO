import sys
import pyqtgraph as pg
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
    QWidget, QLabel, QPushButton, QComboBox
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, QTimer
import ccxt


class HoverButton(QPushButton):
    """Custom QPushButton with hover effect."""
    def __init__(self, text):
        super().__init__(text)
        self.default_style = """
            QPushButton {
                background-color: #4caf50; 
                color: #ffffff; 
                padding: 10px; 
                border: none; 
                border-radius: 5px;
            }
        """
        self.hover_style = """
            QPushButton {
                background-color: #45a049; 
                color: #ffffff; 
                padding: 10px; 
                border: none; 
                border-radius: 5px;
            }
        """
        self.setStyleSheet(self.default_style)

    def enterEvent(self, event):
        self.setStyleSheet(self.hover_style)

    def leaveEvent(self, event):
        self.setStyleSheet(self.default_style)


class CryptoBotUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Crypto Trading Bot with AI Suggestions")
        self.setGeometry(100, 100, 1400, 900)

        # Central Widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Main Layout
        main_layout = QVBoxLayout()
        self.central_widget.setLayout(main_layout)

        # Header
        header = QLabel("Real-Time Crypto Trading Bot with Fibonacci Indicators")
        header.setFont(QFont("Arial", 20, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("color: #ffffff; background-color: #333; padding: 10px; border-radius: 10px;")
        main_layout.addWidget(header)

        # Controls Layout
        controls_layout = QHBoxLayout()

        # Dropdown for Pair Selection
        pair_label = QLabel("Trading Pair:")
        pair_label.setStyleSheet("color: white;")
        controls_layout.addWidget(pair_label)

        self.pair_combo = QComboBox()
        self.pair_combo.setStyleSheet("""
            QComboBox {
                background-color: #555; 
                color: #ffffff; 
                padding: 5px; 
                border-radius: 4px;
            }
            QComboBox QAbstractItemView {
                background-color: #777;
                color: #fff;
            }
        """)
        self.pair_combo.addItems(["BTC/USDT", "ETH/USDT", "BNB/USDT"])
        controls_layout.addWidget(self.pair_combo)

        # Dropdown for Timeframe Selection
        timeframe_label = QLabel("Timeframe:")
        timeframe_label.setStyleSheet("color: white;")
        controls_layout.addWidget(timeframe_label)

        self.timeframe_combo = QComboBox()
        self.timeframe_combo.setStyleSheet("""
            QComboBox {
                background-color: #555; 
                color: #ffffff; 
                padding: 5px; 
                border-radius: 4px;
            }
            QComboBox QAbstractItemView {
                background-color: #777;
                color: #fff;
            }
        """)
        self.timeframe_combo.addItems(["1m", "5m", "15m", "30m", "1h", "4h", "1d"])
        self.timeframe_combo.currentIndexChanged.connect(self.refresh_chart)
        controls_layout.addWidget(self.timeframe_combo)

        # Button to refresh chart data
        self.refresh_button = HoverButton("Refresh Data")
        self.refresh_button.clicked.connect(self.refresh_chart)
        controls_layout.addWidget(self.refresh_button)

        main_layout.addLayout(controls_layout)

        # Graph Area
        self.graph_widget = pg.PlotWidget()
        self.graph_widget.setBackground('w')  # Set a clean background
        main_layout.addWidget(self.graph_widget)

        # Placeholder for real-time data and exchange connection
        self.exchange = ccxt.binance({})  # Connect to Binance
        self.current_pair = "BTC/USDT"
        self.current_timeframe = "1m"
        self.candlestick_data = []
        self.timer = QTimer()
        self.timer.timeout.connect(self.fetch_market_data)
        self.timer.start(3000)  # Fetch data every 3 seconds

    def fetch_market_data(self):
        """Fetch real-time market data from Binance."""
        try:
            # Fetch recent historical data
            ohlcv = self.exchange.fetch_ohlcv(
                self.current_pair, timeframe=self.current_timeframe, limit=100
            )
            self.candlestick_data = ohlcv
            self.update_graph()
        except Exception as e:
            print(f"Error fetching data: {e}")

    def update_graph(self):
        """Update candlestick graph with fetched data."""
        self.graph_widget.clear()

        # Prepare data for candlestick rendering
        if len(self.candlestick_data) > 0:
            opens = [candle[1] for candle in self.candlestick_data]
            closes = [candle[4] for candle in self.candlestick_data]
            highs = [candle[2] for candle in self.candlestick_data]
            lows = [candle[3] for candle in self.candlestick_data]

            # Use BarGraphItem for candlesticks
            x_positions = range(len(opens))
            heights = [close - open for open, close in zip(opens, closes)]
            widths = [0.6] * len(opens)  # Uniform candlestick width

            bg_item = pg.BarGraphItem(
                x=x_positions, 
                height=heights, 
                width=widths,
                brush=[pg.mkBrush('g') if close >= open else pg.mkBrush('r') for open, close in zip(opens, closes)]
            )

            self.graph_widget.addItem(bg_item)

        # Draw Fibonacci retracements
        self.draw_fibonacci_levels()

    def draw_fibonacci_levels(self):
        """Overlay Fibonacci retracements dynamically."""
        if not self.candlestick_data:
            return

        prices = [candle[4] for candle in self.candlestick_data]
        max_price, min_price = max(prices), min(prices)

        # Calculate retracement levels
        fib_levels = [
            max_price - 0.236 * (max_price - min_price),
            max_price - 0.382 * (max_price - min_price),
            max_price - 0.5 * (max_price - min_price),
            max_price - 0.618 * (max_price - min_price)
        ]

        for level in fib_levels:
            self.graph_widget.plot(
                [0, len(prices) - 1], [level, level], pen=pg.mkPen('b', width=1, style=pg.mkPen.DashLine)
            )

    def refresh_chart(self):
        """Refresh chart data when filters change."""
        self.current_pair = self.pair_combo.currentText()
        self.current_timeframe = self.timeframe_combo.currentText()
        print(f"Fetching data for pair {self.current_pair} with timeframe {self.current_timeframe}")


# Run the App
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CryptoBotUI()
    window.show()
    sys.exit(app.exec())




