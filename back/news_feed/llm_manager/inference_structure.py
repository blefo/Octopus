from typing import List
from pydantic import BaseModel, Field

class GroqNews(BaseModel):
    rephrased_title: str = Field(description=f"""
                                    You are provided with a news title and content. Your task is to rephrase the title.
                                    Ensure the rephrased title is concise, catchy, and highly informative.
                                    Avoid unnecessary words and focus on capturing the essence of the news.
                                    """)
    news_keypoints: List[str] = Field(description=f"""
                                    You are provided with a news title and content. Your task is to generate three key points.
                                    Each key point must be concise, highly informative, and meaningful.
                                    Focus on the most critical and engaging aspects of the article.
                                    Ensure clarity and relevance in each key point.
                                    """)
    news_related_question: List[str] = Field(description=f"""
                                            You are provided with a news title and content. Your task is to generate three related questions.
                                            Each question must be concise, highly relevant, and directly related to the article.
                                            Focus on the most important and interesting aspects of the news.
                                            Ensure the questions provoke thought and invite further exploration.
                                            """)
