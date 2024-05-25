import os
import sys
from os import getenv
from dotenv import load_dotenv
from pgvector.psycopg import register_vector
import psycopg
from groq import Groq
from mistralai.client import MistralClient

load_dotenv()
KEY_MISTRAL = getenv('MISTRAL_API_KEY')

client = MistralClient(api_key=KEY_MISTRAL)

def get_embeddings_by_chunks(data, chunk_size):
    chunks = [data[x : x + chunk_size] for x in range(0, len(data), chunk_size)]
    embeddings_response = [
        client.embeddings(model="mistral-embed", input=c) for c in chunks
    ]
    print("DONE")
    return [d.embedding for e in embeddings_response for d in e.data]

def get_query_embedding(query):
    response = client.embeddings(model="mistral-embed", input=query)
    return response.data[0].embedding

