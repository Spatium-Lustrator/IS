import telebot
from telebot import types

token = '1303608144:AAH09kqBe4ahjau7lUKbx6kibiyK2QyvAXk'
qb = telebot.TeleBot(token)

first_pic = 'https://i.etsystatic.com/12566580/r/il/04bc88/1172748671/il_1588xN.1172748671_t0rf.jpg'
second_pic = 'https://www.backgroundscool.com/wp-content/uploads/2020/02/darth-vader-arts-pq-1080x1920-1.jpg'
third_pic = 'https://i.pinimg.com/736x/45/f9/75/45f97530a8d3e33437307d700015efcd.jpg'
pic_tie_fig = open('imgs/tie_fig.jpg', 'rb')
pic_tie_def = open('imgs/tie_def.jpg', 'rb')
pic_tie_int = open('imgs/tie_int.jpg', 'rb')
ties = [pic_tie_fig, pic_tie_def, pic_tie_int]
all_data = {'1': first_pic, '2': second_pic, '3': third_pic, 'now_id': 1}

markup = types.InlineKeyboardMarkup(row_width=2)
but1 = types.InlineKeyboardButton('<<<', callback_data='<')
but2 = types.InlineKeyboardButton('>>>', callback_data='>')
markup.add(but1, but2)

@qb.message_handler(commands=['start'])
def pics(message):
    global id
    id = qb.send_photo(message.from_user.id, photo=first_pic, reply_markup=markup)

@qb.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == '<':
                if (all_data['now_id'] - 1) > 0:
                    all_data['now_id'] -= 1
                else:
                    all_data['now_id'] += 2
                qb.edit_message_media(media=types.InputMedia(type='photo', media=ties[all_data['now_id']]),
                                      chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=markup)

            elif call.data == '>':
                if (all_data['now_id'] + 1) < 4:
                    all_data['now_id'] += 1
                else:
                    all_data['now_id'] -= 2
                qb.edit_message_media(media=types.InputMedia(type='photo', media=all_data[str(all_data['now_id'])]),
                                      chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=markup)



    except Exception as e:
        print(repr(e))

qb.polling(none_stop=True, interval=0)