import sqlite3

order_id = None

class Sqlither:

    def user_exists(self, user_id):
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        result = cursor.execute('SELECT * FROM `users` WHERE `user_id` = ?', (user_id,)).fetchall()
        print(result)
        return result

    def add_user(self, user_id, order_id):
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute('insert into users(user_id, order_id) values(?, ?)', (user_id, order_id))
        conn.commit()
        conn.close()

    def get_order_id(self, user_id):
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        a = cursor.execute('select * from users(order_id) where user_id = ?' (user_id, ))
        print(a)

    def add_fighter(self, order_id, count):
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE `order_composition` SET `tie_fig` = ? WHERE `order_id` = ?', (count, order_id))
        conn.commit()
        conn.close()


