from bot.bot_connection import bot
from telebot import types

if __name__ == '__main__':
    @bot.message_handler(content_types=['text'])
    def search_result(msg: types.Message):
        markup = types.InlineKeyboardMarkup()
        for result in results:
            markup.add(types.InlineKeyboardButton(result, callback_data='hello'))
        markup.add(types.InlineKeyboardButton('<-', callback_data='<-'),
                   types.InlineKeyboardButton('0', callback_data='0'),
                   types.InlineKeyboardButton('->', callback_data='->'),
                   row_width=3)
        
        bot.send_message(msg.chat.id, f'Вот что я нашел по запросу {msg.text}:',
                         reply_markup = markup)
        
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
        
    bot.infinity_polling()
        