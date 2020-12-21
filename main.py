import telebot
from telebot import types
import db
import oplata
import sqlite3

first_prod = None
token = '1301756828:AAF3FjdaW20t2gL3nIl2dqvtQfM4T0Mc0Lg'
zero = 0
qb = telebot.TeleBot(token)

all_data1 = {'1': 'tie_fig', '2': 'tie_def', '3': 'tie_int', 'now_id': 1}

all_data = {'last_order_id': 0, 'counts': 0, 'now_id': None, 'now_prod': None, 'now_price': None, 'now_del': None,
            'mesid': None}

place = {1: 'Татуин, Мос Эйсли, пл. №14',
         2: 'Корусант, Бывший Храм Джедаев, пл. №3',
         3: 'Лотал, столица, пл. №9'}

product_data = {'tie_fig': {'beat_name': 'TIE-fighter', 'price': 500, 'desc': 'TIE-fighter: Обычный истребитель'},
                'tie_def': {'beat_name': 'TIE-defender', 'price': 600, 'desc': 'TIE-defender: Улучшенный истребитель, проект предложен гранд-адмиралом Трауном'},
                'tie_int': {'beat_name': 'TIE-intereceptor', 'price': 650, 'desc': 'TIE-intereceptor: Резвый истребитель в Ваши ряды!'}}


markup = types.ReplyKeyboardMarkup(True)  # основная клавиатура, присылается по команде /start
item1 = types.KeyboardButton('Корзина')
item2 = types.KeyboardButton('Каталог')
item3 = types.KeyboardButton('Контакты')
item4 = types.KeyboardButton('Оформление заказа')
markup.add(item1, item2, item3, item4)

markup1 = types.InlineKeyboardMarkup(row_width=3)  # меню TIE типа
but1 = types.InlineKeyboardButton('TIE-fighter', callback_data='tie1')
but2 = types.InlineKeyboardButton('TIE-defender', callback_data='tie2')
but3 = types.InlineKeyboardButton('TIE-interceptor', callback_data='tie3')
but4 = types.InlineKeyboardButton('Мне не подходит ничего из выше предложенного', callback_data='no')
bu5 = types.InlineKeyboardButton('>>>', callback_data='>')
bu6 = types.InlineKeyboardButton('<<<', callback_data='<')
markup1.add(but1, but2, but3, bu6, bu5)

setstat_markup = types.InlineKeyboardMarkup(row_width=2)
but5 = types.InlineKeyboardButton('Заказ доставлен', callback_data='deliver')
but6 = types.InlineKeyboardButton('Клиент забрал заказ', callback_data='carry')
setstat_markup.add(but5, but6)

adresses_markup = types.InlineKeyboardMarkup(row_width=2)
butt5 = types.InlineKeyboardButton('Татуин, Мос Эйсли, пл. №14', callback_data='place1')
but6 = types.InlineKeyboardButton('Корусант, Бывший Храм Джедаев, пл. №3', callback_data='place2')
but7 = types.InlineKeyboardButton('Лотал, столица, пл. №9', callback_data='place3')
adresses_markup.add(butt5, but6, but7)

delete_markup = types.InlineKeyboardMarkup(row_width=2)
delete_markup1 = types.InlineKeyboardMarkup(row_width=2)
delete_markup2 = types.InlineKeyboardMarkup(row_width=2)
del1 = types.InlineKeyboardButton('-первый элемент в кол-ве:', callback_data='del1')
del2 = types.InlineKeyboardButton('-второй элемент в кол-ве:', callback_data='del2')
del3 = types.InlineKeyboardButton('-третий элемент в кол-ве:', callback_data='del3')
del_all = types.InlineKeyboardButton('Очистить корзину', callback_data='delall')
delete_markup.add(del1)
delete_markup1.add(del1, del2, del_all)
delete_markup2.add(del1, del2, del3,  del_all)

check_markup = types.InlineKeyboardMarkup(row_width=2)
but8 = types.InlineKeyboardButton('Да, все верно', callback_data='right')
but9 = types.InlineKeyboardButton('Нет, не так', callback_data='un_right')
check_markup.add(but8, but9)



