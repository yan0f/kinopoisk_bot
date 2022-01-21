import json
import os

import requests

from types_ import Film

API_VERSION = 'v2.1'
KINOPOISK_UNOFFICIAL_API = 'https://kinopoiskapiunofficial.tech/api/' + API_VERSION + '/'


class Movie:
    def __init__(self, data: Film) -> None:
        self.kp_id = data['filmId']
        self.name = data.get('nameEn') or data.get('nameRu') or ''
        self.ru_name = data.get('nameRu', '')
        self.year = data['year'].split('-')[0] if data['year'] != 'null' else None
        self.duration = data.get('filmLength', '')
        self.genres = [genre['genre'] for genre in data['genres']]
        self.countries = [country['country'] for country in data['countries']]
        self.kp_rate = data['rating'] if data['rating'] != 'null' else None
        self.kp_url = f'https://www.kinopoisk.ru/film/{self.kp_id}/'
        self.poster_url = data['posterUrl']
        self.poster_preview_url = data['posterUrlPreview']
        self.description = data.get('description', '')


def search_for_movie(query: str) -> list[Movie]:
    headers = {"X-API-KEY": os.getenv('KINOPOISK_API_TOKEN')}
    request = requests.get(
        KINOPOISK_UNOFFICIAL_API + 'films/search-by-keyword',
        headers=headers,
        params={"keyword": query, "page": 1}
    )
    request_json = json.loads(request.text)
    if request_json.get('error'):
        raise Exception(request_json['error'])
    result = []
    for film in request_json['films']:
        result.append(Movie(film))
    return result
