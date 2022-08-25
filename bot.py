import sqlite3
import telebot
from telebot import types

API_TOKEN = '5443440197:AAF5ssvLRdO5xhNdVu-ne6Hzzb_TVZRpW8s'
DB_FILE_NAME = 'dbFin.sqlite'


def create_connect():
    return sqlite3.connect(DB_FILE_NAME)


def init_db():
    # Создание базы и таблицы
    with create_connect() as connect:
        connect.execute('''
            CREATE TABLE IF NOT EXISTS Message (
                id      INTEGER  PRIMARY KEY,
                user_id INTEGER  NOT NULL,
                nazvanie    TEXT  NOT NULL,
                deviz   TEXT  NOT NULL
            );
        ''')

        connect.commit()


def add_message(user_id, message, message1):
    with create_connect() as connect:
        connect.execute(
            'INSERT INTO Message (user_id, nazvanie, deviz) VALUES (?, ?, ?)', (user_id, message, message1)
        )
        connect.commit()


init_db()


bot = telebot.TeleBot(API_TOKEN)
z = []

@bot.message_handler(commands="start")
def start(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Новая Идея!")
    markup.add(item1)
    bot.send_message(message.chat.id, "Привет 👋\n\nТут ты можешь предложить идею как назвать новое объединение РДДМ 😎 \n\nНажми кнопку - Новая идея!", reply_markup=markup)

@bot.message_handler(content_types=["text"])
def command(message):
    if message.text == "Новая Идея!":
        msg = bot.send_message(message.chat.id, "Напиши придуманное название 🤔")
        bot.register_next_step_handler(msg, txt)
def txt(message):
    nazvanie = message.text
    z.append(nazvanie)
    bot.reply_to(message, "Записал 😊")
    msg = bot.send_message(message.chat.id, "А теперь напиши кричалку к данному названию 🤔")
    bot.register_next_step_handler(msg, txt1)
def txt1(message):
    deviz = message.text
    bot.send_message(message.chat.id, "Обрабатываю 🤖")
    user_id = message.from_user.id
    nazvanie = z[0]
    add_message(user_id, nazvanie, deviz)
    # ^^^^^^^^^^^^^^^^^
    bot.reply_to(message, "Записал 😊")
# bot.polling()
bot.infinity_polling()
