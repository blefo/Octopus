
# Octopus - Mistral Hackathon - May 2024

<div align="center">
  <img src="https://avatars.githubusercontent.com/u/132372032?s=200&v=4" alt="Mistral AI" width="100"/>
  <img src="https://m.iotone.com/files/vendor/groq635203cb3080c_1.jpg" alt="Groq" width="100"/>
</div>

## Live Demo
<div align="center">
  <img src="https://github.com/blefo/Octopus/blob/main/live_demo.gif" alt="Live Octopus" height="400" width="200"/>
</div>

## Pitch Deck

### Inspiration
When it comes to staying informed, you have two options: traditional newspapers, which are reliable but often cluttered with irrelevant content, or social media, which is quick but plagued with ads and disinformation. Our project merges the best of both worlds: **fast and truly informative**. You receive only the information that is **relevant to you and based on real facts**. Additionally, you can dive deeper into topics with naturally arising questions.

### What it does
It all starts with the most informative news feed. You skip the useless content and read what truly matters: the key points of current events and related questions. For each news item, you get an informative title followed by three key points, sparing you from reading the entire article. As you read these brief points, questions will naturally come to mind. You can click on any question that interests you or ask a custom question if your specific interest isn't addressed. You'll then receive answers from various sources and perspectives, all concisely presented. In summary, you navigate current events by accessing relevant and unbiased information.

### How we built it
We developed both the back end and front end of the project. The back end utilizes technologies like Python and Django. We use a PostgreSQL database to store the news feed, and we developed an API to provide answers to questions with sources and content.

### Challenges we ran into
For a rapid-answer RAG application focused on news, speed is crucial. Our main challenge was leveraging free data sources and retrieving pertinent information quickly. To achieve faster responses, we utilized the latest hosted databases for storing vectors and retrieving information more efficiently. Storing all the latest embedded articles in the database was a viable solution.

### Accomplishments that we're proud of
We are proud to present an MVP that effectively embodies the original concept we envisioned at the start of the hackathon.

### What we learned
We gained deeper insights into Mistral technologies. Leveraging the instructor library for formatting the LLM's output was a remarkable discovery for most of us, and we applied it throughout the project.

### What's next for Octopus
Our next step is to make Octopus faster at answering questions. We designed Octopus to be scalable, so the subsequent phase involves deploying it on cloud providers.

## Installation

### Requirements
- [Python >= 3.8](https://www.python.org/downloads/)
- [Node.js](https://nodejs.org/en/download/)

### Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/blefo/Octopus.git
    cd Octopus
    ```
2. Install the required packages for the backend:
    ```bash
    cd back
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
    pip install -e .
    ```
3. Create a `.env` file at the root of the project with the following content:
    ```bash
    MISTRAL_API_KEY=YOUR_MISTRAL_API_KEY
    GROQ_API_KEY=YOUR_GROQ_API_KEY
    ```
4. Install the required packages for the frontend:
    ```bash
    cd front
    npm install
    ```
5. Run the backend:
    ```bash
    cd back
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver
    ```
6. Run the frontend:
    ```bash
    cd front
    npm run dev
    ```
