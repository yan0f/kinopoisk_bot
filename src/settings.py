from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')

    API_VERSION: str = 'v2.1'
    KINOPOISK_UNOFFICIAL_API: str = f'https://kinopoiskapiunofficial.tech/api/{API_VERSION}'
    KINOPOISK_API_TOKEN: str
    TELEGRAM_BOT_API_TOKEN: str


settings = Settings()
