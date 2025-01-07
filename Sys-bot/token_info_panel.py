import tkinter as tk
import requests
from tkinter import messagebox
from datetime import datetime
import json
import os

# Funkcja do pobierania danych z API i aktualizacji widoku
def fetch_crypto_data(crypto_id):
    try:
        # Wysłanie zapytania do CoinGecko API
        response = requests.get(
            f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies=usd&include_24hr_vol=true",
            timeout=10  # Limit czasu na odpowiedź
        )

        # Sprawdzanie, czy odpowiedź jest poprawna
        if response.status_code != 200:
            raise ValueError(f"Błąd API: {response.status_code} {response.reason}")

        data = response.json()

        # Walidacja danych w odpowiedzi
        if crypto_id not in data or "usd" not in data[crypto_id] or "usd_24h_vol" not in data[crypto_id]:
            raise ValueError("Niekompletna odpowiedź z API")

        # Pobieranie danych
        price = data[crypto_id]["usd"]
        volume = data[crypto_id]["usd_24h_vol"]

        # Aktualizacja etykiet
        price_label.config(text=f"Aktualna cena {crypto_id.upper()}: ${price:.4f}")
        volume_label.config(text=f"Wolumen 24h: ${volume:,.2f}")
        update_date_label()

        # Zapis danych do pliku
        save_data_to_file(crypto_id, price, volume, file_format_var.get())

    except requests.exceptions.Timeout:
        messagebox.showerror("Błąd", "Przekroczono czas oczekiwania na odpowiedź z API.")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Błąd", f"Problem z połączeniem: {str(e)}")
    except ValueError as e:
        messagebox.showerror("Błąd", f"Błąd w danych: {str(e)}")
    except Exception as e:
        messagebox.showerror("Błąd", f"Nieoczekiwany błąd: {str(e)}")

# Funkcja do aktualizacji daty i godziny
def update_date_label():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_label.config(text=f"Ostatnia aktualizacja: {current_time}")

# Funkcja do odświeżania danych dla wybranej kryptowaluty
def refresh_data():
    crypto_id = crypto_var.get()
    fetch_crypto_data(crypto_id)

# Funkcja do zapisywania danych do pliku
def save_data_to_file(crypto_id, price, volume, file_format):
    data = {
        "crypto_id": crypto_id,
        "price": price,
        "volume": volume,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    os.makedirs("data", exist_ok=True)
    if file_format == "json":
        with open(f"data/{crypto_id}_data.json", "w") as file:
            json.dump(data, file)
        print(f"Data saved to data/{crypto_id}_data.json")
    elif file_format == "txt":
        with open(f"data/{crypto_id}_data.txt", "w") as file:
            file.write(str(data))
        print(f"Data saved to data/{crypto_id}_data.txt")

# Tworzenie głównego okna
root = tk.Tk()
root.title("Informacje o kryptowalutach")
root.geometry("450x350")
root.configure(bg="black")

# Nagłówek
header_label = tk.Label(
    root,
    text="Mini Panel - Kryptowaluty",
    font=("Arial", 18, "bold"),
    bg="black",
    fg="white"
)
header_label.pack(pady=10)

# Wybór kryptowaluty
crypto_var = tk.StringVar(value="ripple")
crypto_menu = tk.OptionMenu(root, crypto_var, "ripple", "bitcoin", "ethereum", "litecoin")
crypto_menu.config(font=("Arial", 12), bg="#555", fg="white", relief="raised", bd=3)
crypto_menu.pack(pady=5)

# Wybór formatu pliku
file_format_var = tk.StringVar(value="json")
file_format_menu = tk.OptionMenu(root, file_format_var, "json", "txt")
file_format_menu.config(font=("Arial", 12), bg="#555", fg="white", relief="raised", bd=3)
file_format_menu.pack(pady=5)

# Etykieta do wyświetlania ceny
price_label = tk.Label(
    root,
    text="Aktualna cena: Ładowanie...",
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
    command=refresh_data,
    bg="#555",
    fg="white",
    relief="raised",
    bd=3
)
refresh_button.pack(pady=10)

# Pobierz dane przy starcie programu
fetch_crypto_data(crypto_var.get())

# Uruchomienie aplikacji
root.mainloop()


