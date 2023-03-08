import telebot
from telebot import types
import time
import psycopg2
import emoji
import random

week = ('понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота')
lessons_time = (('1', '09.30-11.05'),
                ('2', '11.20-12.55'),
                ('3', '13.10-14.45'),
                ('4', '15.25-17.00'),
                ('5', '17.15-18.50'))
rock = emoji.emojize('Камень :raised_fist:')
scissors = emoji.emojize('Ножницы :victory_hand:')
paper = emoji.emojize('Бумага :raised_hand:')
rps = (rock, paper, scissors)

this_week = (time.localtime().tm_yday-30) // 7 + 1
db_this_week = str(((time.localtime().tm_yday-30) // 7 + 1) % 2)
db_next_week = '2'
if db_this_week == '0':
    db_this_week = '2'
    db_next_week = '1'

token = "6260080511:AAGO5KHxpp9GDBCxw3XYw_6H0qGYWFjIb1s"

bot = telebot.TeleBot(token)

conn = psycopg2.connect(database="Telegram_bot",
                        user="postgres",
                        password="2022",
                        host="localhost",
                        port="5432")

cursor = conn.cursor()

on_day = "SELECT timetable.subject, timetable.subject_type, full_name, room_numb " \
        "FROM timetable, teacher " \
        "WHERE timetable.week = %s " \
        "AND timetable.day = %s " \
        "AND timetable.study_time = %s " \
        "AND timetable.subject = teacher.subject " \
        "AND timetable.subject_type = teacher.subject_type"

help_text = 'Список комманд:\n' \
            '/start - включение стартовой клавиатуры с командами\n' \
            '/mtuci - ссылка на официальный сайт МТУСИ\n' \
            '/week - определение текущей недели\n' \
            '/days - смена клавиатуры на дни текущей недели\n' \
            '/game - игра "камень-ножницы-бумага"\n' \
            '/back - возврат к стартовой клавиатуре"\n' \
            '-----------------------------------\n' \
            'Список ключевых слов\n' \
            'Расписание на текущую неделю\n' \
            'Расписание на следующую неделю\n' \
            'Сегодня\n' \
            'Завтра\n' \
            'Понедельник\n' \
            'Вторник\n' \
            'Среда\n' \
            'Четверг\n' \
            'Пятница\n' \
            'Суббота\n' + str(rock) + '\n' + str(scissors) + '\n' + str(paper)


@bot.message_handler(commands=['start', 'back'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("/help", "/mtuci", "/week")
    keyboard.row("/days", "/game")
    keyboard.row("Расписание на текущую неделю", "Расписание на следующую неделю")
    keyboard.row("Сегодня", "Завтра")
    bot.send_message(message.chat.id, 'Для ознакомления с командами пропишите /help', reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, help_text)


@bot.message_handler(commands=['mtuci'])
def start_message(message):
    bot.send_message(message.chat.id, 'Официальный сайт МТУСИ: https://mtuci.ru/')


@bot.message_handler(commands=['week'])
def start_message(message):
    if this_week % 2 == 1:
        output = 'Сейчас верхняя неделя (' + str(this_week) + ' по счету)'
    else:
        output = 'Сейчас нижняя неделя (' + str(this_week) + ' по счету)'
    bot.send_message(message.chat.id, output)


@bot.message_handler(commands=['days'])
def day_list(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("Понедельник", "Вторник")
    keyboard.row("Среда", "Четверг")
    keyboard.row("Пятница", "Суббота")
    keyboard.row("/back")
    bot.send_message(message.chat.id, 'Для возврата пропишите /back', reply_markup=keyboard)


@bot.message_handler(commands=['game'])
def day_list(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row(rock)
    keyboard.row(paper)
    keyboard.row(scissors)
    keyboard.row("/back")
    bot.send_message(message.chat.id, 'Для возврата пропишите /back', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text.lower() in week:
        this_day = message.text.lower().title()
        output = this_day
        for lesson in lessons_time:
            lesson_time = lesson[1]
            cursor.execute(on_day, (db_this_week, this_day, lesson_time))
            records = list(cursor.fetchall())
            if records:
                output += '\n------------------------------'
                output += '                                                                        \n'
                output += lesson[0] + '. ' + lesson_time + '\n'
                output += records[0][0] + '\n'
                output += records[0][1] + ' (' + records[0][3] + ')\n'
                output += records[0][2]
            else:
                output += '\n------------------------------'
                output += '                                                                        \n'
                output += lesson[0] + '. Занятия нет'
        bot.send_message(message.chat.id, output)
    elif message.text.lower() == "расписание на текущую неделю":
        for day in week:
            this_day = day.title()
            output = this_day
            for lesson in lessons_time:
                lesson_time = lesson[1]
                cursor.execute(on_day, (db_this_week, this_day, lesson_time))
                records = list(cursor.fetchall())
                if records:
                    output += '\n------------------------------'
                    output += '                                                                        \n'
                    output += lesson[0] + '. ' + lesson_time + '\n'
                    output += records[0][0] + '\n'
                    output += records[0][1] + ' (' + records[0][3] + ')\n'
                    output += records[0][2]
                else:
                    output += '\n------------------------------'
                    output += '                                                                        \n'
                    output += lesson[0] + '. Занятия нет'
            bot.send_message(message.chat.id, output)
    elif message.text.lower() == "расписание на следующую неделю":
        for day in week:
            this_day = day.title()
            output = this_day
            for lesson in lessons_time:
                lesson_time = lesson[1]
                cursor.execute(on_day, (db_next_week, this_day, lesson_time))
                records = list(cursor.fetchall())
                if records:
                    output += '\n------------------------------'
                    output += '                                                                        \n'
                    output += lesson[0] + '. ' + lesson_time + '\n'
                    output += records[0][0] + '\n'
                    output += records[0][1] + ' (' + records[0][3] + ')\n'
                    output += records[0][2]
                else:
                    output += '\n------------------------------'
                    output += '                                                                        \n'
                    output += lesson[0] + '. Занятия нет'
            bot.send_message(message.chat.id, output)
    elif message.text.lower() == "сегодня":
        wday = time.localtime().tm_wday
        if wday == 6:
            bot.send_message(message.chat.id, "Сегодня воскресенье")
        else:
            this_day = week[wday].title()
            output = this_day
            for lesson in lessons_time:
                lesson_time = lesson[1]
                cursor.execute(on_day, (db_this_week, this_day, lesson_time))
                records = list(cursor.fetchall())
                if records:
                    output += '\n------------------------------'
                    output += '                                                                        \n'
                    output += lesson[0] + '. ' + lesson_time + '\n'
                    output += records[0][0] + '\n'
                    output += records[0][1] + ' (' + records[0][3] + ')\n'
                    output += records[0][2]
                else:
                    output += '\n------------------------------'
                    output += '                                                                        \n'
                    output += lesson[0] + '. Занятия нет'
            bot.send_message(message.chat.id, output)
    elif message.text.lower() == "завтра":
        wday = (time.localtime().tm_wday + 1) % 7
        if wday == 6:
            bot.send_message(message.chat.id, "Завтра воскресенье")
        else:
            this_day = week[wday].title()
            output = this_day
            for lesson in lessons_time:
                lesson_time = lesson[1]
                if wday == 0:
                    cursor.execute(on_day, (db_next_week, this_day, lesson_time))
                else:
                    cursor.execute(on_day, (db_this_week, this_day, lesson_time))
                records = list(cursor.fetchall())
                if records:
                    output += '\n------------------------------'
                    output += '                                                                        \n'
                    output += lesson[0] + '. ' + lesson_time + '\n'
                    output += records[0][0] + '\n'
                    output += records[0][1] + ' (' + records[0][3] + ')\n'
                    output += records[0][2]
                else:
                    output += '\n------------------------------'
                    output += '                                                                        \n'
                    output += lesson[0] + '. Занятия нет'
            bot.send_message(message.chat.id, output)
    elif message.text in rps:
        player_choice = message.text
        bot_choice = random.choice(rps)
        output = ''
        if player_choice == bot_choice:
            output = 'У меня тоже ' + bot_choice.lower() + ', ничья'
        elif player_choice == rock:
            if bot_choice == paper:
                output = 'У меня ' + bot_choice.lower() + ',вы проиграли'
            else:
                output = 'Вы победили, у меня ' + bot_choice.lower()
        elif player_choice == paper:
            if bot_choice == scissors:
                output = 'У меня ' + bot_choice.lower() + ',вы проиграли'
            else:
                output = 'Вы победили, у меня ' + bot_choice.lower()
        elif player_choice == scissors:
            if bot_choice == rock:
                output = 'У меня ' + bot_choice.lower() + ',вы проиграли'
            else:
                output = 'Вы победили, у меня ' + bot_choice.lower()
        bot.send_message(message.chat.id, output)

    else:
        bot.send_message(message.chat.id, 'Извините, я Вас не понимаю')


bot.polling(none_stop=True, interval=0)
