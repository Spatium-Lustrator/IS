import sqlite3

order_id = None
ad = {'nci': None, 'None': 0, 'np': None}
datas = {'Err': False, 'paid': False}
ties = ['tie_fig', 'tie_def', 'tie_int']
basket = {'tie_fig': None, 'tie_def': None, 'tie_int': None, 'all_price': None, 'empty': False}

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

    def add_user(self, user_id, order_id, paid, delivered, carried, tie_fig, tie_int, tie_def, all_price):
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute('insert into order_status(user_id, order_id, paid, delivered, carried) values(?, ?, ?, ?, ?)',
                       (user_id, order_id, paid, delivered, carried))
        cursor.execute('insert into order_composition(order_id, user_id, tie_fig, tie_de, tie_int, all_price) values(?, ?, ?, ?, ?, ?)',
                       (order_id, user_id, tie_fig, tie_def, tie_int, all_price))
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
            nc = cursor.execute('SELECT `all_price` FROM `order_composition` WHERE `user_id` = ?', (user_id,)).fetchone()
            cursor.execute('UPDATE `order_composition` SET `all_price` = ? WHERE `user_id` = ?', (count*500 + nc[0], user_id))
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
            nc = cursor.execute('SELECT `all_price` FROM `order_composition` WHERE `user_id` = ?',
                                (user_id,)).fetchone()
            cursor.execute('UPDATE `order_composition` SET `all_price` = ? WHERE `user_id` = ?',
                           (count * 600 + nc[0], user_id))

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
            nc = cursor.execute('SELECT `all_price` FROM `order_composition` WHERE `user_id` = ?',
                                (user_id,)).fetchone()
            cursor.execute('UPDATE `order_composition` SET `all_price` = ? WHERE `user_id` = ?',
                           (count * 650 + nc[0], user_id))

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
        a = cursor.execute('SELECT * FROM `order_status` WHERE `user_id` = ?', (user_id,)).fetchone()
        ad['np'] = a[5]
        print('yo3')
        conn.commit()
        conn.close()


    def basket(self, user_id):
        basket['empty'] = False
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        result = cursor.execute('SELECT * FROM `order_composition` WHERE user_id = ?', (user_id,)).fetchone()
        print(result)
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
        basket['all_price'] = result[5]

    def delete_from_basket(self, user_id, counts, numb):
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        try:
            if numb == '1':
                if basket2[0] == 'tie_fig':
                    nc = cursor.execute('SELECT `tie_fig` FROM `order_composition` WHERE `user_id` = ?', (user_id,)).fetchone()
                    if nc[0] >= int(counts):
                        print('It`s ok')
                        cursor.execute('UPDATE `order_composition` SET `tie_fig` = ? WHERE `user_id` = ?', (int(nc[0])-int(counts), user_id))
                        nc = cursor.execute('SELECT `all_price` FROM `order_composition` WHERE `user_id` = ?',
                                            (user_id,)).fetchone()
                        cursor.execute('UPDATE `order_composition` SET `all_price` = ? WHERE `user_id` = ?',
                                       (nc[0]-int(counts)*500, user_id))
                    else:
                        datas['Err'] = True
                        return AttributeError

                elif basket2[0] == 'tie_def':
                    nc = cursor.execute('SELECT `tie_de` FROM `order_composition` WHERE `user_id` = ?',
                                        (user_id,)).fetchone()
                    if nc[0] >= int(counts):
                        cursor.execute('UPDATE `order_composition` SET `tie_de` = ? WHERE `user_id` = ?',
                                   (int(nc[0]) - int(counts), user_id))
                        nc = cursor.execute('SELECT `all_price` FROM `order_composition` WHERE `user_id` = ?',
                                        (user_id,)).fetchone()
                        cursor.execute('UPDATE `order_composition` SET `all_price` = ? WHERE `user_id` = ?',
                                       (nc[0] - int(counts) * 600, user_id))

                elif basket2[0] == 'tie_int':
                    nc = cursor.execute('SELECT `tie_int` FROM `order_composition` WHERE `user_id` = ?',
                                    (user_id,)).fetchone()
                    if nc[0] >= int(counts):
                        cursor.execute('UPDATE `order_composition` SET `tie_int` = ? WHERE `user_id` = ?',
                                   (int(nc[0]) - int(counts), user_id))
                        nc = cursor.execute('SELECT `all_price` FROM `order_composition` WHERE `user_id` = ?',
                                            (user_id,)).fetchone()
                        cursor.execute('UPDATE `order_composition` SET `all_price` = ? WHERE `user_id` = ?',
                                       (nc[0] - int(counts) * 650, user_id))

            elif numb == '2':
                if basket2[1] == 'tie_fig':
                    nc = cursor.execute('SELECT `tie_fig` FROM `order_composition` WHERE `user_id` = ?',
                                        (user_id,)).fetchone()
                    if nc[0] >= int(counts):
                        cursor.execute('UPDATE `order_composition` SET `tie_fig` = ? WHERE `user_id` = ?',
                                       (int(nc[0]) - int(counts), user_id))
                        nc = cursor.execute('SELECT `all_price` FROM `order_composition` WHERE `user_id` = ?',
                                            (user_id,)).fetchone()
                        cursor.execute('UPDATE `order_composition` SET `all_price` = ? WHERE `user_id` = ?',
                                       (nc[0] - int(counts) * 500, user_id))

                elif basket2[1] == 'tie_def':
                    nc = cursor.execute('SELECT `tie_de` FROM `order_composition` WHERE `user_id` = ?',
                                        (user_id,)).fetchone()
                    if nc[0] >= int(counts):
                        cursor.execute('UPDATE `order_composition` SET `tie_de` = ? WHERE `user_id` = ?',
                                    (int(nc[0]) - int(counts), user_id))
                        nc = cursor.execute('SELECT `all_price` FROM `order_composition` WHERE `user_id` = ?',
                                            (user_id,)).fetchone()
                        cursor.execute('UPDATE `order_composition` SET `all_price` = ? WHERE `user_id` = ?',
                                       (nc[0] - int(counts) * 600, user_id))

                elif basket2[1] == 'tie_int':
                    nc = cursor.execute('SELECT `tie_int` FROM `order_composition` WHERE `user_id` = ?',
                                        (user_id,)).fetchone()
                    if nc[0] >= int(counts):
                        cursor.execute('UPDATE `order_composition` SET `tie_int` = ? WHERE `user_id` = ?',
                                   (int(nc[0]) - int(counts), user_id))
                        nc = cursor.execute('SELECT `all_price` FROM `order_composition` WHERE `user_id` = ?',
                                            (user_id,)).fetchone()
                        cursor.execute('UPDATE `order_composition` SET `all_price` = ? WHERE `user_id` = ?',
                                       (nc[0] - int(counts) * 650, user_id))

            elif numb == '3':
                if basket2[2] == 'tie_fig':
                    nc = cursor.execute('SELECT `tie_fig` FROM `order_composition` WHERE `user_id` = ?',
                                        (user_id,)).fetchone()
                    if nc[0] >= int(counts):
                        cursor.execute('UPDATE `order_composition` SET `tie_fig` = ? WHERE `user_id` = ?',
                                           (int(nc[0]) - int(counts), user_id))
                        nc = cursor.execute('SELECT `all_price` FROM `order_composition` WHERE `user_id` = ?',
                                            (user_id,)).fetchone()
                        cursor.execute('UPDATE `order_composition` SET `all_price` = ? WHERE `user_id` = ?',
                                       (nc[0] - int(counts) * 500, user_id))

                elif basket2[2] == 'tie_def':
                    nc = cursor.execute('SELECT `tie_de` FROM `order_composition` WHERE `user_id` = ?',
                                        (user_id,)).fetchone()
                    if nc[0] >= int(counts):
                        cursor.execute('UPDATE `order_composition` SET `tie_de` = ? WHERE `user_id` = ?',
                                       (int(nc[0]) - int(counts), user_id))
                        nc = cursor.execute('SELECT `all_price` FROM `order_composition` WHERE `user_id` = ?',
                                            (user_id,)).fetchone()
                        cursor.execute('UPDATE `order_composition` SET `all_price` = ? WHERE `user_id` = ?',
                                       (nc[0] - int(counts) * 600, user_id))

                elif basket2[2] == 'tie_int':
                    nc = cursor.execute('SELECT `tie_int` FROM `order_composition` WHERE `user_id` = ?',
                                        (user_id,)).fetchone()
                    if nc[0] >= int(counts):
                        cursor.execute('UPDATE `order_composition` SET `tie_int` = ? WHERE `user_id` = ?',
                                       (int(nc[0]) - int(counts), user_id))
                        nc = cursor.execute('SELECT `all_price` FROM `order_composition` WHERE `user_id` = ?',
                                            (user_id,)).fetchone()
                        cursor.execute('UPDATE `order_composition` SET `all_price` = ? WHERE `user_id` = ?',
                                       (nc[0] - int(counts) * 650, user_id))

        except Exception as er:
            print(er)
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

    def set_place(self, user_id, place):
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE `order_status` SET `place` = ? WHERE user_id = ?', (place, user_id))
        conn.commit()
        conn.close()

    def add_user_card(self, user_id, card_num):
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE `users` SET `num_acc` = ? WHERE user_id = ?', (card_num, user_id))
        conn.commit()
        conn.close()

    def wait_for_payment(self, user_id):
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        a = 0
        while datas['paid'] == False:
            res = cursor.execute('SELECT `paid` FROM `order_status` WHERE `user_id` = ?',
                           (user_id,)).fetchone()
            if a == 6:
                cursor.execute('UPDATE `order_status` SET `paid` = 1 WHERE user_id = ?', (user_id, ))
            a += 1
            datas['paid'] = res[0]
            print(res)

        conn.commit()
        conn.close()


    def reg_order(self, user_id):
        pass
