import telebot
from telebot import types
import db

token = '1303608144:AAH09kqBe4ahjau7lUKbx6kibiyK2QyvAXk'
qb = telebot.TeleBot(token)
# db = db.Sqlither('db.db')
all_data = {'last_order_id': 0, 'counts': 0}


markup = types.ReplyKeyboardMarkup(True)  # основная клавиатура, присылается по команде /start
item1 = types.KeyboardButton('Корзина')
item2 = types.KeyboardButton('Каталог')
item3 = types.KeyboardButton('Помощь')
item4 = types.KeyboardButton('Оформление заказа')
markup.add(item1, item2, item3, item4)

markup1 = types.InlineKeyboardMarkup(row_width=3)  # меню TIE типа
but1 = types.InlineKeyboardButton('TIE-fighter', callback_data='tie1')
but2 = types.InlineKeyboardButton('TIE-defender', callback_data='tie2')
but3 = types.InlineKeyboardButton('TIE-interceptor', callback_data='tie3')
but4 = types.InlineKeyboardButton('Мне не подходит ничего из выше предложенного', callback_data='no')
markup1.add(but1, but2, but3, but4)

@qb.message_handler(commands=['start'])
def welcome(message):
    if (not db.Sqlither.user_exists(self=True, user_id=message.from_user.id)):
        db.Sqlither.add_user(self=True, user_id=message.from_user.id, order_id=all_data['last_order_id'])
        qb.send_message(message.from_user.id, 'Добро пожаловать! Будем знакомы, я - Эрик.', reply_markup=markup)
        all_data['last_order_id'] += 1
        print(all_data['last_order_id'])
    else:
        qb.send_message(message.from_user.id, 'Эй, привет! Я тебя знаю', reply_markup=markup)
        print(2)

@qb.message_handler(commands=['test'])
def testing(message):
    res = db.Sqlither.get_order_id(self=True, user_id=message.from_user.id)
    print(res)


def set_count(message):
    all_data['counts'] = message.text
    # print(all_data['counts'])
    u_id = db.Sqlither.get_order_id(self=True, user_id=message.from_user.id)
    print('u_id = % s' % u_id)
    # db.Sqlither.add_fighter(self=True, order_id=0, count=int(all_data['counts']))




@qb.message_handler(content_types=['text'])
def reactions(message):
    if message.text == 'Корзина':
        qb.send_message(message.from_user.id, 'Эта функция пока не работает')

    if message.text == 'Каталог':
        qb.send_message(message.from_user.id, '...', reply_markup=markup1)

    if message.text == 'Помощь':
        qb.send_message(message.from_user.id, 'Эта функция пока не работает')

    if message.text == 'Оформление заказа':
        qb.send_message(message.from_user.id, 'Эта функция пока не работает')


@qb.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'tie1':
                send = qb.send_message(call.message.chat.id, 'Введите необходимое количество товара: ')
                qb.register_next_step_handler(send, set_count)



    except Exception as e:
        print(repr(e))


qb.polling(none_stop=True, interval=0)