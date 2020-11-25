import sqlite3

order_id = None

class Sqlither:

    def user_exists(self, user_id):
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        result = cursor.execute('SELECT * FROM `users` WHERE `user_id` = ?', (user_id, )).fetchall()
        print(result)
        return result

    def add_user(self, user_id, paid, delivered, carried, tie_fig, tie_int, tie_def):
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute('insert into order_status(user_id, paid, delivered, carried) values(?, ?, ?, ?)', (user_id, paid,
                                                                                                          delivered,
                                                                                                          carried))
        cursor.execute('insert into order_composition(user_id, tie_fig, tie_def, tie_int) values(?, ?, ?, ?)', (user_id,
                                                                                                                tie_fig,
                                                                                                                tie_def,
                                                                                                                tie_int))
        cursor.execute('insert into users(user_id) values(?)', (user_id, ))
        conn.commit()
        conn.close()

    def add_fighter(self, user_id, count):
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE `order_composition` SET `tie_fig` = ? WHERE `user_id` = ?', (count, user_id))
        conn.commit()
        conn.close()

    def add_defender(self, user, count):
        pass