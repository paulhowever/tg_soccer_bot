from const import *
import random
import telebot
from telebot import types
from telebot.apihelper import ApiTelegramException
from markups import *
from moderacia import *
from const import *
import time
import sqlite3

# Инициализация базы данных
conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()

# Создание таблицы, если её нет
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                  (user_id TEXT PRIMARY KEY)''')
conn.commit()

# Функция для получения всех пользователей
def get_joined_users():
    cursor.execute("SELECT user_id FROM users")
    return {row[0] for row in cursor.fetchall()}

joinedUsers = get_joined_users()

@bot.message_handler(commands=['start'])
def start(message):
    if bot.get_chat_member(chat_id=my_channel_id, user_id=message.from_user.id).status != 'left':
        bot.send_message(message.chat.id, text_start, reply_markup=markup1)
    else:
        bot.send_message(message.chat.id, "Подпишись на канал {} для продолжения".format(set_channel))
    
    user_id = str(message.chat.id)
    if user_id not in joinedUsers:
        try:
            cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
            conn.commit()
            joinedUsers.add(user_id)
        except sqlite3.IntegrityError:
            pass  # Пользователь уже существует

@bot.message_handler(commands=['phelp'])
def help(message):
    cursor.execute("SELECT user_id FROM users")
    users = cursor.fetchall()
    for user in users:
        try:
            bot.send_message(user[0], 'ura robit')
        except ApiTelegramException as e:
            if e.description == "Forbidden: bot was blocked by the user":
                print(f"User {user[0]} blocked the bot")

@bot.message_handler(commands=['help'])
def phelp(message):
    bot.send_message(chat_id=message.chat.id, text=f'Проблемы с ботом/Хочешь такой же? {Media}')

@bot.message_handler(commands=['send_uved'])
def mess(message):
    if bot.get_chat_member(chat_id=my_channel_id, user_id=message.from_user.id).status in ['creator', 'administrator']:
        cursor.execute("SELECT user_id FROM users")
        for user in cursor.fetchall():
            try:
                bot.send_message(user[0], message.text[message.text.find(' '):])
                with open('ronaldo_reklama.jpg', 'rb') as photo:
                    bot.send_photo(user[0], photo)
            except ApiTelegramException as e:
                if e.description == "Forbidden: bot was blocked by the user":
                    print(f"User {user[0]} blocked the bot")

@bot.message_handler(content_types=['text'])
def text(message):
    if message.text == 'УДАРИТЬ🥅':
        def goal(message):
            if message.text in ['1', '2', '3', '4', '5']:
                if random.choice([0, 100]) not in list(range(22)):
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
    elif message.text == 'Открыть Пак😉':
            global tm
            if float(time.time()) - float(tm) > 3600.0:
                number_hero = random.randint(0, 100)
                try:
                    with open(f'{draft[number_hero]}', 'rb') as g1:
                        bot.send_photo(message.chat.id, g1)
                    bot.send_message(message.chat.id, f'Вам выпал игрок ^^^^^^^')
                except:
                    with open('unlucky.png', 'rb') as l1:
                        bot.send_photo(message.chat.id, l1)
                    bot.send_message(message.chat.id, 'Вам не повезло :(')
                tm = time.time()
            else:
                bot.send_message(message.chat.id, f'До следующего открытия пака осталось -- {(tm + 3600.0 - time.time())//60} минут')
    elif message.text == 'root' and bot.get_chat_member(chat_id=my_channel_id, user_id=message.from_user.id).status in ['creator', 'administrator']:
        tm = 0
    else:
        bot.send_message(message.chat.id, 'Я вас не понял(')

if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    finally:
        conn.close()  # Закрываем соединение с БД при завершении работы