@qb.message_handler(commands=['start'])
def welcome(message):
    if (not db.Sqlither.user_exists(self=True, user_id=message.from_user.id)):
        db.Sqlither.add_user(self=True, user_id=message.from_user.id, order_id=all_data['last_order_id'],
                             paid=False, delivered=False, carried=False,
                             tie_def=0, tie_int=0, tie_fig=0, all_price=0)
        all_data['last_order_id'] += 1
        qb.send_message(message.from_user.id, 'Добро пожаловать! Будем знакомы, я - Имперский интернет-магазин'
                                              ' (модель IS-002).', reply_markup=markup)
    else:
        qb.send_message(message.from_user.id, 'Эй, привет! Я тебя знаю', reply_markup=markup)
        all_data['last_order_id'] += 1

def oplata1(message):
    try:
        print('1')
        import requests
        import json
        import sqlite3
        from random import randint
        print('1')
        conn = sqlite3.connect('db.db')
        c = conn.cursor()

        db.Sqlither.basket(user_id=message.from_user.id, self=True)
        print('1')
        phone = str(message.text)
        sum = db.basket['all_price']
        nw = c.execute('SELECT `order_id` FROM `users` WHERE `user_id` = ?', (message.from_user.id,)).fetchone()
        random_code = nw[0]
        print('1')
        print('2')
        QIWI_TOKEN = '33a620d083281a4a3641f7845563bc5b'
        QIWI_ACCOUNT = '79109024495'
        print('3')
        s = requests.Session()
        s.headers['authorization'] = 'Bearer ' + QIWI_TOKEN
        parameters = {'rows': '50'}
        h = s.get('https://edge.qiwi.com/payment-history/v1/persons/' + QIWI_ACCOUNT + '/payments', params=parameters)
        req = json.loads(h.text)
        print('1')
        c.execute("CREATE TABLE IF NOT EXISTS payment_query(user_id INTEGER, phone TEXT, sum INTEGER, code INTEGER)")


        c.execute(f"INSERT INTO payment_query VALUES(?, ?, ?, ?)", (message.from_user.id, phone, sum, random_code))

        result = c.execute(f"SELECT * FROM payment_query WHERE user_id = {message.chat.id}").fetchone()  # достаем данные из таблицы


        print(phone, random_code, sum)
        db.basket=[]

        qb.send_message(message.from_user.id, 'Ваш телефон: %s, Ваш айди заказа: %s, Сумма: %s' % (phone, random_code, sum))
        qb.send_message(message.from_user.id, 'Переведите деньги на этот счет киви:\n'
                                              '33a620d083281a4a3641f7845563bc5b')

        oplata.process.check_qiwi(self=True)
        # проходимся циклом по словарю
        for i in range(len(req['data'])):
            if req['data'][i]['account'] == phone:
                if req['data'][i]['comment'] == random_code:
                    if req['data'][i]['sum']['amount'] == sum:
                        c.execute('UPDATE `order_status` SET `paid` = 1 WHERE user_id = ?', (message.from_user.id))
                        qb.send_message(message.from_user.id, 'Оплата принята')

        conn = sqlite3.connect('db.db')
        c = conn.cursor()
        db.Sqlither.regorder(self=True, user_id=message.from_user.id, new_order_id=all_data['last_order_id'])
        all_data['last_order_id'] += 1
        conn.commit()
    except Exception as e:
        print(e)

def setstat2(message):
    all_data['now_id'] = message.text
    qb.send_message(message.from_user.id, 'Какой статус Вы хотите добавить?', reply_markup=setstat_markup)

def delivered(message):
    print('yo1')
    db.Sqlither.delivered(self=True, user_id=all_data['now_id'], deliv=True)
    print('yo2')
    qb.send_message(all_data['now_id'], 'Заказ с идентификатором %s доставлен по адресу:\n!' % (db.ad['nci'], place[db.ad['np']]))
    all_data['now_id'] = None


