import sqlite3

order_id = None
ad = {'nci': None, 'None': 0}
ties = ['tie_fig', 'tie_def', 'tie_int']
basket = {'tie_fig': None, 'tie_def': None, 'tie_int': None, 'empty': False}
basket1 = []

class Sqlither:

    def user_exists(self, user_id):
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        result = cursor.execute('SELECT * FROM `users` WHERE `user_id` = ?', (user_id, )).fetchall()
        print(result)
        return result
        conn.close()

    def add_user(self, user_id, order_id, paid, delivered, carried, tie_fig, tie_int, tie_def):
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute('insert into order_status(user_id, order_id, paid, delivered, carried) values(?, ?, ?, ?, ?)',
                       (user_id, order_id, paid, delivered, carried))
        cursor.execute('insert into order_composition(order_id, user_id, tie_fig, tie_def, tie_int) values(?, ?, ?, ?, ?)',
                       (order_id, user_id, tie_fig, tie_def, tie_int))
        cursor.execute('insert into users(user_id, order_id) values(?, ?)', (user_id, order_id))
        conn.commit()
        conn.close()

    def add_fighter(self, user_id, count):
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE `order_composition` SET `tie_fig` = ? WHERE `user_id` = ?', (count, user_id))
        conn.commit()
        conn.close()

    def add_defender(self, user_id, count):
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE `order_composition` SET `tie_def` = ? WHERE `user_id` = ?', (count, user_id))
        conn.commit()
        conn.close()

    def add_interceptor(self, user_id, count):
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE `order_composition` SET `tie_int` = ? WHERE `user_id` = ?', (count, user_id))
        conn.commit()
        conn.close()

    def check_workers(self, user_id):
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        result = cursor.execute('SELECT * FROM `our_workers` WHERE `user_id` = ?', (user_id,)).fetchall()
        return result
        conn.close()

    def delivered(self, user_id, deliv):
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE `order_status` SET `delivered` = 1 WHERE `user_id` = ?', (user_id, ))
        a = cursor.execute('SELECT * FROM `users` WHERE `user_id` = ?', (user_id,)).fetchone()
        ad['nci'] = a[1]
        print('yo3')
        conn.commit()
        conn.close()
        # print('yo3')
        # cursor.execute('UPDATE `order_status` SET `delivered` = ? WHERE `order_id` = ?', (deliv, user_id, ))
        # print('yo4')
        # nui = cursor.execute('SELECT * FROM `users` WHERE `order_id` = ?', (order_id, ))
        # ad['nci'] = nui[0]
        # print(nui[0])
        # conn.commit()
        # conn.close()

    def basket(self, user_id):
        basket['empty'] = False
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        for i in range(0, 3):
            result = cursor.execute('SELECT * FROM `order_composition` WHERE user_id = ?', (user_id, )).fetchone()
            if result != None:
                basket[ties[i]] = result[i+2]
            print(result)
            print(basket)
        for i in range(0, 3):
            if basket[ties[i]] == 0:
                ad['None'] += 1
                print(ad['None'])
            else:
                basket1.append(ties[i])

        if ad['None'] >= 3:
            basket['empty'] = True
        ad['None'] = 0

    def reg_order(self, user_id):
        pass
