import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QTableWidget, QTableWidgetItem
)
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QFont
import requests


class Top10CryptoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Top 10 Kryptowalut - Longi i Shorty")
        self.setGeometry(100, 100, 800, 500)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Nagłówek
        self.header_label = QLabel("Top 10 Kryptowalut - Longi i Shorty", self)
        self.header_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.header_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.header_label)

        # Tabela do wyświetlania danych
        self.crypto_table = QTableWidget(self)
        self.crypto_table.setColumnCount(4)
        self.crypto_table.setHorizontalHeaderLabels(
            ["Kryptowaluta", "Wolumen Longów", "Wolumen Shortów", "Zakres Kwot"]
        )
        self.crypto_table.horizontalHeader().setStretchLastSection(True)
        self.crypto_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.layout.addWidget(self.crypto_table)

        # Przycisk odświeżania
        self.refresh_button = QPushButton("Odśwież dane", self)
        self.refresh_button.clicked.connect(self.fetch_crypto_data)
        self.layout.addWidget(self.refresh_button)

        # Timer do automatycznego odświeżania co 60 sekund
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.fetch_crypto_data)
        self.timer.start(60000)  # 60 sekund

        # Pobranie danych przy starcie programu
        self.fetch_crypto_data()

    def fetch_crypto_data(self):
        try:
            # Przykładowe dane (symulacja odpowiedzi z API)
            # W rzeczywistym przypadku tutaj należy podłączyć API dostarczające dane o longach i shortach.
            simulated_data = [
                {"name": "Bitcoin", "longs": 50000000, "shorts": 20000000, "range": "$20,000 - $22,000"},
                {"name": "Ethereum", "longs": 30000000, "shorts": 15000000, "range": "$1,500 - $1,700"},
                {"name": "BNB", "longs": 15000000, "shorts": 8000000, "range": "$300 - $320"},
                {"name": "XRP", "longs": 12000000, "shorts": 5000000, "range": "$0.40 - $0.50"},
                {"name": "Cardano", "longs": 10000000, "shorts": 4000000, "range": "$0.30 - $0.35"},
                {"name": "Solana", "longs": 8000000, "shorts": 3000000, "range": "$20 - $22"},
                {"name": "Polkadot", "longs": 7000000, "shorts": 2500000, "range": "$5 - $6"},
                {"name": "Dogecoin", "longs": 6000000, "shorts": 2000000, "range": "$0.07 - $0.08"},
                {"name": "Shiba Inu", "longs": 5000000, "shorts": 1000000, "range": "$0.000007 - $0.000008"},
                {"name": "Litecoin", "longs": 4000000, "shorts": 2000000, "range": "$90 - $100"},
            ]

            # Aktualizacja tabeli
            self.crypto_table.setRowCount(len(simulated_data))
            for row, crypto in enumerate(simulated_data):
                self.crypto_table.setItem(row, 0, QTableWidgetItem(crypto["name"]))
                self.crypto_table.setItem(row, 1, QTableWidgetItem(f"${crypto['longs']:,}"))
                self.crypto_table.setItem(row, 2, QTableWidgetItem(f"${crypto['shorts']:,}"))
                self.crypto_table.setItem(row, 3, QTableWidgetItem(crypto["range"]))

        except Exception as e:
            self.crypto_table.setRowCount(0)
            error_label = QLabel(f"Błąd podczas pobierania danych: {str(e)}", self)
            error_label.setStyleSheet("color: red; font-size: 14px;")
            self.layout.addWidget(error_label)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("background-color: white; font-size: 14px;")
    window = Top10CryptoWindow()
    window.show()
    sys.exit(app.exec())
