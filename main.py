from bot.bot_connection import bot
from database.database_commands import create_database
import bot.bot_messages as messages
from bot.bot_messages import callback


def start_polling():
    @bot.message_handler(commands=['start'])
    def start_message(message):
        messages.start(message)
    
    @bot.message_handler(content_types=['text'])
    def handle_text_messages(message):
        messages.reply(message)

    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        messages.callback(call)

    bot.infinity_polling()

if __name__ == "__main__":
    create_database()
    start_polling()
