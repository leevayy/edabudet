import telebot

BOT_TOKEN = open('BOT_TOKEN.txt').readline()

bot = telebot.TeleBot(BOT_TOKEN)