def set_count(message):
    try:
        all_data['counts'] = message.text
        print(all_data['now_prod'])
        if all_data['now_prod'] == 'tie_fig':
            db.Sqlither.add_fighter(self=True, user_id=message.from_user.id, count=int(all_data['counts']))
            if db.datas['Err'] == True:
                send = qb.send_message(message.from_user.id, 'Оххх, вы не так ввели запрос!')
                db.datas['Err'] = False
                qb.register_next_step_handler(send, set_count)
            else:
                qb.send_message(message.from_user.id, 'Успешно добавлено  в корзину')

        elif all_data['now_prod'] == 'tie_def':
            db.Sqlither.add_defender(self=True, user_id=message.from_user.id, count=int(all_data['counts']))
            if db.datas['Err'] == True:
                send = qb.send_message(message.from_user.id, 'Оххх, вы не так ввели запрос!')
                db.datas['Err'] = False
                qb.register_next_step_handler(send, set_count)
            else:
                qb.send_message(message.from_user.id, 'Успешно добавлено  в корзину')

        elif all_data['now_prod'] == 'tie_int':
            db.Sqlither.add_interceptor(self=True, user_id=message.from_user.id, count=int(all_data['counts']))
            if db.datas['Err'] == True:
                send = qb.send_message(message.from_user.id, 'Оххх, вы не так ввели запрос!')
                db.datas['Err'] = False
                qb.register_next_step_handler(send, set_count)
            else:
                qb.send_message(message.from_user.id, 'Успешно добавлено  в корзину')

        all_data['counts'] = None
        all_data['now_prod'] = None

    except Exception as er:
        db.datas['Err'] = True

    if db.datas['Err'] == True:
        send = qb.send_message(message.from_user.id, 'Введите пожалуйста только число:')
        db.datas['Err'] = False
        qb.register_next_step_handler(send, set_count)


def delete_fromb(message):
    all_data['now_id'] = message.from_user.id
    all_data['counts'] = message.text

    if all_data['now_del'] == '1':
        db.Sqlither.delete_from_basket(self=True, user_id=message.from_user.id, counts=all_data['counts'], numb='1')
        if db.datas['Err'] == True:
            send = qb.send_message(message.from_user.id, 'Введите пожалуйста только число, не превышающее количество,'
                                                         'уже присутствующее в Вашей корзине: ')
            db.datas['Err'] = False
            print('III')
            qb.register_next_step_handler(send, delete_fromb)
            print('XXX')
            breakpoint()




    elif all_data['now_del'] == '2':
        print('deleting2')
        db.Sqlither.delete_from_basket(self=True, user_id=message.from_user.id, counts=all_data['counts'],
                                       numb='2')
        if db.datas['Err'] == True:
            send = qb.send_message(message.from_user.id, 'Введите пожалуйста только число, не превышающее количество,'
                                                         'уже присутствующее в Вашей корзине: ')
            db.datas['Err'] = False
            print('III')
            qb.register_next_step_handler(send, delete_fromb)
            print('XXX')
            breakpoint()

    elif all_data['now_del'] == '3':
        db.Sqlither.delete_from_basket(self=True, user_id=message.from_user.id, counts=all_data['counts'],
                                       numb='3')
        if db.datas['Err'] == True:
            send = qb.send_message(message.from_user.id, 'Введите пожалуйста только число, не превышающее количество,'
                                                         'уже присутствующее в Вашей корзине: ')
            db.datas['Err'] = False
            print('III')
            qb.register_next_step_handler(send, delete_fromb)
            print('XXX')
            breakpoint()

    all_data['now_id'] = None
    all_data['counts'] = None
    all_data['now_del'] = None
    db.basket2 = []
    qb.send_message(message.from_user.id, 'Успешно удалено из корзины')



def regorder(message):
    try:
        db.Sqlither.add_user_card(user_id=message.from_user.id, card_num=int(message.text))
        qb.send_message(message.from_user.id, 'Ваш платеж принят, спасибо за покупку!!')

    except Exception:
        print('THIS IS ERROR!!!11!!1')



