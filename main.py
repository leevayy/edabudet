from bot.bot_connection import bot
from database.database_commands import create_database, get_users
import bot.bot_messages as messages


def start_polling():
    @bot.message_handler(commands=['start'])
    def start_message(message):
        messages.start(message, bot)
    
    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):
        messages.reply(message, bot)
        print(get_users())
    
    bot.infinity_polling()


if __name__ == "__main__":
    create_database()
    start_polling()

