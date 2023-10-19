import httpx

from settings import settings
from types_ import Film


class Movie:
    def __init__(self, data: Film) -> None:
        self.kp_id = data['filmId']
        self.name = data.get('nameEn') or data.get('nameRu') or ''
        self.ru_name = data.get('nameRu', '')
        self.year = data['year'].split('-')[0] if data['year'] != 'null' else None
        self.duration = data.get('filmLength', '')
        self.countries = [country['country'] for country in data['countries']]
        self.kp_rate = data['rating'] if data['rating'] != 'null' else None
        self.kp_url = f'https://www.kinopoisk.ru/film/{self.kp_id}/'
        self.poster_preview_url = data['posterUrlPreview']
        self.description = data.get('description', '')


async def search_for_movie(query: str) -> list[Movie]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            settings.KINOPOISK_UNOFFICIAL_API + '/films/search-by-keyword',
            headers={'X-API-KEY': settings.KINOPOISK_API_TOKEN},
            params={'keyword': query, 'page': 1},
        )
    json = response.json()
    if response.status_code != 200:
        raise Exception(json['error'])
    result = []
    for film_data in json['films']:
        result.append(Movie(film_data))
    return result