@qb.message_handler(commands=['setstat'])
def setstat(message):
    if db.Sqlither.check_workers(self=True, user_id=message.from_user.id):
        send = qb.send_message(message.from_user.id, 'Рад видеть тебя! Введи идентификатор заказа: ')
        qb.register_next_step_handler(send, setstat2)

def basket1(message, mo):
    if mo == 1:
        db.Sqlither.basket(self=True, user_id=message.from_user.id)
        if db.basket['empty'] == False:
            couel = len(db.basket1)
            print(couel, db.basket1)
            for x in range(0, couel):
                qb.send_message(message.from_user.id, '%s. %s * %s\n'
                                                  'Итого за %s: %s' % (x + 1, product_data[db.basket1[x]]['beat_name'],
                                                                       db.basket[db.basket1[x]],
                                                                       product_data[db.basket1[x]]['beat_name'],
                                                                       product_data[db.basket1[x]]['price'] * db.basket[
                                                                           db.basket1[x]]))
                print(db.basket1[x])
                all_data['now_price'] = product_data[db.basket1[x]]['price'] * db.basket[db.basket1[x]]

            if couel == 1:
                qb.send_message(message.from_user.id, 'Итого: %s' % db.basket['all_price'], reply_markup=delete_markup)

            elif couel == 2:
                qb.send_message(message.from_user.id, 'Итого: %s' % db.basket['all_price'], reply_markup=delete_markup1)

            elif couel == 3:
                qb.send_message(message.from_user.id, 'Итого: %s' % db.basket['all_price'], reply_markup=delete_markup2)

            # qb.send_message(message.from_user.id, 'Итого: %s' % all_data['now_price'], reply_markup=delete_markup)
            all_data['now_price'] = None
            db.basket1 = []

        elif db.basket['empty'] == True:
            qb.send_message(message.from_user.id, 'Ваша корзина пуста')



@qb.message_handler(content_types=['text'])
def reactions(message):
    if message.text == 'Корзина':
        basket1(message=message, mo=1)


    elif message.text == 'Каталог':
        send = qb.send_message(message.from_user.id, '%s' % product_data['tie_fig']['desc'])
        all_data['mesid'] = send.message_id
        qb.send_photo(chat_id=message.chat.id, photo=open('imgs/%s.jpg' % all_data1[str(all_data1['now_id'])], 'rb'),
                       reply_markup=markup1)

        # qb.send_message(message.from_user.id, '...', reply_markup=markup1)

    elif message.text == 'Контакты':
        qb.send_message(message.chat.id, '===☎Контакты===\n\nГлавный разработчик\n@Spatium_Lustrator\nГлавный менеджер\n@Space_Scout_1')

    elif message.text == 'Оформление заказа':
        db.Sqlither.basket(self=True, user_id=message.from_user.id)
        if db.basket['empty'] == False:
            qb.send_message(message.from_user.id, 'Ваша корзина не пуста')
            couel = len(db.basket1)
            print(couel, db.basket1)
            for x in range(0, couel):
                qb.send_message(message.from_user.id, '%s. %s * %s\n'
                                                      'Итого за %s: %s' % (
                                x + 1, product_data[db.basket1[x]]['beat_name'],
                                db.basket[db.basket1[x]], product_data[db.basket1[x]]['beat_name'],
                                product_data[db.basket1[x]]['price'] * db.basket[db.basket1[x]]))
                print(db.basket1[x])
            qb.send_message(message.from_user.id, 'Итого: %s' % db.basket['all_price'])
            qb.send_message(message.from_user.id, 'Проверьте, верно ли составлен Ваш заказ', reply_markup=check_markup)

        elif db.basket['empty'] == True:
            qb.send_message(message.from_user.id, 'Эээ нет, погоди-ка. У тебя в корзине ведь ничего нет!!')
        # qb.send_message(message.from_user.id, 'Эта функция пока не работает')


