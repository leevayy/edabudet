from telebot import types


def start(message, bot):
    id = message.chat.id
    RepMarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    text = 'Добро пожаловать в меню Едабота.'
    btn1 = types.KeyboardButton('Найти рецепт')
    btn2 = types.KeyboardButton('Добавить рецепт')
    RepMarkup.add(btn1, btn2)
    bot.send_message(id, text=text, reply_markup=RepMarkup)


def reply(message, bot):
    user_ans = message.text
    RepMarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    InlMarkup = types.InlineKeyboardMarkup()
    ans = "incorrect input"
    back = types.KeyboardButton('Назад к поиску')
    ex = types.KeyboardButton('Выход в меню')
    match user_ans:
        # Блок с поиском рецептов
        case 'Найти рецепт'| 'Назад к поиску':
            btn1 = types.KeyboardButton('Поиск по названию')
            btn2 = types.KeyboardButton('Поиск по тегам')
            btn3 = types.KeyboardButton('Топ рецептов')

            RepMarkup.add(btn1, btn2, btn3, ex)
            ans = 'Как будете искать?'

        case 'Поиск по названию':
            RepMarkup.add(ex, back)
            ans = 'Пожалуйста, введите название блюда'

        case 'Поиск по тегам':
            RepMarkup.add(ex, back)
            ans = 'Пожалуйста, введите теги через запятую'

        case 'Топ рецептов':
            # Здесь должно быть обращение к бд, но её ещё нет
            RepMarkup.add(ex, back)
            ans = 'Сделайте бд, плиз'
            form_preview(message.chat.id, bot)

        case 'рецепт':
            btn1 = types.InlineKeyboardButton('Лайк', callback_data='liked')
            btn2 = types.InlineKeyboardButton('ДизЛайк', callback_data='disliked')
            InlMarkup.add(btn1, btn2)
            ans = '<b>Самое вкусное нихуя</b>'

        # Блок с созданием рецептов
        case 'Добавить рецепт':
            RepMarkup.add(ex)
            ans = 'Сделайте хз что, чтобы добавить рецепт в бд бота'

        # Блок обработчик возвратов
        case 'Выход в меню':
            btn1 = types.KeyboardButton('Найти рецепт')
            btn2 = types.KeyboardButton('Добавить рецепт')
            RepMarkup.add(btn1, btn2)
            ans = 'С возвращением в меню Едабота'

    bot.send_message(message.chat.id, text=ans, reply_markup=RepMarkup, parse_mode='HTML')

def form_preview(id, bot):
    name = 'ы' # Вытянуть из бд
    description = 'Я ебал, меня сосали' # Вытянуть из бд
    parts = 'Доширак' # Вытянуть из бд
    ans = f'<center><b>{name}</b></center>'
    bot.send_message(id, text=ans)


