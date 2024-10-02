import os
import json
import requests
import csv
from datetime import datetime
from dotenv import load_dotenv
from time import sleep
import json
import pandas as pd
import numpy as np

year = 2021

# Folder paths
input_folder = "../data/raw"
output_folder = "../data/processed"

# CSV file to get movie data from and write processed data to
input_csv = os.path.join(input_folder, f'tmdb_movies_{year}.csv')
output_csv = os.path.join(output_folder, f'tmdb_movies_{year}_processed.csv')
output_json = os.path.join(output_folder, f'tmdb_movies_{year}_processed.json')


def create_movie_document(row):    
    # Prepare the document structure with handling for null/NaN values
    movie_document = {
        "_id": row["id"] if pd.notna(row["id"]) else None,  # Ensure there's no NaN for ID
        "content": row["semantic_field"] if pd.notna(row["semantic_field"]) else "",
        "content_semantic": row["semantic_field"] if pd.notna(row["semantic_field"]) else "",  # Copy of content for vectorization
        "metadata": {
            "source": f"https://www.themoviedb.org/movie/{row['id']}" if pd.notna(row['id']) else "",
            "title": row["title"] if pd.notna(row["title"]) else "",
            "language": "en",  # Language is always "en"
            "id": row["id"] if pd.notna(row["id"]) else "",
            "genre": row["genres"] if pd.notna(row["genres"]) else "",
            "cast": row["cast"] if pd.notna(row["cast"]) else "",
            "director": row["director"] if pd.notna(row["director"]) else "",
            "poster_path": row["poster_path"] if pd.notna(row["poster_path"]) else "",
            "release_date": row["release_date"] if pd.notna(row["release_date"]) else ""
        }
    }
    
    return movie_document

# Write the movie data to a CSV file
def write_to_csv(movies):
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['_id', 'content', 'content_semantic', 'metadata']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for movie in movies:
            writer.writerow(movie)

# Write the movie data to a JSON file
def write_to_json(movies):
    with open(output_json, 'w', encoding='utf-8') as jsonfile:
        json.dump(movies, jsonfile, ensure_ascii=False, indent=4)


def process_movies_for_langflow():
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(input_csv)

    # Replace NaN values with empty strings before processing
    df = df.replace({np.nan: ""})

    # Process each row into the required format
    documents = [create_movie_document(row) for _, row in df.iterrows()]

    #Write to json file
    write_to_json(documents)

if __name__ == "__main__":
    process_movies_for_langflow()