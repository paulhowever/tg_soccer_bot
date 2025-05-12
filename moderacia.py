from const import *
needHelp = []

@bot.message_handler(commands=['support'])
def support(message):
    needHelpFile = open('needHelp.txt', 'a')
    if message.chat.id > 0:
        needHelpFile.write(str(message.chat.id) + "\n" + str(message.chat.first_name) + "\n")
    else:
        needHelpFile.write(str(message.chat.id) + "\n" + str(message.chat.title) + "\n")
    needHelpFile.close()
    supportFile = open('support.txt', 'r')
    supportTeam = set()
    for line in supportFile:
        supportTeam.add(line.strip())
    supportFile.close()
    def get_problem(message):
        for user in supportTeam:
            if message.chat.id > 0 and not any(word in message.text for word in ['/help', '/support', '/start', 'УДАРИТЬ🥅', 'Открыть Пак😉']):
                bot.send_message(int(user), str(message.chat.id) + " (" + message.chat.first_name + "): " + message.text)
            elif message.chat.id < 0 and not any(word in message.text for word in ['/help', '/support', '/start', 'УДАРИТЬ🥅', 'Открыть Пак😉']):
                bot.send_message(int(user), str(message.chat.id) + " (" + message.chat.title + "): " + message.text)
        bot.send_message(message.chat.id,'"Подождите немного, {0.first_name}! Мы отправили ваше сообщение разработчику! \n Пожалуйста, больше не отправляйте сообщения. \n Вы находитесь в очереди."'.format(message.from_user), parse_mode='html')
    bot.send_message(message.chat.id, 'Опишите вашу проблему')
    bot.register_next_step_handler(message, get_problem)
@bot.message_handler(commands=['answer'])
def answer(message):
    supportFile = open('support.txt', 'r')
    supportTeam = set()
    for line in supportFile:
        supportTeam.add(line.strip())
    supportFile.close()
    if str(message.chat.id) in supportTeam:
        needHelp = []
        needHelpFile = open('needHelp.txt', 'r')
        for line in needHelpFile:
            needHelp.append(line.strip())
        needHelpFile.close()
        for user in supportTeam:
            if message.chat.id > 0:
                bot.send_message(user, str(message.chat.id) + '(' + message.chat.first_name + ') Answering to ' + needHelp[0] + ' (' + needHelp[1] + '): ' + message.text[message.text.find(' '):].format(message.from_user), parse_mode='html')
            else:
                bot.send_message(user, str(message.chat.id) + '(' + message.chat.title + ') Answering to ' + needHelp[0] + ' (' + needHelp[1] + '): ' + message.text[message.text.find(' '):].format(message.from_user),parse_mode='html')
        bot.send_message(needHelp[0], text='Вам отвечает модерация Live ИГРЫ: ' + message.text[message.text.find(' '):].format(message.from_user),parse_mode='html')
        with open('needHelp.txt', 'r') as nhf:
            lines = nhf.readlines()
        with open('needHelp.txt', 'w') as nhf:
            for line in lines:
                if line.strip("\n") != needHelp[0] and line.strip('\n') != needHelp[1]:
                    nhf.write(line)
    else:
        bot.send_message(message.chat.id, 'You do not have permission to answer'.format(message.from_user), parse_mode='html')