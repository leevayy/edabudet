from bot.bot_connection import bot
from database.database_commands import create_database
from inline import query_text
import bot.bot_messages as messages


def start_polling():
    @bot.message_handler(commands=['start'])
    def start_message(message):
        messages.start(message)
    
    @bot.message_handler(content_types=['text'])
    def handle_text_messages(message):
        messages.reply(message)

    @bot.inline_handler(lambda query: len(query.query) > 0)
    def get_inline_request(request):
        query_text(request)


    bot.infinity_polling()

if __name__ == "__main__":
    create_database()

    start_polling()