@qb.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'tie1':
                send = qb.send_message(call.message.chat.id, 'Введите необходимое количество товара: ')
                all_data['now_prod'] = 'tie_fig'
                qb.register_next_step_handler(send, set_count)

            elif call.data == 'deliver':
                print('yo')
                #all_data['now_id'] = call.message
                all_data['now_id'] = call.message.chat.id
                delivered(call.message)

            elif call.data == 'tie3':
                send = qb.send_message(call.message.chat.id, 'Введите необходимое количество товара: ')
                all_data['now_prod'] = 'tie_int'
                qb.register_next_step_handler(send, set_count)


            elif call.data == 'tie2':
                send = qb.send_message(call.message.chat.id, 'Введите необходимое количество товара: ')
                all_data['now_prod'] = 'tie_def'
                qb.register_next_step_handler(send, set_count)

            elif call.data == 'del1':
                all_data['now_del'] = '1'
                send = qb.send_message(call.message.chat.id, 'Введите кол-во, которое необходимо удалить: ')
                qb.register_next_step_handler(send, delete_fromb)

            elif call.data == 'del2':
                all_data['now_del'] = '2'
                send = qb.send_message(call.message.chat.id, 'Введите кол-во, которое необходимо удалить: ')
                qb.register_next_step_handler(send, delete_fromb)
                print('deleting1')

            elif call.data == 'del3':
                all_data['now_del'] = '3'
                send = qb.send_message(call.message.chat.id, 'Введите кол-во, которое необходимо удалить: ')
                qb.register_next_step_handler(send, delete_fromb)

            elif call.data == "delall":
                db.Sqlither.clear_basket(self=True, user_id=call.message.chat.id)
                qb.send_message(call.message.chat.id, 'Успешно')

            elif call.data == '>':
                if (all_data1['now_id'] + 1) < 4:
                    all_data1['now_id'] += 1
                else:
                    all_data1['now_id'] -= 2
                    print('!?')

                print('!?!')
                qb.edit_message_text(chat_id=call.message.chat.id, message_id=all_data['mesid'], text='%s' % product_data[all_data1[str(all_data1['now_id'])]]['desc'])
                qb.edit_message_media(media=types.InputMedia(type='photo', media=open('imgs/%s.jpg' % all_data1[str(all_data1['now_id'])], 'rb')),
                                      chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=markup1)

            elif call.data == '<':
                if (all_data1['now_id'] - 1) > 0:
                    all_data1['now_id'] -= 1
                else:
                    all_data1['now_id'] += 2

                qb.edit_message_text(chat_id=call.message.chat.id, message_id=all_data['mesid'],
                                     text='%s' % product_data[all_data1[str(all_data1['now_id'])]]['desc'])
                qb.edit_message_media(media=types.InputMedia(type='photo', media=open('imgs/%s.jpg' % all_data1[str(all_data1['now_id'])], 'rb')),
                                      chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=markup1)

            elif call.data == 'right':
                qb.send_message(call.message.chat.id, 'Выберите место доставки: ', reply_markup=adresses_markup)

            elif call.data == 'place1':
                db.Sqlither.set_place(self=True, place=1, user_id=call.message.chat.id)
                send = qb.send_message(call.message.chat.id, 'Напишите ваш номер телефона\nВ формате +79998887766')
                qb.register_next_step_handler(send, oplata1)


            elif call.data == 'place2':
                db.Sqlither.set_place(self=True, place=2, user_id=call.message.chat.id)
                send = qb.send_message(call.message.chat.id, 'Напишите ваш номер телефона\nВ формате +79998887766')
                qb.register_next_step_handler(send, oplata1)

            elif call.data == 'place3':
                db.Sqlither.set_place(self=True, place=3, user_id=call.message.chat.id)
                send = qb.send_message(call.message.chat.id, 'Напишите ваш номер телефона\nВ формате +79998887766')
                qb.register_next_step_handler(send, oplata1)

            elif call.data == 'un_right':
                qb.send_message(call.message.chat.id, 'Если Вы зайдете в корзину, сможете удалить ненужные товары. '
                                                      'Чтобы добавить товар в корзину, войдите в каталог.'
                                                      'Вернитесь, когда будете уверены в заказе))')






    except Exception as e:
        print(repr(e))


qb.polling(none_stop=True, interval=0)