from const import *
import sqlite3

# Инициализация базы данных
conn = sqlite3.connect('support.db', check_same_thread=False)
cursor = conn.cursor()

# Создание таблиц, если их нет
cursor.execute('''CREATE TABLE IF NOT EXISTS support_team
                  (user_id TEXT PRIMARY KEY)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS help_requests
                  (chat_id TEXT PRIMARY KEY,
                   name TEXT,
                   problem TEXT)''')
conn.commit()

@bot.message_handler(commands=['support'])
def support(message):
    # Добавляем запрос в базу данных
    if message.chat.id > 0:
        name = message.chat.first_name
    else:
        name = message.chat.title
    
    try:
        cursor.execute("INSERT INTO help_requests (chat_id, name) VALUES (?, ?)", 
                      (str(message.chat.id), name))
        conn.commit()
    except sqlite3.IntegrityError:
        # Если запрос уже существует, обновляем имя
        cursor.execute("UPDATE help_requests SET name = ? WHERE chat_id = ?", 
                      (name, str(message.chat.id)))
        conn.commit()

    def get_problem(message):
        # Обновляем запрос с описанием проблемы
        cursor.execute("UPDATE help_requests SET problem = ? WHERE chat_id = ?", 
                      (message.text, str(message.chat.id)))
        conn.commit()
        
        # Отправляем сообщение команде поддержки
        cursor.execute("SELECT user_id FROM support_team")
        support_team = cursor.fetchall()
        
        for user in support_team:
            user_id = int(user[0])
            if message.chat.id > 0:
                msg_text = f"{message.chat.id} ({message.chat.first_name}): {message.text}"
            else:
                msg_text = f"{message.chat.id} ({message.chat.title}): {message.text}"
            
            try:
                bot.send_message(user_id, msg_text)
            except ApiTelegramException as e:
                if e.description == "Forbidden: bot was blocked by the user":
                    print(f"Support team member {user_id} blocked the bot")

        bot.send_message(message.chat.id, 
                       f"Подождите немного, {message.from_user.first_name}! Мы отправили ваше сообщение разработчику!\n"
                       "Пожалуйста, больше не отправляйте сообщения.\n"
                       "Вы находитесь в очереди.",
                       parse_mode='html')

    bot.send_message(message.chat.id, 'Опишите вашу проблему')
    bot.register_next_step_handler(message, get_problem)

@bot.message_handler(commands=['answer'])
def answer(message):
    # Проверяем, есть ли пользователь в команде поддержки
    cursor.execute("SELECT 1 FROM support_team WHERE user_id = ?", (str(message.chat.id),))
    is_support = cursor.fetchone()
    
    if is_support:
        # Получаем первый запрос в очереди
        cursor.execute("SELECT chat_id, name FROM help_requests ORDER BY rowid LIMIT 1")
        request = cursor.fetchone()
        
        if request:
            chat_id, name = request
            answer_text = message.text[message.text.find(' '):].strip()
            
            # Отправляем ответ команде поддержки
            cursor.execute("SELECT user_id FROM support_team")
            support_team = cursor.fetchall()
            
            for user in support_team:
                user_id = int(user[0])
                if message.chat.id > 0:
                    msg_text = (f"{message.chat.id} ({message.chat.first_name}) отвечает {chat_id} ({name}): "
                              f"{answer_text}")
                else:
                    msg_text = (f"{message.chat.id} ({message.chat.title}) отвечает {chat_id} ({name}): "
                              f"{answer_text}")
                
                try:
                    bot.send_message(user_id, msg_text, parse_mode='html')
                except ApiTelegramException:
                    continue
            
            # Отправляем ответ пользователю
            try:
                bot.send_message(int(chat_id), 
                               f"Вам отвечает модерация Live ИГРЫ: {answer_text}",
                               parse_mode='html')
            except ApiTelegramException as e:
                if e.description == "Forbidden: bot was blocked by the user":
                    print(f"User {chat_id} blocked the bot")
            
            # Удаляем обработанный запрос
            cursor.execute("DELETE FROM help_requests WHERE chat_id = ?", (chat_id,))
            conn.commit()
        else:
            bot.send_message(message.chat.id, "Нет активных запросов на поддержку")
    else:
        bot.send_message(message.chat.id, "У вас нет прав для ответа на запросы", parse_mode='html')
