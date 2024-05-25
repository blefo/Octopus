import time
from datetime import datetime
from gnews import GNews
from typing import List

from .models import News

class NewsFetcher:
    
    def __init__(self, database, language='en', country='US', max_results=10):
        self.gnews = GNews(language=language, country=country, max_results=max_results)
        self.latest_news = []
        self.database = database

    def get_hash(self, content: str):
        return str(hash(content))

    def fetch_latest_news(self):
        # Fetch latest news
        self.latest_news = self.gnews.get_top_news()

    def get_latest_news(self):
        # Return the latest news as a list
        return self.latest_news

    def only_not_in_database(self, database, latest_news: List):
        not_in_database: List = []
        for news in latest_news:
            news_hashed: str = self.get_hash(news['title'])
            if not News.object.filters(hash = news_hashed).exists():
                not_in_database.append(news)
        return not_in_database

def news_generator():
    while True:
        news_fetcher = NewsFetcher()
        news_fetcher.fetch_latest_news()
        latest_news = news_fetcher.get_latest_news()
        for new in 


        yield latest_news
        time.sleep(60)

if __name__ == "__main__":
    for news in news_generator():
        print(news)
