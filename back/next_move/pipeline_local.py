import os
import time
import asyncio
import aiohttp
import numpy as np
import faiss
from pydantic import BaseModel
from dotenv import load_dotenv
from gnews import GNews
from instructor import from_groq, Mode
from groq import Groq, AsyncGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter, HTMLHeaderTextSplitter
from langchain.schema import Document
from mistralai.client import MistralClient


# Load environment variables
load_dotenv()
KEY_GROQ = os.getenv('GROQ_API_KEY')
MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')


class GroqClient:
    def __init__(self, api_key: str):
        self.client = AsyncGroq(api_key=api_key)
        self.client = from_groq(self.client, mode=Mode.TOOLS)

    async def generate_queries(self, instruction: str, question: str):
        data = instruction + question
        response = await self.client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": data}],
            response_model=QueryList,
        )
        return response.model_dump()["queries"]


class QueryList(BaseModel):
    queries: list[str]


class NewsFetcher:
    def __init__(self, language: str = 'en', country: str = 'US', max_results: int = 3):
        self.gnews = GNews(language=language, country=country, max_results=max_results)

    def fetch_articles(self, query: str):
        articles_json_list = self.gnews.get_news(query)
        tasks = [self.gnews.get_full_article(article['url']) for article in articles_json_list]
        tasks = [t.text for t in tasks if t is not None]
        return tasks


class TextChunker:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, 
                                                       chunk_overlap=chunk_overlap)

    def chunk_text(self, text: str):
        text = Document(page_content=text)
        return self.splitter.split_documents(documents=[text])


class VectorSearch:
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def fetch_embeddings(self, articles: list[Document]):
        client = MistralClient(api_key=MISTRAL_API_KEY)

        #articles = 

        embeddings_response = client.embeddings(model="mistral-embed", input=[a.page_content for a in articles])
        
        embeddings_response = [e.embedding for e in embeddings_response.data]

        return embeddings_response

    async def encode_articles(self, articles: list[str]):
        vectors = await self.fetch_embeddings(articles)
        self.index = faiss.IndexFlatL2(len(vectors[0]))
        self.index.add(np.array(vectors))


    def search_similar_articles(self, query: str, articles: list[str], top_k: int = 5):
        query_vector = asyncio.run(self.fetch_embeddings([query]))
        distances, indices = self.index.search(np.array(query_vector), top_k)
        return [(articles[idx], distances[0][i]) for i, idx in enumerate(indices[0])]


class ResponseGenerator:
    def __init__(self, client: GroqClient):
        self.client = client

    async def generate_response(self, retrieved_text: str, prompt_template: str):
        response = await self.client.client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": prompt_template.format(text=retrieved_text)}],
            response_model=ResponseModel,
        )
        return response.model_dump()["text"]


class ResponseModel(BaseModel):
    text: str


class NewsAggregator:
    def __init__(self):
        self.groq_client = GroqClient(KEY_GROQ)
        self.news_fetcher = NewsFetcher()
        self.chunker = TextChunker()
        self.vector_search = VectorSearch(MISTRAL_API_KEY)
        self.response_generator = ResponseGenerator(self.groq_client)

    async def process(self, question: str):
        instruction = "Please generate a list of three queries related to the following question: "
        
        # Generate three queries
        time_start = time.time()
        queries = await self.groq_client.generate_queries(instruction, question)
        print(f"Time taken for query generation: {time.time() - time_start:.2f} seconds")

        # Fetch news articles for each query asynchronously
        time_start = time.time()
        tasks = []
        for query in queries:
            tasks.extend(self.news_fetcher.fetch_articles(query))
        all_articles = tasks
        merged_articles = all_articles#[article for articles in all_articles for article in articles]
        print(f"Time taken for article fetching: {time.time() - time_start:.2f} seconds")

        # Chunk articles
        time_start = time.time()
        chunked_articles = []
        for article in merged_articles:
            chunks = self.chunker.chunk_text(article)
            chunked_articles.extend(chunks)
        print(f"Time taken for text chunking: {time.time() - time_start:.2f} seconds")

        # Vectorize articles
        time_start = time.time()
        await self.vector_search.encode_articles(chunked_articles)
        print(f"Time taken for vectorisation: {time.time() - time_start:.2f} seconds")

        # Search similar articles
        time_start = time.time()
        user_query = question
        similar_articles = self.vector_search.search_similar_articles(user_query, chunked_articles)
        retrieved_text = "\n\n".join([article for article, _ in similar_articles])
        print(f"Time taken for article retrieval: {time.time() - time_start:.2f} seconds")

        # Generate response
        time_start = time.time()
        prompt_template = "Please provide a comprehensive summary of the following information:\n\n{text}\n\nSummary:"
        response = await self.response_generator.generate_response(retrieved_text, prompt_template)
        print(f"Time taken for response generation: {time.time() - time_start:.2f} seconds")

        return response


async def main():
    aggregator = NewsAggregator()
    question = "How many people were killed in Gaza?"
    response = await aggregator.process(question)
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
