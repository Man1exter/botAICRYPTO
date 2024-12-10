import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
    QWidget, QLabel, QPushButton, QComboBox, QTableWidget,
    QTableWidgetItem, QGraphicsView
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt


class CryptoBotUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Crypto Trading Bot")
        self.setGeometry(100, 100, 1200, 800)

        # Central Widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Main Layout
        main_layout = QVBoxLayout()
        self.central_widget.setLayout(main_layout)

        # Header
        header = QLabel("Crypto Trading Bot: Fibonacci Strategy")
        header.setFont(QFont("Arial", 20, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("color: #ffffff; background-color: #2a2e38; padding: 10px; border-radius: 10px;")
        main_layout.addWidget(header)

        # Controls Layout
        controls_layout = QHBoxLayout()

        # Pair Selection
        pair_label = QLabel("Trading Pair:")
        pair_label.setStyleSheet("color: #ffffff;")
        controls_layout.addWidget(pair_label)

        self.pair_combo = QComboBox()
        self.pair_combo.setStyleSheet("""
            QComboBox {
                background-color: #3b3f4a; 
                color: #ffffff; 
                padding: 5px; 
                border: 1px solid #5c5f69; 
                border-radius: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: #3b3f4a; 
                color: #ffffff;
            }
        """)
        self.pair_combo.addItems(["BTC/USDT", "ETH/USDT", "BNB/USDT"])
        controls_layout.addWidget(self.pair_combo)

        # Timeframe Selection
        timeframe_label = QLabel("Timeframe:")
        timeframe_label.setStyleSheet("color: #ffffff;")
        controls_layout.addWidget(timeframe_label)

        self.timeframe_combo = QComboBox()
        self.timeframe_combo.setStyleSheet("""
            QComboBox {
                background-color: #3b3f4a; 
                color: #ffffff; 
                padding: 5px; 
                border: 1px solid #5c5f69; 
                border-radius: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: #3b3f4a; 
                color: #ffffff;
            }
        """)
        self.timeframe_combo.addItems(["1m", "5m", "15m", "1h", "4h", "1d"])
        controls_layout.addWidget(self.timeframe_combo)

        # Update Button
        update_button = QPushButton("Update Chart")
        update_button.setStyleSheet("""
            QPushButton {
                background-color: #4caf50; 
                color: #ffffff; 
                padding: 10px; 
                border: none; 
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        update_button.clicked.connect(self.update_chart)
        controls_layout.addWidget(update_button)

        main_layout.addLayout(controls_layout)

        # Chart Area
        chart_label = QLabel("Trading Chart (Fibonacci Levels Applied)")
        chart_label.setFont(QFont("Arial", 14, QFont.Bold))
        chart_label.setStyleSheet("color: #ffffff;")
        main_layout.addWidget(chart_label)

        self.chart_view = QGraphicsView()
        self.chart_view.setStyleSheet("background-color: #2a2e38; border-radius: 10px;")
        main_layout.addWidget(self.chart_view)

        # Trade Suggestions
        suggestions_label = QLabel("Trade Suggestions")
        suggestions_label.setFont(QFont("Arial", 14, QFont.Bold))
        suggestions_label.setStyleSheet("color: #ffffff;")
        main_layout.addWidget(suggestions_label)

        self.trade_table = QTableWidget(0, 3)
        self.trade_table.setHorizontalHeaderLabels(["Action", "Entry Price", "Target Price"])
        self.trade_table.setStyleSheet("""
            QTableWidget {
                background-color: #3b3f4a; 
                color: #ffffff; 
                border: 1px solid #5c5f69; 
                border-radius: 5px;
            }
            QHeaderView::section {
                background-color: #2a2e38; 
                color: #ffffff; 
                padding: 5px;
            }
        """)
        main_layout.addWidget(self.trade_table)

        # Start Bot Button
        start_bot_button = QPushButton("Start Trading Bot")
        start_bot_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336; 
                color: #ffffff; 
                padding: 15px; 
                border: none; 
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        start_bot_button.clicked.connect(self.start_bot)
        main_layout.addWidget(start_bot_button)

    def update_chart(self):
        # Simulated placeholder for chart updates
        print("Chart updated with selected pair and timeframe.")

    def start_bot(self):
        # Simulated placeholder for bot starting logic
        print("Bot started with given trading strategy.")


# Run Application
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Dark Theme for the App
    app.setStyleSheet("""
        QWidget {
            background-color: #1f232a;
            font-family: Arial;
        }
    """)

    window = CryptoBotUI()
    window.show()
    sys.exit(app.exec())

