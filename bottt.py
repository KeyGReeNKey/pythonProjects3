import telebot
import sqlite3
from datetime import datetime
from telebot import types

bot = telebot.TeleBot('6963860320:AAHhJo4WB-y6zzfPm2BSmby8rQw9VflMiYs')


@bot.message_handler(commands=['start'])
def start(message):
    marcap = types.InlineKeyboardMarkup()
    marcap.add(types.InlineKeyboardButton('Добавить дело', callback_data='add'))
    marcap.add(types.InlineKeyboardButton('Удалить дело', callback_data='delete'))
    marcap.add(types.InlineKeyboardButton('Вывести дела на сегодня', callback_data='all'))
    marcap.add(types.InlineKeyboardButton('Закончить все дела на сегодня', callback_data='alldell'))
    marcap.add(types.InlineKeyboardButton('покажи картинку', callback_data='photo'))
    bot.send_message(message.chat.id, 'Что бы ты хотел сделать?', reply_markup=marcap)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'add':
        bot.send_message(callback.message.chat.id, 'Введите дело для добавления:')
        bot.register_next_step_handler(callback.message, add_affair)
    elif callback.data == 'delete':
        bot.send_message(callback.message.chat.id, 'Введите ID дела для удаления:')
        bot.register_next_step_handler(callback.message, delete_affair)
    elif callback.data == 'alldell':
        delete_all_affairs(callback.message)
    elif callback.data == 'all':
        show_today_affairs(callback.message)
    elif callback.data == 'photo':
        bot.send_message(callback.message.chat.id, 'напишите номер картинки:')
        bot.register_next_step_handler(callback.message, photo)

def photo (message):
    photo = open('Cold.jpg', 'rb')
    bot.send_photo(message.chat.id, photo)

def delete_all_affairs(message):
    conn = sqlite3.connect('Do_todey.db')
    cur = conn.cursor()
    cur.execute('DELETE FROM affairs')
    conn.commit()
    bot.send_message(message.chat.id, 'Все дела успешно удалены из базы данных.')


def add_affair(message):
    conn = sqlite3.connect('Do_todey.db')
    cur = conn.cursor()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS affairs (id INTEGER PRIMARY KEY AUTOINCREMENT, description TEXT, created_at TEXT)')
    conn.commit()
    cur.execute('INSERT INTO affairs (description, created_at) VALUES (?, ?)',
                [message.text, datetime.now().strftime('%Y-%m-%d')])
    conn.commit()
    bot.send_message(message.chat.id, 'Дело успешно добавлено в базу данных.')


def delete_affair(message):
    conn = sqlite3.connect('Do_todey.db')
    cur = conn.cursor()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS affairs (id INTEGER PRIMARY KEY AUTOINCREMENT, description TEXT, created_at TEXT)')
    conn.commit()
    cur.execute('DELETE FROM affairs WHERE id = ?', [message.text])
    conn.commit()
    bot.send_message(message.chat.id, 'Дело успешно удалено из базы данных.')


def show_today_affairs(message):
    conn = sqlite3.connect('Do_todey.db')
    cur = conn.cursor()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS affairs (id INTEGER PRIMARY KEY AUTOINCREMENT, description TEXT, created_at TEXT)')
    conn.commit()
    cur.execute('SELECT description FROM affairs WHERE created_at = ?', [datetime.now().strftime('%Y-%m-%d')])
    rows = cur.fetchall()
    if rows:
        today_affairs = '\n'.join([row[0] for row in rows])
        bot.send_message(message.chat.id, f'Дела на сегодня:\n{today_affairs}')
    else:
        bot.send_message(message.chat.id, 'На сегодня нет добавленных дел.')


bot.polling()
