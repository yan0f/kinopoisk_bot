import logging
import os
from uuid import uuid4

from dotenv import load_dotenv, find_dotenv
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import CallbackContext, CommandHandler, InlineQueryHandler, Updater

load_dotenv(find_dotenv())

from kinopoisk import Movie, search_for_movie

TELEGRAM_BOT_API_TOKEN = os.environ['TELEGRAM_BOT_API_TOKEN']

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Этот бот помогает искать фильмы на Кинопоиске. '
                              'Он работает в любом чате, просто напиши @kp_bobot в поле ввода.')


def help_command(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def inlinequery(update: Update, _: CallbackContext) -> None:
    """Handle the inline query."""
    query = update.inline_query.query
    logger.info(query)
    movies = search_for_movie(query)
    result = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            description=movie.description,
            title=get_result_article_title(movie),
            thumb_url=movie.poster_preview_url,
            input_message_content=InputTextMessageContent(movie.kp_url),
        ) for movie in movies]
    update.inline_query.answer(result)


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
    updater = Updater(token=TELEGRAM_BOT_API_TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help_command))

    dispatcher.add_handler(InlineQueryHandler(inlinequery))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
