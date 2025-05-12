from telebot import types
markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
goal_markup = types.KeyboardButton('УДАРИТЬ🥅')
packs_markup = types.KeyboardButton('Открыть Пак😉')

markup1.add(goal_markup, packs_markup)

markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
udar1 = types.KeyboardButton('1')
udar2 = types.KeyboardButton('2')
udar3 = types.KeyboardButton('3')
udar4 = types.KeyboardButton('4')
home = types.KeyboardButton('Домой🥅')
udar5 = types.KeyboardButton('5')
markup2.add(udar1, udar2, udar3, udar4, home, udar5)

