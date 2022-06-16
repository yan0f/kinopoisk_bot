from typing import TypedDict


class Country(TypedDict):
    country: str


class Genre(TypedDict):
    genre: str


class Film(TypedDict):
    filmId: int
    nameEn: str
    nameRu: str
    year: str
    filmLength: str
    genres: list[Genre]
    countries: list[Country]
    rating: str
    posterUrl: str
    posterUrlPreview: str
    description: str
