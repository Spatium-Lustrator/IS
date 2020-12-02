import sqlite3

order_id = None
ad = {'nci': None, 'None': 0}
datas = {'Err': False}
ties = ['tie_fig', 'tie_def', 'tie_int']
basket = {'tie_fig': None, 'tie_def': None, 'tie_int': None, 'empty': False}
basket1 = []
basket2 = []

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
        cursor.execute('insert into order_composition(order_id, user_id, tie_fig, tie_de, tie_in) values(?, ?, ?, ?, ?)',
                       (order_id, user_id, tie_fig, tie_def, tie_int))
        cursor.execute('insert into users(user_id, order_id) values(?, ?)', (user_id, order_id))
        conn.commit()
        conn.close()

    def add_fighter(self, user_id, count):
        try:
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            nc = cursor.execute('SELECT `tie_fig` FROM `order_composition` WHERE `user_id` = ?', (user_id, )).fetchone()
            print(nc)
            cursor.execute('UPDATE `order_composition` SET `tie_fig` = ? WHERE `user_id` = ?', (count+nc[0], user_id))
            conn.commit()
            conn.close()
            print('!888')

        except Exception as er:
            datas['Err'] = True

    def add_defender(self, user_id, count):
        try:
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            nc = cursor.execute('SELECT `tie_de` FROM `order_composition` WHERE `user_id` = ?', (user_id, )).fetchone()
            print(nc)
            cursor.execute('UPDATE `order_composition` SET `tie_de` = ? WHERE `user_id` = ?', (count+nc[0], user_id))
            conn.commit()
            conn.close()

        except Exception as er:
            datas['Err'] = True

    def add_interceptor(self, user_id, count):
        try:
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            nc = cursor.execute('SELECT `tie_int` FROM `order_composition` WHERE `user_id` = ?', (user_id,)).fetchone()
            print(nc)
            cursor.execute('UPDATE `order_composition` SET `tie_int` = ? WHERE `user_id` = ?', (count+nc[0], user_id))
            conn.commit()
            conn.close()
        except Exception as er:
            datas['Err'] = True

    def check_workers(self, user_id):
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        result = cursor.execute('SELECT * FROM `our_workers` WHERE `user_id` = ?', (user_id,)).fetchall()
        return result
        conn.close()

    def delivered(self, user_id):
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE `order_status` SET `delivered` = 1 WHERE `user_id` = ?', (user_id, ))
        a = cursor.execute('SELECT * FROM `users` WHERE `user_id` = ?', (user_id,)).fetchone()
        ad['nci'] = a[1]
        print('yo3')
        conn.commit()
        conn.close()


    def basket(self, user_id):
        basket['empty'] = False
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        result = cursor.execute('SELECT * FROM `order_composition` WHERE user_id = ?', (user_id,)).fetchone()
        for i in range(0, 3):
            if result != None:
                basket[ties[i]] = result[i+2]
                print(basket)
                print(i)
                print(ties[i])

        for i in range(0, 3):
            if basket[ties[i]] == 0:
                print('This is dict', basket[ties[i]])
                ad['None'] += 1
                print(ad['None'])
            else:
                if ties[i] not in basket1 and basket[ties[i]] > 0:
                    basket1.append(ties[i])
                    print(basket1)
                    basket2.append(ties[i])


        if ad['None'] >= 3:
            basket['empty'] = True
        ad['None'] = 0

    def delete_from_basket(self, user_id, counts, numb):
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        try:
            if numb == '1':
                if basket2[0] == 'tie_fig':
                    nc = cursor.execute('SELECT `tie_fig` FROM `order_composition` WHERE `user_id` = ?', (user_id,)).fetchone()
                    cursor.execute('UPDATE `order_composition` SET `tie_fig` = ? WHERE `user_id` = ?', (int(nc[0])-int(counts), user_id))

                elif basket2[0] == 'tie_def':
                    nc = cursor.execute('SELECT `tie_de` FROM `order_composition` WHERE `user_id` = ?',
                                        (user_id,)).fetchone()
                    cursor.execute('UPDATE `order_composition` SET `tie_de` = ? WHERE `user_id` = ?',
                                   (int(nc[0]) - int(counts), user_id))

                elif basket2[0] == 'tie_int':
                    nc = cursor.execute('SELECT `tie_int` FROM `order_composition` WHERE `user_id` = ?',
                                    (user_id,)).fetchone()
                    cursor.execute('UPDATE `order_composition` SET `tie_int` = ? WHERE `user_id` = ?',
                               (int(nc[0]) - int(counts), user_id))

            elif numb == '2':
                if basket2[1] == 'tie_fig':
                    nc = cursor.execute('SELECT `tie_fig` FROM `order_composition` WHERE `user_id` = ?',
                                        (user_id,)).fetchone()
                    cursor.execute('UPDATE `order_composition` SET `tie_fig` = ? WHERE `user_id` = ?',
                                   (int(nc[0]) - int(counts), user_id))

                elif basket2[1] == 'tie_def':
                    nc = cursor.execute('SELECT `tie_de` FROM `order_composition` WHERE `user_id` = ?',
                                        (user_id,)).fetchone()
                    cursor.execute('UPDATE `order_composition` SET `tie_de` = ? WHERE `user_id` = ?',
                                (int(nc[0]) - int(counts), user_id))

                elif basket2[1] == 'tie_int':
                    nc = cursor.execute('SELECT `tie_int` FROM `order_composition` WHERE `user_id` = ?',
                                        (user_id,)).fetchone()
                    cursor.execute('UPDATE `order_composition` SET `tie_int` = ? WHERE `user_id` = ?',
                               (int(nc[0]) - int(counts), user_id))

            elif numb == '3':
                if basket2[2] == 'tie_fig':
                    nc = cursor.execute('SELECT `tie_fig` FROM `order_composition` WHERE `user_id` = ?',
                                        (user_id,)).fetchone()
                    cursor.execute('UPDATE `order_composition` SET `tie_fig` = ? WHERE `user_id` = ?',
                                   (int(nc[0]) - int(counts), user_id))

                elif basket2[2] == 'tie_def':
                    nc = cursor.execute('SELECT `tie_de` FROM `order_composition` WHERE `user_id` = ?',
                                        (user_id,)).fetchone()
                    cursor.execute('UPDATE `order_composition` SET `tie_de` = ? WHERE `user_id` = ?',
                                   (int(nc[0]) - int(counts), user_id))

                elif basket2[2] == 'tie_int':
                    nc = cursor.execute('SELECT `tie_int` FROM `order_composition` WHERE `user_id` = ?',
                                        (user_id,)).fetchone()
                    cursor.execute('UPDATE `order_composition` SET `tie_int` = ? WHERE `user_id` = ?',
                                   (int(nc[0]) - int(counts), user_id))

        except Exception as er:
            datas['Err'] = True




        conn.commit()
        conn.close()

    def clear_basket(self, user_id):
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE `order_composition` SET `tie_fig` = 0, `tie_de` = 0, `tie_int` = 0 WHERE user_id = ?',
                       (user_id, ))
        conn.commit()
        conn.close()


    def reg_order(self, user_id):
        pass