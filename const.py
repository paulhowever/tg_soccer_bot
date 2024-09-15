import telebot
from telebot import types
my_channel_id = '@zakonbvi'
TOKEN = '0_0'
bot = telebot.TeleBot(TOKEN)
set_channel = ''
img1 = open('penalty.png', 'rb')

markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
goal = types.KeyboardButton('УДАРИТЬ')
markup1.add(goal)

markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
udar1 = types.KeyboardButton('1')
udar2 = types.KeyboardButton('2')
udar3 = types.KeyboardButton('3')
udar4 = types.KeyboardButton('4')
home = types.KeyboardButton('Домой🥅')
udar5 = types.KeyboardButton('5')
markup2.add(udar1, udar2, udar3, udar4, home, udar5)

Media = """Автор бота. Обратная связь!
discord server: https://discord.gg/eem2NNKa6G
tg: @paulhowever
web-site: http://a0836219.xsph.ru/
"""
