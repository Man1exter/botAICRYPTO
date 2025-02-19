# Trading Bot Dashboard

## Overview

Trading Bot Dashboard is an interactive web-based application built using Streamlit to monitor and manage cryptocurrency trading bots. The dashboard provides real-time analytics, risk metrics, historical price data, AI forecasts, and key performance indicators to help traders make informed decisions.

## Directory Structure

```
botAICRYPTO/
│
├── MainControl.py
├── config.json
├── token_info_panel.py
├── tempCodeRunnerFile.py
├── service.py
├── panel.py
├── longshort.py
├── futures_test.py
├── binance_his.py
├── bloomberg_terminal.py
├── security.py
├── ultra_secure.py
├── securize.sh
├── PowerOfPC.cs
└── README.md
```

## Files

### MainControl.py

This is the main control script for the Trading Bot Dashboard. It includes functions to:

- Load and validate configuration settings.
- Download charts for the top 10 cryptocurrency tokens using the TradingView API.
- Schedule downloads at regular intervals.
- Handle retries in case of download failures.
- Send notifications using different methods (log, email, SMS).
- Log the start and end of the download process.
- Analyze downloaded charts using an AI agent.
- Save analysis results to a file.
- Handle different logging levels and formats.
- Handle different time zones for scheduling downloads.

### config.json

This configuration file contains customizable settings for the Trading Bot Dashboard, including:

- `top_10_tokens`: List of the top 10 cryptocurrency tokens.
- `timeframes`: List of timeframes for each token.
- `file_formats`: List of file formats for each chart.
- `interval_minutes`: Interval in minutes for scheduling downloads.
- `retries`: Number of retries for download failures.
- `api_urls`: List of API URLs for each token.
- `output_dirs`: List of output directories for each chart.
- `notification_methods`: List of notification methods for each chart.
- `email_settings`: Email settings for notifications.
- `sms_settings`: SMS settings for notifications.
- `logging_level`: Logging level for the application.
- `logging_format`: Logging format for the application.
- `time_zone`: Time zone for scheduling downloads.

### token_info_panel.py

This script creates a simple GUI using Tkinter to display the current price and 24-hour volume of selected cryptocurrencies. It fetches data from the CoinGecko API, updates the display, and saves the data to a file in different formats (JSON, TXT).

### tempCodeRunnerFile.py

This file contains a single line to run a Streamlit script.

### service.py

This script defines a `CryptoBot` class that interacts with the Binance exchange using the `ccxt` library. It includes methods to fetch balance, fetch ticker data, create orders, and run a simple trading loop.

### panel.py

This script creates a Streamlit dashboard for AI trading. It fetches historical data from Binance, calculates technical indicators, builds an LSTM model for price prediction, and displays trading signals and backtest results.

### longshort.py

This script creates a PyQt application to display the top 10 cryptocurrencies with their long and short volumes. It includes a table to display the data and a button to refresh the data.

### futures_test.py

This script creates a PyQt application with a real-time candlestick chart and Fibonacci retracement levels. It fetches market data from Binance and updates the chart at regular intervals.

### binance_his.py

This script creates a Streamlit dashboard for real-time trading data and AI forecasts. It fetches data from Binance, displays a TradingView chart, and includes tabs for risk analysis and historical data.

### bloomberg_terminal.py

This script fetches news from the Bloomberg API, filters articles based on keywords, displays the news, saves it to a file, and sends notifications for new articles. It also schedules regular news fetches.

### security.py

This script provides functions for securely saving and loading sensitive data and configuration settings using encryption.

### ultra_secure.py

This script enhances security features by including multi-factor authentication (MFA) and secure environment checks.

### securize.sh

This bash script generates an encryption key, encrypts the configuration file, and removes the plain configuration file for security.

### PowerOfPC.cs

This C# script analyzes the computational power of the system, including CPU usage, available memory, total memory, disk usage, GPU usage, and system uptime.

### README.md

This file provides an overview of the Trading Bot Dashboard, its directory structure, and descriptions of the main files.

## Usage

1. Ensure you have Python and the required libraries installed.
2. Update the `config.json` file with your desired settings.
3. Run the `securize.sh` script to encrypt the configuration file.

```sh
bash securize.sh
```

4. Run the `MainControl.py` script to start downloading charts and scheduling future downloads.

```sh
python MainControl.py
```

## Ultra Secure Usage

1. Ensure you have Python and the required libraries installed.
2. Set the `SECURE_ENV` environment variable to `true`.

```sh
export SECURE_ENV=true
```

3. Run the `ultra_secure.py` script to perform multi-factor authentication and secure the configuration file.

```sh
python ultra_secure.py
```

## PowerOfPC Usage

1. Ensure you have .NET installed.
2. Compile the `PowerOfPC.cs` file.

```sh
csc PowerOfPC.cs
```

3. Run the compiled executable to analyze the computational power of the system.

```sh
./PowerOfPC.exe
```

## Requirements

- Python 3.x
- `requests` library
- `schedule` library
- `logging` library
- `json` library
- `os` library
- `tkinter` library
- `ccxt` library
- `streamlit` library
- `pandas` library
- `numpy` library
- `tensorflow` library
- `ta` library
- `PySide6` library
- `pyqtgraph` library
- `cryptography` library
- `pyotp` library
- .NET SDK

## License

This project is licensed under the MIT License.
