from telebot import types
from bot.bot_connection import bot
from database.database_commands import search


def query_text(inline_query):
    try:
        result = list(
            map(lambda recipe: types.InlineQueryResultArticle(id=recipe[0],
                    title=recipe[2], input_message_content=types.InputTextMessageContent(recipe[2])
                ),
                search('recipe', inline_query.query)
            ))

        bot.answer_inline_query(inline_query.id, result)
    except Exception as e:
        print(e)
