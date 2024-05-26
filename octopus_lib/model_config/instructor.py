from typing import List
from pydantic import BaseModel, Field

class GroqNews(BaseModel):
    rephrased_title: str = Field(description=f"""
                                    You are provided with a news title and content. Your task is to rephrase the title.
                                    Ensure the rephrased title is concise, catchy, and highly informative.
                                    Avoid unnecessary words and focus on capturing the essence of the news.
                                    You MUST not provide the source.
                                    """)
    news_keypoints: List[str] = Field(description=f"""
                                    You are provided with a news title and content and your task is to generate a list of three keypoints.
                                    
                                      You MUST write very short keypoints. Each keypoint MUST be 13 words maximum.
                                      You MUST generate very informative and meaningfull keypoints.
                                      You MUST focus on the main interesting points of the article.
                                      You MUST use complete words, not abbreviations.
                                    """)
    news_related_question: List[str] = Field(description=f"""
                                            You are provided with a news title and content and your task is to generate a list of three questions.
                                        
                                            You MUST write very short questions. Each question MUST be 10 words maximum.
                                            You MUST write questions that are naturally related to the news article when reading it.
                                            You MUST generate very informative and meaningfull questions.
                                            You MUST focus on the main interesting points of the article.
                                            You MUST only generate questions that are not predictive about an events.
                                            """)
    


class ResponseQuestionFormat(BaseModel):
    rephrased_title: str = Field(description=f"""
                                    You are provided with a question, articles chunks which contain the informations to respond to the question.
                                    Your task is to give the question again.
                                    Rephrased ONLY if the question is not clear.
                                    """)
    news_keypoints: List[str] = Field(description=f"""
                                      You are provided with a question, articles chunks which contain the informations to respond to the question and your task is to generate a list of three keypoints.
                                    
                                      You MUST write very short keypoints.
                                      You MUST generate very informative and meaningfull keypoints.
                                      You MUST focus on the main interesting points of the article.
                                    """)
    news_related_question: List[str] = Field(description=f"""
                                            You are provided with a question, articles chunks which contain the informations to respond to the question and your task is to generate a list of two questions on the content of response.
                                        
                                            You MUST write very short questions.
                                            You MUST write questions that are naturally related to the news article when reading it.
                                            You MUST generate very informative and meaningfull questions.
                                            You MUST focus on the main interesting points of the article.
                                            """)
