from pydantic import BaseModel, ConfigDict, Field, computed_field, field_validator


class CamelModel(BaseModel):

    @staticmethod
    def to_camel_case(string: str) -> str:
        string_split = string.split('_')
        return string_split[0] + ''.join(word.capitalize() for word in string_split[1:])

    model_config = ConfigDict(
        alias_generator=to_camel_case,
        populate_by_name=True,
    )


class Country(BaseModel):
    country: str


class Genre(BaseModel):
    genre: str


class Film(CamelModel):
    kp_id: int = Field(alias='filmId')
    name_en: str | None = None
    name_ru: str | None = None
    year: str
    duration: str | None = Field('', alias='filmLength')
    genres: list[Genre]
    countries: list[Country]
    kp_rate: str | None = Field(alias='rating')
    poster_url: str | None = None
    poster_url_preview: str = Field(alias='posterUrlPreview')
    description: str | None = Field('')

    @field_validator('year')
    @classmethod
    def transform_year(cls, year: str) -> str | None:
        return year.split('-')[0] if year != 'null' else None

    @computed_field
    @property
    def kp_url(self) -> str:
        return f'https://www.kinopoisk.ru/film/{self.kp_id}/'

    @field_validator('kp_rate')
    @classmethod
    def transform_kp_rate(cls, kp_rate: str) -> str | None:
        return kp_rate if kp_rate != 'null' else None

    @property
    def article_title(self) -> str:
        title = ''
        if self.name_ru and self.name_en and self.year:
            title += f'«{self.name_ru}» ({self.name_en}, {self.year})'
        elif self.name_ru:
            title += f'«{self.name_ru}», {self.year}'
        else:
            title += f'{self.name_en}, {self.year}'
            if self.year:
                title += f', {self.year}'
        if self.kp_rate:
            title += f' • {self.kp_rate}'
        return title
