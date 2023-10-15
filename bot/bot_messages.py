from telebot import types
from bot.bot_connection import bot
from database.database_commands import add_user, get_user, search, change_search_state

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
                
                search_result = search(search_state, message.text)
                if len(search_result) == 0:
                    return bot.send_message(message.chat.id, DB_NOT_FOUND_MSG)
                else:
                    return bot.send_message(message.chat.id, str(search_result[0]))
                
            # except TypeError as error:
            #     print(error)
            except Exception as error:
                if str(error) != SEARCH_STATE_IS_NONE: raise error

