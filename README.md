# MovieLang 🎬

This project is a movie recommendation system built using AstraDB, LangChain, Langflow, Langsmith, Vercel AI SDK, and Next.js, with data sourced from the TMDB API. The system processes user queries and provides personalized movie recommendations in a structured JSON format.

**Try it out here**: [MovieLang](https://movielang.shubh.ink/)

## Features:

- AI-Powered Recommendations: Leveraging LangChain and a Langflow vector-based RAG (Retrieval-Augmented Generation) pipeline to provide accurate and relevant movie suggestions.
- Feedback: Fine-tuning with Langsmith for continuous improvement and better user experience.
- Real-time Interactivity: Integrated with Vercel AI SDK for dynamic, real-time chat interactions.
- Movie Data from TMDB: Retrieves and formats movie data such as title, rating, genres, cast, and streaming providers using the TMDB API.

## Setup:

#### .env
- Langflow Endpoint and Token: Required for interacting with Langflow’s vector RAG pipeline.
- AstraDB Endpoint and Token: Used to store and query vectorized movie data.
- OpenAI Token: For language model interactions.

#### Data
- Get data from TMDB and format it using `scripts/download_tmdb_movies.py` and `scripts/process_movies_for_langflow.py`.
- Upload the processed data to AstraDB using `scripts/upload_movies_to_astra.py`.

## Set Up a RAG Pipeline in Langflow:
- Create a new RAG flow that connects to OpenAI and AstraDB.
- Get the Endpoints.

## Running the Project:

- Clone the repository.
- Set up your environment variables in a .env.local file.
- Run the project as a standard Next.js app using: