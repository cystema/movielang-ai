import os
import json
import requests
import csv
from datetime import datetime
from dotenv import load_dotenv
from time import sleep

# Load environment variables
load_dotenv()

# TMDB API credentials
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# Base URL for TMDB API
TMDB_BASE_URL = "https://api.themoviedb.org/3"

year = 2021

input_folder = "data/raw"

# CSV file to store movie data
output_csv = os.path.join(input_folder, f'tmdb_movies_{year}.csv')


# Fetch data from the /discover endpoint for 2024
def fetch_movies_from_tmdb(page):
    url = f"{TMDB_BASE_URL}/discover/movie"
    params = {
        'api_key': TMDB_API_KEY,
        'include_adult': 'true',
        'include_video': 'false',
        'language': 'en-US',
        'page': page,
        'primary_release_year': year,
        'region': 'US',
        'sort_by': 'popularity.desc',
        'vote_count.gte': 20,
        'watch_region': 'US',   
        'with_original_language': 'en'  
    }
    response = requests.get(url, params=params)
    response.raise_for_status()  # Raise error for invalid response
    return response.json()


# Fetch additional details (genres, cast, director)
def fetch_movie_details(movie_id):
    # Fetch genres
    details_url = f"{TMDB_BASE_URL}/movie/{movie_id}"
    credits_url = f"{TMDB_BASE_URL}/movie/{movie_id}/credits"
    providers_url = f"{TMDB_BASE_URL}/movie/{movie_id}/watch/providers"

    details_params = {'api_key': TMDB_API_KEY, 'language': 'en-US'}
    
    details_response = requests.get(details_url, params=details_params)
    credits_response = requests.get(credits_url, params=details_params)
    providers_response = requests.get(providers_url, params=details_params)
    
    details_response.raise_for_status()
    credits_response.raise_for_status()
    providers_response.raise_for_status()

    details = details_response.json()
    credits = credits_response.json()
    providers = providers_response.json()

    # Extract genres
    genres = [genre['name'] for genre in details.get('genres', [])]

    # Extract cast and director
    cast = [member['name'] for member in credits.get('cast', [])[:5]]  # Top 5 cast members
    director = None
    for crew_member in credits.get('crew', []):
        if crew_member['job'] == 'Director':
            director = crew_member['name']
            break

    # Extract streaming providers for US
    us_providers = providers.get('results', {}).get('US', {}).get('flatrate', [])
    provider_names = [provider['provider_name'] for provider in us_providers]
    
    return genres, cast, director, provider_names

# Scrub data (optional cleaning step)
def scrub(text):
    return text.replace('\n', ' ').strip()


# Write the movie data to a CSV file
def write_to_csv(movies):
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'id', 'genres', 'cast', 'director', 'poster_path', 'release_date', 'semantic_field']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for movie in movies:
            writer.writerow(movie)


# Main function to fetch and process movies from TMDB
def process_movies():
    all_movies = []
    page = 1
    total_pages = 1

    while page <= total_pages:
        print(f"Fetching page {page} of movies from TMDB API...")
        
        # Fetch movies for the current page
        movie_data = fetch_movies_from_tmdb(page)
        total_pages = movie_data['total_pages']  # Update total pages dynamically

        for movie in movie_data['results']:
            movie_id = movie['id']
            title = movie.get('title', 'Unknown')
            poster_path = movie.get('poster_path', 'N/A')
            release_date = movie.get('release_date', 'N/A')
            synopsis = movie.get('overview', 'N/A')
            average_rating = movie.get('vote_average', 'N/A')
            popularity = movie.get('popularity', 'N/A')

            try:
                # Fetch genres, cast, and director
                genres, cast, director, providers = fetch_movie_details(movie_id)

                if (providers):
                    # Construct semantic field
                    semantic_field = f"Movie '{title}', directed by {director}, released on {release_date}. \
                        Average rating is {average_rating} out of 10, and current popularity is {popularity}. \
                                    Overview: '{synopsis}' \
                                        Top cast includes: {', '.join(cast)}. Genres: {', '.join(genres)}.\
                                            Available on: {', '.join(providers)}."
                else:
                    # Construct semantic field
                    semantic_field = f"Movie '{title}', directed by {director}, released on {release_date}. \
                        Average rating is {average_rating} out of 10, and current popularity is {popularity}. \
                                    Overview: '{synopsis}' \
                                        Top cast includes: {', '.join(cast)}. Genres: {', '.join(genres)}. Streaming providers unkown."

                print(semantic_field)

                # Add to the movie list
                all_movies.append({
                    'title': title,
                    'id': movie_id,
                    'genres': ', '.join(genres),
                    'cast': ', '.join(cast),
                    'director': director,
                    'poster_path': poster_path,
                    'release_date': release_date,
                    'semantic_field': scrub(semantic_field)
                })

                print(f"Processed: {title}")
            except Exception as e:
                print(f"Failed to process movie {title}: {e}")

            # Sleep to avoid rate limits
            sleep(0.5)

        page += 1

    # Write the final movie data to CSV
    write_to_csv(all_movies)
    print(f"Finished processing all movies. Data saved to {output_csv}")


if __name__ == "__main__":
    process_movies()
