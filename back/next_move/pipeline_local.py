import os
import sys
from os import getenv
from dotenv import load_dotenv
from pydantic import BaseModel
from gnews import GNews
import newspaper
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter
import instructor
from groq import Groq

import time

# Charger les variables d'environnement
load_dotenv()
KEY_GROQ = getenv('GROQ_API_KEY')

# Initialiser le client Groq
client = Groq(api_key=KEY_GROQ)
client = instructor.from_groq(client, mode=instructor.Mode.TOOLS)

#### Extraction des mots clés pour la query gnews

time_start = time.time()

# Classe pour extraire les mots-clés
class UserExtract(BaseModel):
    keywords: list[str]

# Définir la question et obtenir les mots-clés
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

time_end1 = time.time()
print(f"Time taken for keyword extraction: {time.time() - time_end1:.2f} seconds")

##### Requete GNews pour obtenir les articles

# Utiliser GNews pour obtenir les articles
gnews = GNews(language='en', country='US', max_results=10)
articles_json_list = gnews.get_news(' '.join(list_of_keywords))

# Extraire le contenu complet des articles
articles_content = []
for article in articles_json_list:
    try:
        article_data = gnews.get_full_article(article['url'])
        articles_content.append(article_data.text)
    except Exception as e:
        print(f"Error extracting article: {e}")
        
print(f"Time taken for article extraction: {time.time() - time_end1:.2f} seconds")
        
#### RAG pour générer une réponse

# Initialiser le modèle de transformation des phrases
model = SentenceTransformer('all-MiniLM-L6-v2')

# Encoder les articles dans des vecteurs
vectors = model.encode(articles_content)

# Créer et peupler l'index FAISS
index = faiss.IndexFlatL2(vectors.shape[1])
index.add(np.array(vectors))

# Fonction pour rechercher des articles similaires
def search_similar_articles(query, model, index, articles_content, top_k=5):
    query_vector = model.encode([query])
    distances, indices = index.search(np.array(query_vector), top_k)
    return [(articles_content[idx], distances[0][i]) for i, idx in enumerate(indices[0])]

time_end2 = time.time()
print(f"Time taken for vectorisation: {time.time() - time_end2:.2f} seconds")


#### Recherche dans les vecteurs pour obtenir des articles similaires

# Exemple de question utilisateur
user_query = "What are the recent developments in the war in Ukraine?"

# Recherche des articles similaires
similar_articles = search_similar_articles(user_query, model, index, articles_content)

# Joindre les articles similaires pour la génération de la réponse
retrieved_text = "\n\n".join([article for article, _ in similar_articles])

time_end3 = time.time()
print(f"Time taken for article retrieval: {time.time() - time_end3:.2f} seconds")

print(retrieved_text)

#### Génération de la réponse

class ResponseModel(BaseModel):
    text: str

# Définir une fonction pour générer une réponse à partir des articles similaires
def generate_response(retrieved_text, model, prompt_template):
    response = model.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {
                "role": "user",
                "content": prompt_template.format(text=retrieved_text),
            }
        ],
        response_model=ResponseModel,
    )
    return response.model_dump()["text"]

# Définir le modèle et le template de prompt pour générer la réponse
prompt_template = "Please provide a comprehensive summary of the following information:\n\n{text}\n\nSummary:"
response = generate_response(retrieved_text, client, prompt_template)

# Afficher la réponse
print(response)

time_end4 = time.time()
print(f"Time taken for response generation: {time.time() - time_end4:.2f} seconds")
