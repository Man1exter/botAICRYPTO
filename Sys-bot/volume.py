import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QMessageBox
)
from PySide6.QtCore import QTimer, Qt
import requests
from datetime import datetime


class CryptoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kryptowaluty - Top 5 Wolumenów 24h")
        self.setGeometry(100, 100, 600, 400)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)
        self.central_widget.setLayout(self.layout)
        
        # Nagłówek
        self.header_label = QLabel("Top 5 Kryptowalut - Wolumen 24h", self)
        self.header_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #003366;")
        self.header_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.header_label)
        
        # Etykiety dla kryptowalut
        self.crypto_labels = []
        for _ in range(5):
            label = QLabel("Ładowanie...", self)
            label.setStyleSheet("font-size: 14px; color: #333333;")
            self.crypto_labels.append(label)
            self.layout.addWidget(label)
        
        # Etykieta czasu ostatniej aktualizacji
        self.update_time_label = QLabel("Ostatnia aktualizacja: --", self)
        self.update_time_label.setStyleSheet("font-size: 12px; color: #666666;")
        self.update_time_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.update_time_label)
        
        # Przycisk odświeżania
        self.refresh_button = QPushButton("Odśwież dane", self)
        self.refresh_button.setStyleSheet(
            "font-size: 14px; background-color: #0044cc; color: white; padding: 8px; border-radius: 5px;"
        )
        self.refresh_button.clicked.connect(self.fetch_crypto_data)
        self.layout.addWidget(self.refresh_button)
        
        # Automatyczne odświeżanie co 60 sekund
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.fetch_crypto_data)
        self.timer.start(60000)  # 60 sekund
        
        # Inicjalne pobranie danych
        self.fetch_crypto_data()
    
    def fetch_crypto_data(self):
        try:
            # Wysłanie zapytania do CoinGecko API
            response = requests.get(
                "https://api.coingecko.com/api/v3/coins/markets",
                params={
                    "vs_currency": "usd",
                    "order": "market_cap_desc",
                    "per_page": 5,
                    "page": 1
                },
                timeout=10
            )
            
            if response.status_code != 200:
                raise ValueError(f"Błąd API: {response.status_code} {response.reason}")
            
            data = response.json()
            
            # Aktualizacja etykiet dla 5 kryptowalut
            for i, crypto in enumerate(data):
                name = crypto.get("name", "Nieznane")
                volume = crypto.get("total_volume", 0)
                self.crypto_labels[i].setText(f"{i + 1}. {name}: ${volume:,.2f}")
            
            # Aktualizacja czasu ostatniej aktualizacji
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.update_time_label.setText(f"Ostatnia aktualizacja: {current_time}")
        
        except requests.exceptions.Timeout:
            QMessageBox.critical(self, "Błąd", "Przekroczono czas oczekiwania na odpowiedź z API.")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Błąd", f"Problem z połączeniem: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nieoczekiwany błąd: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("background-color: #f5f5f5;")
    window = CryptoApp()
    window.show()
    sys.exit(app.exec())
