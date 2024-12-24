# Trading Bot Dashboard

## Overview

Trading Bot Dashboard is an interactive web-based application built using Streamlit to monitor and manage cryptocurrency trading bots. The dashboard provides real-time analytics, risk metrics, historical price data, AI forecasts, and key performance indicators to help traders make informed decisions.

## Directory Structure

```
botAICRYPTO/
│
├── MainControl.py
├── config.json
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

### README.md

This file provides an overview of the Trading Bot Dashboard, its directory structure, and descriptions of the main files.

## Usage

1. Ensure you have Python and the required libraries installed.
2. Update the `config.json` file with your desired settings.
3. Run the `MainControl.py` script to start downloading charts and scheduling future downloads.

```sh
python MainControl.py
```

## Requirements

- Python 3.x
- `requests` library
- `schedule` library
- `logging` library
- `json` library
- `os` library

## License

This project is licensed under the MIT License.
