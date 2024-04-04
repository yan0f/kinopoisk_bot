import html
import json
import logging
import traceback
from uuid import uuid4

from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    InlineQueryHandler,
)

from kinopoisk import search_for_movie
from settings import settings

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.getLogger('httpx').setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def start(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text(
        'Этот бот помогает искать фильмы на Кинопоиске. '
        'Он работает в любом чате, просто напиши @kp_bobot в поле ввода.'
    )


async def inlinequery(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the inline query."""
    query = update.inline_query.query
    user = update.inline_query.from_user
    logger.info(f'@{user.username}, {user.id=}, {query=}')
    movies = await search_for_movie(query)
    result = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            description=movie.description,
            title=movie.article_title,
            thumbnail_url=movie.poster_url_preview,
            input_message_content=InputTextMessageContent(movie.kp_url),
        )
        for movie in movies
    ]
    await update.inline_query.answer(result)


async def error_handler(update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error('Exception while handling an update:', exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = ''.join(tb_list)

    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        'An exception was raised while handling an update\n'
        f'<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}'
        '</pre>\n\n'
        f'<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n'
        f'<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n'
        f'<pre>{html.escape(tb_string)}</pre>'
    )

    await context.bot.send_message(
        chat_id=settings.DEVELOPER_CHAT_ID, text=message, parse_mode=ParseMode.HTML
    )


def main() -> None:
    application = Application.builder().token(settings.TELEGRAM_BOT_API_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(InlineQueryHandler(inlinequery))

    application.add_error_handler(error_handler)

    application.run_polling(allowed_updates=Update.INLINE_QUERY)


if __name__ == '__main__':
    main()
