import requests
import json
import logging
import os
from datetime import datetime
from security import load_secure_config

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration
config = load_secure_config('secure_config.enc')

# TradingView API URL
TRADINGVIEW_API_URL = "https://api.tradingview.com/chart"

# Function to fetch chart data from TradingView API
def fetch_chart_data(symbol, timeframe='1D'):
    url = f"{TRADINGVIEW_API_URL}/{symbol}/{timeframe}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching chart data for {symbol}: {e}")
        return None

# Function to save chart data to a file
def save_chart_data(symbol, data, output_dir='.'):
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"{symbol}_chart.json")
    with open(file_path, 'w') as file:
        json.dump(data, file)
    logging.info(f"Chart data for {symbol} saved to {file_path}")

# Function to calculate Fibonacci retracement levels
def calculate_fibonacci_levels(data):
    high = max(data, key=lambda x: x['high'])['high']
    low = min(data, key=lambda x: x['low'])['low']
    diff = high - low
    levels = {
        '0.0%': high,
        '23.6%': high - 0.236 * diff,
        '38.2%': high - 0.382 * diff,
        '50.0%': high - 0.5 * diff,
        '61.8%': high - 0.618 * diff,
        '100.0%': low
    }
    return levels

# Function to create a TradingView chart with Fibonacci levels
def create_tradingview_chart(symbol, timeframe='1D', output_dir='.'):
    data = fetch_chart_data(symbol, timeframe)
    if data:
        save_chart_data(symbol, data, output_dir)
        levels = calculate_fibonacci_levels(data)
        logging.info(f"Fibonacci levels for {symbol}: {levels}")
        display_fibonacci_levels(symbol, levels, output_dir)
        logging.info(f"TradingView chart for {symbol} created successfully")
    else:
        logging.error(f"Failed to create TradingView chart for {symbol}")

# Function to display Fibonacci levels on the chart
def display_fibonacci_levels(symbol, levels, output_dir='.'):
    chart_path = os.path.join(output_dir, f"{symbol}_chart.json")
    with open(chart_path, 'r') as file:
        chart_data = json.load(file)
    
    # Add Fibonacci levels to the chart data
    chart_data['fibonacci_levels'] = levels
    
    # Save the updated chart data
    with open(chart_path, 'w') as file:
        json.dump(chart_data, file)
    logging.info(f"Fibonacci levels for {symbol} added to the chart")

# Function to plot the chart with Fibonacci levels
def plot_chart_with_fibonacci(symbol, output_dir='.'):
    import matplotlib.pyplot as plt

    chart_path = os.path.join(output_dir, f"{symbol}_chart.json")
    with open(chart_path, 'r') as file:
        chart_data = json.load(file)

    prices = [item['close'] for item in chart_data]
    dates = [datetime.fromtimestamp(item['time'] / 1000) for item in chart_data]

    plt.figure(figsize=(12, 6))
    plt.plot(dates, prices, label='Price')

    for level, value in chart_data['fibonacci_levels'].items():
        plt.axhline(y=value, color='r', linestyle='--', label=f'Fibonacci {level}')

    plt.title(f'{symbol} Price Chart with Fibonacci Levels')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.show()

# Example usage
if __name__ == "__main__":
    symbols = config.get('top_10_tokens', ['BTC', 'ETH', 'BNB', 'USDT', 'ADA', 'SOL', 'XRP', 'DOT', 'DOGE', 'USDC'])
    timeframes = config.get('timeframes', ['1D'] * len(symbols))
    output_dirs = config.get('output_dirs', ['.'] * len(symbols))

    for symbol, timeframe, output_dir in zip(symbols, timeframes, output_dirs):
        create_tradingview_chart(symbol, timeframe, output_dir)
        plot_chart_with_fibonacci(symbol, output_dir)
