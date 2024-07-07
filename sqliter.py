import sqlite3
from datetime import datetime
from aiogram import html


class SQLiter:
    def __init__(self, connection):
        self.connection = connection

        with sqlite3.connect(connection) as db:
            cursor = db.cursor()

            # Создаем таблицу users с необходимыми полями
            cursor.execute("""CREATE TABLE IF NOT EXISTS users(
				user_id INTEGER PRIMARY KEY, 
				first_name VARCHAR, 
                last_name VARCHAR,
				username VARCHAR,
				date VARCHAR,
                language_code VARCHAR,
                is_premium VARCHAR
			)""")

    # Проверяем, существует ли пользователь с указанным user_id в базе данных
    def user_exists(self, user_id):
        with sqlite3.connect(self.connection) as db:
            cursor = db.cursor()

             # Выполняем запрос для поиска пользователя по user_id
            cursor.execute("SELECT user_id FROM users WHERE user_id = ?", [user_id])
            if cursor.fetchone() == None:
                return 0
            elif cursor.fetchone() != None:
                return 1
            
    def add_user(self, user_id, first_name, last_name, username, language_code, is_premium):
        with sqlite3.connect(self.connection) as db:
            cursor = db.cursor()
            data = [user_id, first_name, last_name, username, datetime.today(), language_code, is_premium]

            cursor.execute("INSERT INTO users(user_id, first_name, last_name, username, date, language_code, is_premium) VALUES(?, ?, ?, ?, ?, ?, ?)", data)


    def get_users(self):
        with sqlite3.connect(self.connection) as db:
            cursor = db.cursor()
            data = ""

            for fname, lname, id, usern in cursor.execute("SELECT first_name, last_name, user_id, username FROM users"):
                data = data + str(f"id={html.code(id)} @{usern} - {fname} {lname}\n")
            return data


    def get_user_info(self, user_id):
        with sqlite3.connect(self.connection) as db:
            cursor = db.cursor()

            cursor.execute("SELECT first_name, last_name, user_id, username, date, language_code, is_premium FROM users WHERE user_id = ?", [user_id])
            # print(cursor.fetchone())
            return cursor.fetchone()

