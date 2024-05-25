from typing import List
from pydantic import BaseModel, Field

class GroqNews(BaseModel):
    rephrased_title: str = Field(description=f"""
                                    You are provided with a news title and content and your task is to rephrase the title.
                                    You MUST make if very short.
                                    You MUST make it as much informative as possible.
                                    You MSUT make it a little catchy.
                                    """
                                )
    news_keypoints: List[str] = Field(description=f"""
                                    You are provided with a news title and content and your task is to generate a list of three keypoints.
                                    
                                      You MUST write very short keypoints.
                                      You MUST generate very informative and meaningfull keypoints.
                                      You MUST focus on the main interesting points of the article.
                                    """)
    news_related_question: List[str] = Field(description=f"""
                                            You are provided with a news title and content and your task is to generate a list of three questions.
                                        
                                            You MUST write very short questions.
                                            You MUST write questions that are naturally related to the news article when reading it.
                                            You MUST generate very informative and meaningfull questions.
                                            You MUST focus on the main interesting points of the article.
                                            """)