import sqlite3
import random
from db_config import *

conn = sqlite3.connect(DB_NAME, check_same_thread=False)
cur = conn.cursor()

class USER:
    def register(user_id, name, phone):
        cur.execute('SELECT user_id FROM users WHERE user_id=?', (user_id,))
        users = cur.fetchone()

        try:
            if users:
                return 'Вы уже зарегестрированы!'
            else:
                cur.execute('INSERT INTO users (user_id, name, phone) VALUES (?,?,?)', (user_id, name, phone,))
                conn.commit()
                return 'Вы успешно зарегистрированы!'
        except:
            pass

    def reg_taxist(user_id, name, phone, car):
        cur.execute('SELECT user_id FROM taxists WHERE user_id=?', (user_id,))
        users = cur.fetchone()

        try:
            if users:
                return None
            else:
                cur.execute('INSERT INTO taxists (user_id, full_name, phone, car) VALUES (?,?,?,?)', (user_id, name, phone, car,))
                conn.commit()
        except:
            pass

    def check_user(user_id):
        cur.execute('SELECT user_id FROM users WHERE user_id=?', (user_id,))
        users = cur.fetchone()

        if users:
            return True
        else:
            return None
    
    def check_taxist(user):
        cur.execute('SELECT user_id FROM taxists WHERE full_name=?', (user,))
        users = cur.fetchone()

        if users:
            return True
        else:
            return None

    def bun_user(user_id):
        cur.execute('SELECT user_id FROM users WHERE user_id=?', (user_id,))
        users = cur.fetchone()
        
        if users:
            cur.execute('DELETE FROM users WHERE user_id=?', (user_id,))
            conn.commit()
        
            cur.execute('INSERT INTO bun_user VALUES (?)', (user_id,))
            conn.commit()
        else:
            return None
    
    def check_bun_user(user_id):
        cur.execute('SELECT user_id FROM bun_user WHERE user_id=?', (user_id,))
        user = cur.fetchone()
        
        if user:
            return True
        else:
            return None
        
    def edit_driver(user, edited, edit):
        cur.execute('SELECT full_name FROM taxists WHERE full_name=?', (user,))
        users = cur.fetchone()
        
        if users:
            if edited == 'full_name':
                cur.execute('UPDATE taxists SET full_name=? WHERE full_name=?', (edit, user,))
                conn.commit()
            elif edited == 'phone':
                cur.execute('UPDATE taxists SET phone=? WHERE full_name=?', (edit, user,))
                conn.commit()
            elif edited == 'car':
                cur.execute('UPDATE taxists SET car=? WHERE full_name=?', (edit, user,))
                conn.commit()
        else:
            return None
    
    def count_users():
        cur.execute('SELECT COUNT(*) FROM users')
        count = cur.fetchone()
        
        return count[0]

    def user_list():
        cur.execute('SELECT * FROM users')
        users = cur.fetchall()

        return users
    
    def tax_list():
        cur.execute('SELECT * FROM taxists')
        users = cur.fetchall()

        return users
    
    def insert_sum_day(user_id, sum):
        cur.execute('UPDATE taxists SET sum_day=? WHERE user_id=?', (sum, user_id,))
        conn.commit()

    def get_sum_day(user_id):
        cur.execute('SELECT sum_day FROM taxists WHERE user_id=?', (user_id,))
        sum = cur.fetchone()

        return sum[0]

