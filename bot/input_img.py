from bot.bot_connection import bot
from telebot import types




@bot.message_handler(func=lambda message: message.text == name)
def get_recipe(message):
    #photo = open("recipe.jpg", "rb")
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('лайк', callback_data='like'),
               types.InlineKeyboardButton('дизлайк', callback_data='dislike'),
    row_width = 2)
    #bot.send_photo(message.chat.id, photo, description, reply_markup=markup)
    bot.send_message(message.chat.id, photo, description, reply_markup=markup)


