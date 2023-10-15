from telebot import types
from bot.bot_connection import bot
from database.database_commands import add_user, get_user, search, change_search_state, get_recipes

class keynames:
    SEARCH = 'Поиск'
    RECOMMENDATIONS = 'Гига-кнопка'
    SETTINGS = 'Персонализация'
    TO_MENU = 'Отмена'
    BANNED = 'Бан-лист'
    BANNED_ADD = 'Добавить' 
    FAVORITE_TAGS = 'Топ тэгов'


def keyboard(swap_keys = {}):   
    search = types.KeyboardButton(keynames.SEARCH)
    recommendations = types.KeyboardButton(keynames.RECOMMENDATIONS)
    settings = types.KeyboardButton(keynames.SETTINGS)
    
    keyboard = [search, recommendations, settings]
    for place in swap_keys:
        keyboard[place] = swap_keys[place]
        
    return types.ReplyKeyboardMarkup(
        resize_keyboard=True
    ).add(keyboard[0], keyboard[1], keyboard[2])
    
def start(message):
    id = message.chat.id
    add_user(id, message.chat.username)
    
    text = 'Добро пожаловать в меню ЕдаБота.'
    
    bot.send_message(id, text=text, reply_markup=keyboard())

def reply(message):    
    match message.text:
        case keynames.TO_MENU:
            change_search_state(message.chat.id, 'None')
            bot.send_message(message.chat.id, 'Главное меню', reply_markup=keyboard())

        case keynames.SEARCH:
            change_search_state(message.chat.id, 'recipe')
            bot.send_message(message.chat.id, 'Введите запрос: ', reply_markup=keyboard({0: keynames.TO_MENU}))

        case keynames.RECOMMENDATIONS:
            bot.send_message(message.chat.id, 'Вот что мы нашли для вас:')

        case keynames.SETTINGS:
            bot.send_message(message.chat.id, 'Настройки', reply_markup=keyboard({
                0: keynames.TO_MENU,
                1: keynames.BANNED,
                2: keynames.FAVORITE_TAGS
            }))

        case keynames.BANNED:
            bot.send_message(message.chat.id, 'Бан-лист', reply_markup=keyboard({
                0: keynames.TO_MENU,
                1: keynames.BANNED_ADD,
                2: keynames.FAVORITE_TAGS
            }))
            
        case _:
            SEARCH_STATE_IS_NONE = "Search state is None"
            DB_NOT_FOUND_MSG = "У нас нет такого"
            try: 
                search_state = get_user(message.chat.id)[2]
                if search_state == None:
                    raise Exception(SEARCH_STATE_IS_NONE)
                
                search_results = search(search_state, message.text)
                if len(search_results) == 0:
                    return bot.send_message(message.chat.id, DB_NOT_FOUND_MSG)
                else:
                    send_search_card(message.chat.id, message.text, search_results)
                
            except Exception as error:
                if str(error) != SEARCH_STATE_IS_NONE: raise error

def send_search_card(user_id, query, search_results):
    markup = types.InlineKeyboardMarkup()
    for i in range(min(len(search_results), 10)):
        result = search_results[i]
        markup.add(types.InlineKeyboardButton(result[2], callback_data=result[0]))
    # markup.add(types.InlineKeyboardButton('<-', callback_data='<-'),
    #             types.InlineKeyboardButton('0', callback_data='0'),
    #             types.InlineKeyboardButton('->', callback_data='->'),
    #             row_width=3)

    bot.send_message(user_id, f'Вот что мы нашли по запросу: {query}',reply_markup=markup)
    
def callback(call):
    print(call.data)
    for recipe in get_recipes():
        if int(recipe[0]) == int(call.data):
            # bot.delete_message(call.message.chat.id, call.inline_message_id)
            # bot.edit_message_text(message_id=call.inline_message_id,chat_id=call.message.chat.id, text=f'<b>{recipe[2]}</b>\n\n{recipe[3]}', parse_mode='HTML')
            try:
                bot.send_message(call.message.chat.id, f'<b>{recipe[2]}</b>\n\n{recipe[3]}', parse_mode='HTML')
            except Exception as error:
                print(error)
        