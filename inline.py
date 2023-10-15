from telebot import types
from bot.bot_connection import bot
from database.database_commands import get_all_tags


def query_text(inline_query):
    raw_tags = get_all_tags()
    tags = [(i, raw_tags[i][0]) for i in range(len(raw_tags))]
    try:
        result = list(
            map(lambda tag: types.InlineQueryResultArticle(tag[0], tag[1], types.InputTextMessageContent(tag[1])),
                filter(lambda tag: tag[1][:len(inline_query.query)] == inline_query.query, tags)))

        bot.answer_inline_query(inline_query.id, result)
    except Exception as e:
        print(e)
