import time
from datetime import datetime
from gnews import GNews

class NewsFetcher:
    def __init__(self, language='en', country='US', max_results=10):
        self.gnews = GNews(language=language, country=country, max_results=max_results)
        self.latest_news = []

    def get_hash(self, content: str):
        return str(hash(content))

    def fetch_latest_news(self):
        # Fetch latest news
        self.latest_news = self.gnews.get_top_news()

    def get_latest_news(self):
        # Return the latest news as a list
        return self.latest_news

    def print_latest_news(self):
        # Print the fetched news
        print(f"Latest news at {datetime.now()}:\n")
        for news in self.latest_news:
            print(f"Title: {news['title']}")
            print(f"Description: {news['description']}")
            print(f"Published Date: {news['published date']}")
            print(f"URL: {news['url']}\n")
        print("-" * 40)

def news_generator():
    while True:
        news_fetcher = NewsFetcher()
        news_fetcher.fetch_latest_news()
        latest_news = news_fetcher.get_latest_news()
        yield latest_news
        time.sleep(60)

if __name__ == "__main__":
    for news in news_generator():
        print(news)
