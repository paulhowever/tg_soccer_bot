import telebot
from telebot import types
from func import *
import random

@bot.message_handler(commands=['start'])
def start(message):
    if bot.get_chat_member(chat_id=my_channel_id, user_id=message.from_user.id).status != 'left':
            bot.send_message(message.chat.id, "Нажмите на кнопку 'УДАРИТЬ', чтобы запустить игру!", reply_markup=markup1)
    else:
        bot.send_message(message.chat.id, "Подпишись на канал {} для продолжения".format(set_channel))

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(chat_id=message.chat.id, text=f'Проблемы с ботом/Хочешь такой же? {Media}')



@bot.message_handler(content_types=['text'])
def text(message):
    if message.text == 'УДАРИТЬ':
        def goal(message):
            if message.text in ['1', '2', '3', '4', '5']:
                if random.choice([0, 100]) not in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]:
                    with open('zabili.png', 'rb') as f1:
                        bot.send_photo(message.chat.id, f1)
                    bot.send_message(message.chat.id, '''Вы забили гол! Вы молодец!''')
                    bot.register_next_step_handler(message, goal)
                else:
                    with open('goal_nezabit.png', 'rb') as f:
                        bot.send_photo(message.chat.id, f)
                    bot.send_message(message.chat.id, '''Промах! Вы не забили гол! Попробуйте еще раз!''')
                    bot.register_next_step_handler(message, goal)
            else:
                text(message)
        with open('penalty.png', 'rb') as f3:
            bot.send_photo(message.chat.id, f3)
        bot.send_message(message.chat.id, 'Выберите куда хотите ударить! (нажмите на соответствующую кнопку)', reply_markup=markup2)
        bot.register_next_step_handler(message, goal)
    elif message.text == 'Домой🥅':
        start(message)
    else:
        bot.send_message(message.chat.id, 'Я вас не понял(')




bot.polling(none_stop=True)
