import httpx

from schema import Film
from settings import settings


async def search_for_movie(query: str) -> list[Film]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f'{settings.KINOPOISK_UNOFFICIAL_API}/films/search-by-keyword',
            headers={'X-API-KEY': settings.KINOPOISK_API_TOKEN},
            params={'keyword': query, 'page': 1},
        )
    json = response.json()
    if response.status_code != 200:
        raise Exception(json['error'])

    result = []
    for film_data in json['films']:
        film = Film(**film_data)
        result.append(film)
    return result
