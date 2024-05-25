import os
import sys
from os import getenv
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter

import instructor
from groq import Groq
from pydantic import BaseModel
from gnews import GNews

import newspaper

# current_dir = os.path.dirname(os.path.abspath(__file__))
# parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
# sys.path.insert(0, parent_dir)

# from news_feed import news_fetcher
# from news_fetcher import *


load_dotenv()
KEY_GROQ = getenv('GROQ_API_KEY')

client = Groq(api_key=KEY_GROQ)
client = instructor.from_groq(client, mode=instructor.Mode.TOOLS)

class UserExtract(BaseModel):
    keywords: list[str]

instruction = "Please give me a list of five keywords related to the following question : "
question = "What is the situation of the war in Ukraine"
data = instruction + question

user: UserExtract = client.chat.completions.create(
    model="mixtral-8x7b-32768",
    messages=[
        {
            "role": "user",
            "content": data,
        }
    ],
    response_model=UserExtract,
)

list_of_keywords = user.model_dump()["keywords"]
# fetcher = NewsFetcher()
# articles = fetcher.fetch_news_from_keywords(list_of_keywords)
gnews = GNews(language='en', country='US', max_results=10)
articles_json_list = gnews.get_news(' '.join(list_of_keywords))
for article in articles_json_list:
    try:
        data = gnews.get_full_article(article['url'])
        print(data.title)

full_text = "\n\n".join(articles_content)

# Définir une fonction pour résumer le texte
def summarize_text(text, model, prompt_template):
    response = model.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {
                "role": "user",
                "content": prompt_template.format(text=text),
            }
        ],
        response_model=StrOutputParser,
    )
    return response.model_dump()["text"]

# Définir le modèle et le template de prompt pour résumer le texte
prompt_template = "Please summarize the following text:\n\n{text}\n\nSummary:"
summary = summarize_text(full_text, client, prompt_template)

# Afficher le résumé
print(summary)