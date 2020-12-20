import requests
import json
import sqlite3
from random import randint




class process:


    def check_qiwi(self):
        QIWI_TOKEN = '33a620d083281a4a3641f7845563bc5b'
        QIWI_ACCOUNT = '+79109024495'
        s = requests.Session()
        s.headers['authorization'] = 'Bearer ' + QIWI_TOKEN
        parameters = {'tie_fig': '500',
            'tie_def': '600',
            'tie_int': '650'}
        h = s.get('https://edge.qiwi.com/payment-history/v1/persons/'+ QIWI_ACCOUNT +'/payments', params = parameters)
        req = json.loads(h.text)

    def oplata_1(self, user_id, phone, code, counts_2):
        conn = sqlite3.connect('db.db')
        curs = conn.cursor()
        curs.execute('')
        nc = curs.execute('SELECT `phone` FROM `payment_query` WHERE `user_id` = ?', (user_id,)).fetchone()
        print(nc[0])
        curs.execute('UPDATE `payment_query` SET `phone` = ? WHERE `user_id` = ?', (phone, user_id))
        nc = curs.execute('SELECT `sum` FROM `payment_query` WHERE `user_id` = ?', (user_id,)).fetchone()
        curs.execute('UPDATE `payment_query` SET `sum` = ? WHERE `user_id` = ?', (counts_2, user_id))
        nc = curs.execute('SELECT `code` FROM `payment_query` WHERE `user_id` = ?', (user_id,)).fetchone()
        curs.execute('UPDATE `payment_query` SET `code` = ? WHERE `user_id` = ?', (code, user_id))
        conn.commit()
        conn.close()
