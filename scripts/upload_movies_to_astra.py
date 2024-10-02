import os
import json
from datetime import datetime
from astrapy import DataAPIClient
from dotenv import load_dotenv

load_dotenv()

year = 2024

# Define the path to the JSON file   
script_dir = "../data/processed" # Directory of the script
json_file_path = os.path.join(script_dir, f'tmdb_movies_{year}_processed.json')

# Load JSON file into memory
with open(json_file_path, 'r', encoding='utf-8') as json_file:
    movies_data = json.load(json_file)

# Initialize Astra DB client
client = DataAPIClient(os.environ["ASTRA_DB_APPLICATION_TOKEN"])
database = client.get_database(os.environ["ASTRA_DB_API_ENDPOINT"])

collection = database.get_collection("movies")

# Iterate through each movie document in the JSON data
for movie in movies_data:
    movie_id = movie['_id']
    title = movie['metadata']['title']
    genres = movie['metadata']['genre']
    cast = movie['metadata']['cast']
    director = movie['metadata']['director']
    release_date = movie['metadata']['release_date']
    poster_path = movie['metadata']['poster_path']
    content_semantic = movie['content_semantic']
    source = movie['metadata']['source']

    print(f"Processing movie: {title}")

    # Update the database with the movie's content
    while True:
        try:
            collection.insert_one(
                {
                    '_id': movie_id,
                    'title': title,
                    '$vectorize': content_semantic,  
                    'content': movie['content'],
                    'content_semantic': content_semantic,
                    'metadata': {
                        'ingested': datetime.now(),
                        'genres': genres,
                        'cast': cast,
                        'director': director,
                        'release_date': release_date,
                        'poster_path': poster_path,
                        'source': source,
                    }
                }
            )
            print(f"Successfully updated: {title}")
        except Exception as ex:
            print(f"Error updating {title}: {ex}")
            print("Retrying...")
            continue
        break
