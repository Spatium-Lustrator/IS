'''
Сделать оформление заказа:
Пользователь нажал на кнопку >>> бот предлагает места выдачи >>> пользователь выбирает, ответ сохраняется в БД >>>
>> подтверждение заказа >>> новый order_id, соответсвующие записи в БД
Добавить функцию для кассира:
Когда заказ доставлен, он с помощью команды поставит статус "доставлено"
'''
import telebot
from telebot import types
import db

token = '1303608144:AAH09kqBe4ahjau7lUKbx6kibiyK2QyvAXk'
zero = 0
qb = telebot.TeleBot(token)
all_data = {'last_order_id': 0, 'counts': 0, 'now_id': None, 'now_prod': None}
product_data = {'tie_fig': {'beat_name': 'TIE-fighter', 'price': 500, 'desc': 'Обычный истребитель'},
                'tie_def': {'beat_name': 'TIE-defender', 'price': 500, 'desc': 'Улучшенный истребитель, проект предложен гранд-адмиралом Трауном'},
                'tie_int': {'beat_name': 'TIE-intereceptor', 'price': 500, 'desc': 'Резвый истребитель в Ваши ряды!'}}


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

setstat_markup = types.InlineKeyboardMarkup(row_width=2)
but5 = types.InlineKeyboardButton('Заказ доставлен', callback_data='deliver')
but6 = types.InlineKeyboardButton('Клиент забрал заказ', callback_data='carry')
setstat_markup.add(but5, but6)

adresses_markup = types.InlineKeyboardMarkup(row_width=2)
but5 = types.InlineKeyboardButton('Татуин, Мос Эйсли, пл. №14', callback_data='deliver')
but6 = types.InlineKeyboardButton('Корусант, Бывший Храм Джедаев, пл. №3', callback_data='deliver')
but7 = types.InlineKeyboardButton('Лотал, столица, пл. №9', callback_data='deliver')

@qb.message_handler(commands=['start']) #
def welcome(message):
    if (not db.Sqlither.user_exists(self=True, user_id=message.from_user.id)):
        db.Sqlither.add_user(self=True, user_id=message.from_user.id, order_id=all_data['last_order_id'],
                             paid=False, delivered=False, carried=False,
                             tie_def=0, tie_int=0, tie_fig=0)
        all_data['last_order_id'] += 1
        print()
        qb.send_message(message.from_user.id, 'Добро пожаловать! Будем знакомы, я - Эрик.', reply_markup=markup)
    else:
        qb.send_message(message.from_user.id, 'Эй, привет! Я тебя знаю', reply_markup=markup)
        all_data['last_order_id'] += 1

@qb.message_handler(commands=['test'])
def testing(message):
    res = db.Sqlither.get_order_id(self=True, user_id=message.from_user.id)
    print(res)

def setstat2(message):
    all_data['now_id'] = message.text
    qb.send_message(message.from_user.id, 'Какой статус Вы хотите добавить?', reply_markup=setstat_markup)

def delivered(message):
    print('yo1')
    db.Sqlither.delivered(self=True, user_id=all_data['now_id'], deliv=True)
    print('yo2')
    qb.send_message(all_data['now_id'], 'Заказ с идентификатором %s!' % db.ad['nci'])
    # qb.send_message(all_data['now_id'], 'Вы только посмотрите! Ваш заказ с идентификатором "%s" доставлен'
    #                % all_data['now_id'])
    all_data['now_id'] = None


def set_count(message):
    all_data['counts'] = message.text
    print(all_data['counts'])
    if all_data['now_prod'] == 'tie_fig':
        db.Sqlither.add_fighter(self=True, user_id=message.from_user.id, count=int(all_data['counts']))

    elif all_data['now_prod'] == 'tie_def':
        db.Sqlither.add_defender(self=True, user_id=message.from_user.id, count=int(all_data['counts']))

    elif all_data['now_prod'] == 'tie_int':
        db.Sqlither.add_interceptor(self=True, user_id=message.from_user.id, count=int(all_data['counts']))

    all_data['counts'] = None
    all_data['now_prod'] = None


@qb.message_handler(commands=['setstat'])
def setstat(message):
    if db.Sqlither.check_workers(self=True, user_id=message.from_user.id):
        send = qb.send_message(message.from_user.id, 'Рад видеть тебя! Введи идентификатор заказа: ')
        qb.register_next_step_handler(send, setstat2)



@qb.message_handler(content_types=['text'])
def reactions(message):
    if message.text == 'Корзина':
        db.Sqlither.basket(self=True, user_id=message.from_user.id)
        if db.basket['empty'] == False:
            qb.send_message(message.from_user.id, 'Ваша корзина не пуста')
            couel = len(db.basket1)
            for x in range(0, couel):
                qb.send_message(message.from_user.id, '%s. %s * %s\n'
                                                      'Итого за %s: %s' % (x+1, product_data[db.basket1[x]]['beat_name'],
                                                                       db.basket[db.basket1[x]], product_data[db.basket1[x]]['beat_name'],
                                                                           product_data[db.basket1[x]]['price']*db.basket[db.basket1[x]]))

        elif db.basket['empty'] == True:
            qb.send_message(message.from_user.id, 'Ваша корзина пуста')


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
                all_data['now_prod'] = 'tie_fig'
                qb.register_next_step_handler(send, set_count)

            if call.data == 'deliver':
                print('yo')
                #all_data['now_id'] = call.message
                all_data['now_id'] = call.message.chat.id
                delivered(call.message)

            if call.data == 'carry':
                pass



    except Exception as e:
        print(repr(e))


qb.polling(none_stop=True, interval=0)