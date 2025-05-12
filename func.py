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



