import time
from gnews import GNews
from typing import List
import instructor
from news_feed.llm_manager.inference_structure import GroqNews
from groq import Groq

from .models import News

client = Groq(
    api_key= "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" #os.environ.get("GROQ_API_KEY"),
)
client = instructor.from_groq(client, mode=instructor.Mode.TOOLS)

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

    def only_not_in_database(self):
        not_in_database: List = []
        for news in self.latest_news:
            news_hashed: str = self.get_hash(news['title'])
            if not News.objects.filter(hash = news_hashed).exists():
                not_in_database.append(news)
        return not_in_database
    
    def get_inferences_with_groq(self, news_list: List):
        full_list = []

        for news in news_list:
            # Get News content
            news_full_content = self.gnews.get_full_article(news['url']).text
            if news_full_content:
                # The news is correctly scraped
                # Get Inference
                prompt: str = f"""
                    News Title: {news['title']}
                    News Content: {news_full_content}
                """

            else:
                # Could not scrap the news
                # Get Inference
                prompt: str = f"""
                    News Title: {news['title']}
                    News Content: {news['description']}
                """

            groq_news: GroqNews = client.chat.completions.create(
                model="mixtral-8x7b-32768",
                response_model=GroqNews,
                messages=[
                    {"role": "user", "content": prompt},
                ],
            )

            News.objects.create(
                hash=self.get_hash(news['title']),
                base_title=news['title'],
                base_content=news_full_content,
                groq_title=groq_news.rephrased_title,
                groq_key_point_1=groq_news.news_keypoints[0],
                groq_key_point_2=groq_news.news_keypoints[1],
                groq_question_1=groq_news.news_related_question[0],
                groq_question_2=groq_news.news_related_question[1],
            )
            print(groq_news)
                


def news_generator():
    news_fetcher = NewsFetcher()
    news_fetcher.fetch_latest_news()
    latest_news = news_fetcher.get_latest_news()
    latest_news_not_in_database = news_fetcher.only_not_in_database()
    latest_with_inferences = news_fetcher.get_inferences_with_groq(latest_news_not_in_database)

        # Get Grok inference



