import requests
import json
import logging
import os
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to fetch news from Bloomberg API
def fetch_bloomberg_news(api_key, query="Earth"):
    url = f"https://api.bloomberg.com/news/v1/search?q={query}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        news_data = response.json()
        return news_data
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch news: {e}")
        return None

# Function to display news
def display_news(news_data):
    if not news_data or "articles" not in news_data:
        logging.error("No news data available")
        return

    articles = news_data["articles"]
    for article in articles:
        title = article.get("title", "No title")
        description = article.get("description", "No description")
        url = article.get("url", "No URL")
        print(f"Title: {title}\nDescription: {description}\nURL: {url}\n")

# Function to save news to a file
def save_news_to_file(news_data, query):
    if not news_data or "articles" not in news_data:
        logging.error("No news data available to save")
        return

    os.makedirs("news_data", exist_ok=True)
    file_path = f"news_data/{query}_news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(file_path, 'w') as file:
        json.dump(news_data, file)
    logging.info(f"News data saved to {file_path}")

# Main function
def main():
    api_key = "your_bloomberg_api_key"  # Replace with your Bloomberg API key
    query = "Earth"
    news_data = fetch_bloomberg_news(api_key, query)
    display_news(news_data)
    save_news_to_file(news_data, query)

if __name__ == "__main__":
    main()
