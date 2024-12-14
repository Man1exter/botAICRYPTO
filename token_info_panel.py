import tkinter as tk
import requests
from tkinter import messagebox
from datetime import datetime

# Funkcja do pobierania danych z API i aktualizacji widoku
def fetch_xrp_data():
    try:
        # Wysłanie zapytania do CoinGecko API
        response = requests.get(
            "https://api.coingecko.com/api/v3/simple/price?ids=ripple&vs_currencies=usd&include_24hr_vol=true"
        )
        data = response.json()

        # Pobieranie danych
        price = data["ripple"]["usd"]
        volume = data["ripple"]["usd_24h_vol"]

        # Aktualizacja etykiet
        price_label.config(text=f"Aktualna cena XRP: ${price:.4f}")
        volume_label.config(text=f"Wolumen 24h: ${volume:,.2f}")
        update_date_label()

    except Exception as e:
        messagebox.showerror("Błąd", f"Nie udało się pobrać danych: {str(e)}")

# Funkcja do aktualizacji daty i godziny
def update_date_label():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_label.config(text=f"Ostatnia aktualizacja: {current_time}")

# Tworzenie głównego okna
root = tk.Tk()
root.title("XRP - Informacje o cenie i wolumenie")
root.geometry("450x250")
root.configure(bg="black")

# Nagłówek
header_label = tk.Label(
    root,
    text="Mini Panel - XRP",
    font=("Arial", 18, "bold"),
    bg="black",
    fg="white"
)
header_label.pack(pady=10)

# Etykieta do wyświetlania ceny
price_label = tk.Label(
    root,
    text="Aktualna cena XRP: Ładowanie...",
    font=("Arial", 12),
    bg="black",
    fg="white"
)
price_label.pack(pady=5)

# Etykieta do wyświetlania wolumenu
volume_label = tk.Label(
    root,
    text="Wolumen 24h: Ładowanie...",
    font=("Arial", 12),
    bg="black",
    fg="white"
)
volume_label.pack(pady=5)

# Etykieta do wyświetlania daty i godziny
date_label = tk.Label(
    root,
    text="Ostatnia aktualizacja: --",
    font=("Arial", 10),
    bg="black",
    fg="white"
)
date_label.pack(pady=5)

# Przycisk do odświeżania danych
refresh_button = tk.Button(
    root,
    text="Odśwież dane",
    font=("Arial", 12),
    command=fetch_xrp_data,
    bg="#555",
    fg="white",
    relief="raised",
    bd=3
)
refresh_button.pack(pady=10)

# Pobierz dane przy starcie programu
fetch_xrp_data()

# Uruchomienie aplikacji
root.mainloop()