class TAXI:
    def client(user_id, rate, _in, _out):
        cur.execute('INSERT INTO taxi (user_id, rate, _in, _out) VALUES (?,?,?,?)', (user_id, rate, _in, _out,))
        conn.commit()
    
    def random_taxist():
        cur.execute('SELECT user_id, clients FROM tru_taxists')
        id_list = cur.fetchall()
        
        id_drivers = []

        for row in id_list:
            if row[1] != None:
                id_drivers.append(row[0])
                taxist = random.choice(id_drivers)
                return taxist
            else:
                return None
    
    def get_tru_taxists():
        cur.execute('SELECT user_id FROM tru_taxists')
        user = cur.fetchall()[0]
        
        return user
    
    def get_taxi(client_id):
        cur.execute('SELECT * FROM taxi WHERE user_id=?', (client_id,))
        user = cur.fetchall()

        return user
    
    def get_tru_client_taxi(user_id):
        cur.execute('SELECT clients FROM tru_taxists WHERE clients=?', (user_id,))
        user = cur.fetchone()
        
        if user:
            return True
        else:
            return None
    
    def get_client_taxi(user_id):
        cur.execute('SELECT clients FROM tru_taxists WHERE user_id=?', (user_id,))
        user = cur.fetchone()
        
        if user:
            return user
        else:
            return None

    def get_tru_taxi(user_id):
        cur.execute('SELECT user_id FROM tru_taxists WHERE user_id=?', (user_id,))
        user = cur.fetchone()
        
        if user:
            return True
        else:
            return None

    def insert_client_to_taxist(user_id, client):
        cur.execute('UPDATE taxist SET client=? WHERE user_id=?', (client, user_id,))
        conn.commit()

    def check_client(user_id):
        cur.execute('SELECT user_id FROM taxi WHERE user_id=?', (user_id,))
        user = cur.fetchone()

        if user:
            return True
        else:
            return None

    def get_taxist_name(user_id):
        cur.execute('SELECT full_name FROM taxists WHERE user_id=?', (user_id,))
        taxist = cur.fetchone()

        return taxist

    def get_taxist_phone(user_id):
        cur.execute('SELECT phone FROM taxists WHERE user_id=?', (user_id,))
        taxist = cur.fetchone()

        return taxist

    def get_taxist_car(user_id):
        cur.execute('SELECT car FROM taxists WHERE user_id=?', (user_id,))
        taxist = cur.fetchone()

        return taxist

    def check_taxist(user_id):
        cur.execute('SELECT user_id FROM taxists WHERE user_id=?', (user_id,))
        users = cur.fetchone()

        if users:
            return True
        else:
            return None
    
    def del_taxi(user_id):
        cur.execute('DELETE FROM taxi WHERE user_id=?', (user_id,))
        conn.commit()

    def accept(user_id, client):
        cur.execute('UPDATE tru_taxists SET clients=? WHERE user_id=?', (client, user_id,))
        conn.commit()
    
    def close_zakaz(user_id):
        cur.execute('UPDATE tru_taxists SET clients="None" WHERE user_id=?', (user_id,))
        conn.commit()
    
    def insert_taxist_line(user_id):
        cur.execute('INSERT INTO tru_taxists (user_id) VALUES (?)', (user_id,))
        conn.commit()
    
    def del_taxist_line(user_id):
        cur.execute('DELETE FROM `tru_taxists` WHERE `user_id`=?', (user_id,))
        conn.commit()

class PASS:
    def set_pass(password):
        cur.execute('INSERT INTO pred_insert_taxist (password) VALUES (?)', (password,))
        conn.commit()
    
    def del_pred_pass(password):
        cur.execute('DELETE FROM pred_insert_taxist WHERE password=?', (password,))
        conn.commit()

    def get_pass(passwd):
        cur.execute('SELECT password FROM pred_insert_taxist WHERE password=?', (passwd,))
        passw = cur.fetchone()

        return passw

class SUM:
    def insert_sum(count, rate):
        print(count, rate)
        cur.execute('UPDATE sum_taxi SET count=? WHERE rate=?', (count, rate))
        conn.commit()

    def get_sum(rate):
        cur.execute('SELECT count FROM sum_taxi WHERE rate=?', (rate,))
        sum = cur.fetchone()

        return sum

class ADMIN:
    def get_admin():
        cur.execute('SELECT user_id FROM admins')
        usr = cur.fetchall()

        return usr

class NOTIFICATION:
    def notific_taxist():
        cur.execute('SELECT user_id FROM taxists')
        users = cur.fetchall()
        
        return users
    
    def notific():
        cur.execute('SELECT user_id FROM users')
        users = cur.fetchall()
        
        return users