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

# Function to filter news articles based on keywords
def filter_news_by_keywords(news_data, keywords):
    if not news_data or "articles" not in news_data:
        logging.error("No news data available to filter")
        return []

    filtered_articles = []
    for article in news_data["articles"]:
        if any(keyword.lower() in article.get("title", "").lower() or keyword.lower() in article.get("description", "").lower() for keyword in keywords):
            filtered_articles.append(article)
    return filtered_articles

# Function to send notifications for new articles
def send_notification(message):
    # Placeholder for notification logic (e.g., email, SMS, etc.)
    logging.info(f"Notification: {message}")

# Main function
def main():
    api_key = "your_bloomberg_api_key"  # Replace with your Bloomberg API key
    query = "Earth"
    keywords = ["climate", "environment", "sustainability"]
    news_data = fetch_bloomberg_news(api_key, query)
    filtered_news = filter_news_by_keywords(news_data, keywords)
    if filtered_news:
        send_notification(f"Found {len(filtered_news)} new articles about {query}")
    display_news({"articles": filtered_news})
    save_news_to_file({"articles": filtered_news}, query)

if __name__ == "__main__":
    main()
