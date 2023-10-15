from telebot import types

from bot.bot_connection import bot

tags = [(0, 'ххх'), 
        (1, 'хуй'),
        (2, 'жопа')]

@bot.inline_handler(lambda query: len(query.query) > 0)
def query_text(inline_query):
    try:
        result = list(map(
            lambda tag: types.InlineQueryResultArticle(tag[0], tag[1], types.InputTextMessageContent(tag[1])),
            filter(lambda tag: tag[1][:len(inline_query.query)] == inline_query.query, tags)
        ))
        
        bot.answer_inline_query(inline_query.id, result)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    bot.infinity_polling()
    