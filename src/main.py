import logging
from uuid import uuid4

from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    InlineQueryHandler,
    Application,
)

from kinopoisk import Movie, search_for_movie
from settings import settings

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


async def start(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text(
        'Этот бот помогает искать фильмы на Кинопоиске. '
        'Он работает в любом чате, просто напиши @kp_bobot в поле ввода.'
    )


async def help_command(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text('Help!')


async def inlinequery(update: Update, _: CallbackContext) -> None:
    """Handle the inline query."""
    query = update.inline_query.query
    user = update.inline_query.from_user
    logger.info(f'@{user.username}, {user.id=}, {query=}')
    movies = await search_for_movie(query)
    result = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            description=movie.description,
            title=get_result_article_title(movie),
            thumbnail_url=movie.poster_preview_url,
            input_message_content=InputTextMessageContent(movie.kp_url),
        )
        for movie in movies
    ]
    await update.inline_query.answer(result)


def get_result_article_title(movie: Movie) -> str:
    title = ''
    if movie.ru_name:
        title += f'«{movie.ru_name}» ({movie.name}, {movie.year})'
    else:
        title += f'{movie.name}'
        if movie.year:
            title += f', {movie.year}'
    if movie.kp_rate:
        title += f' • {movie.kp_rate}'
    return title


def main() -> None:
    application = Application.builder().token(settings.TELEGRAM_BOT_API_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(InlineQueryHandler(inlinequery))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
