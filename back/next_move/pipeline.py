import os
import sys
from os import getenv
from dotenv import load_dotenv
from requests.exceptions import HTTPError, RequestException
from pydantic import BaseModel, Field
from typing import List

# from langchain_core.prompts import ChatPromptTemplate
# from langchain_groq import ChatGroq
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.runnables import RunnablePassthrough
# from langchain_text_splitters import RecursiveCharacterTextSplitter

import instructor
from groq import Groq
from pydantic import BaseModel
from gnews import GNews

import newspaper

from embedding import *

from pgvector.psycopg import register_vector
import psycopg

# current_dir = os.path.dirname(os.path.abspath(__file__))
# parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
# sys.path.insert(0, parent_dir)

# from news_feed import news_fetcher
# from news_fetcher import *

load_dotenv()
KEY_GROQ = getenv('GROQ_API_KEY')
NEON_CONN=getenv('NEON_POSTGRES_CONNECTION_STRING')

client = Groq(api_key=KEY_GROQ)
client = instructor.from_groq(client, mode=instructor.Mode.TOOLS)

class UserExtract(BaseModel):
    keywords: list[str]

instruction = "Please give me a list of five keywords related to the following question : "
question = "Which team just won the rugby European Champions cup ?"
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
embedded_list = []
for article in articles_json_list:
    try:
        data = gnews.get_full_article(article['url'])
        embeddings = get_embeddings_by_chunks(data.text, 500)
        embedded_list.append((embeddings, data.text))
    except Exception as e:
        print(f"An error as occured {e}")
        
if embedded_list:
    first_embedding = embedded_list[0][0][0]
    dimensions = len(first_embedding)
    print(f"Embedding dimensions determined to be: {dimensions}")

    conn = psycopg.connect(dbname='Octopusdb', autocommit=True)
    register_vector(conn)

    # Create table
    with conn.cursor() as cur:
        cur.execute('CREATE EXTENSION IF NOT EXISTS vector')
        cur.execute('DROP TABLE IF EXISTS items')
        cur.execute('CREATE TABLE items (id bigserial PRIMARY KEY, embedding vector(1024), text_content TEXT)')

    # Insert embeddings into the database
    with conn.cursor() as cur:
        for embeddings, text_content in embedded_list:
            for embedding in embeddings:
                cur.execute('INSERT INTO items (embedding, text_content) VALUES (%s::vector, %s)', (embedding, text_content))

    print("Embeddings successfully inserted into the database.")
else:
    print("No embeddings to insert.")
    

def retrieve_documents(query_embedding, top_k=5):
    with conn.cursor() as cur:
        query_embedding_str = ','.join(map(str, query_embedding))
        query_embedding_vector = f'[{query_embedding_str}]'
        query = f"SELECT id, text_content, embedding <-> %s::vector AS distance FROM items ORDER BY distance LIMIT {top_k}"
        cur.execute(query, (query_embedding_vector,))
        results = cur.fetchall()
    return results

from mistralai.client import MistralClient

load_dotenv()
KEY_MISTRAL = getenv('MISTRAL_API_KEY')
mistral_client = MistralClient(api_key=KEY_MISTRAL)
groq_client = Groq(api_key=KEY_GROQ)

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

def generate_answer(documents, groq_client):
    context = " ".join([doc[1] for doc in documents])
    instruction = "Please from this context provide me a quick article."
    data = instruction + context

    groq_client = instructor.from_groq(groq_client, mode=instructor.Mode.TOOLS)
    response = groq_client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {
                "role": "user",
                "content": data,
            }
        ],
        response_model=GroqNews,
    )
    return response
    

query_embedding = get_query_embedding(question)
results = retrieve_documents(query_embedding)
documents = [(doc_id, text_content) for doc_id, text_content, distance in results]

answer = generate_answer(documents, groq_client)
print(f"Answer: {answer}")

