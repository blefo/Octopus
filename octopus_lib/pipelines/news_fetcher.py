import time
from gnews import GNews
from typing import List
import instructor
from octopus_lib.model_config.instructor import GroqNews
from groq import Groq
from dotenv import load_dotenv
import os
from pathlib import Path

from octopus_lib.model_config.prompt import news_feed_prompt


#from back.news_feed.models import News


load_dotenv()
relative_path = Path(__file__).resolve().parent.parent / "model_config/config.env"
load_dotenv(relative_path)

MODEL_INFERENCE = os.getenv('MODEL_INFERENCE')

client = Groq(
    api_key= os.getenv("GROQ_API_KEY"),
)
client = instructor.from_groq(client, mode=instructor.Mode.TOOLS)

class NewsFetcher:
    def __init__(self, news_db, language='fr', country='FR', max_results=30):
        self.gnews = GNews(language=language, country=country, max_results=max_results)
        self.latest_news = []
        self.news_db = news_db

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
            if not self.news_db.objects.filter(hash = news_hashed).exists():
                not_in_database.append(news)
        return not_in_database
    
    def get_inferences_with_groq(self, news_list: List):
        for news in news_list:
            # Get News content

            news_full_content = self.gnews.get_full_article(news['url'])
            if news_full_content:
                news_full_content_text = news_full_content.text
                image_cover = news_full_content.top_image

                if news_full_content:
                    # The news is correctly scraped
                    # Get Inference
                    prompt: str = news_feed_prompt(news['title'], news_full_content_text)

                else:
                    # Could not scrap the news
                    # Get Inference
                    prompt: str = news_feed_prompt(news['title'], news['description'])

                groq_news: GroqNews = client.chat.completions.create(
                    model=MODEL_INFERENCE,
                    response_model=GroqNews,
                    messages=[
                        {"role": "user", "content": prompt},
                    ],
                )


                self.news_db.objects.create(
                    hash=self.get_hash(news['title']),
                    base_title=news['title'],
                    base_content=news_full_content_text,
                    groq_title=groq_news.rephrased_title,
                    groq_key_point_1=groq_news.news_keypoints[0],
                    groq_key_point_2=groq_news.news_keypoints[1],
                    groq_key_point_3=groq_news.news_keypoints[2],
                    groq_question_1=groq_news.news_related_question[0],
                    groq_question_2=groq_news.news_related_question[1],
                    groq_question_3=groq_news.news_related_question[2],
                    image_cover=image_cover,
                    news_source=news["publisher"]["href"]
                )


                


def news_generator(news_db):
    news_fetcher = NewsFetcher(news_db)
    news_fetcher.fetch_latest_news()
    latest_news_not_in_database = news_fetcher.only_not_in_database()
    latest_with_inferences = news_fetcher.get_inferences_with_groq(latest_news_not_in_database)



