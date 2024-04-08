from datetime import date
import psycopg2
import os

from dotenv import load_dotenv
load_dotenv()

from word.temp_word import read_doc, write_doc
def start_db(list_param):
    try:
        # подключаюсь к базе
        global connection
        connection = psycopg2.connect(host=os.getenv('host'),
                                      user=os.getenv('user'),
                                      password=os.getenv('password'),
                                      database=os.getenv('db_name'))
        connection.autocommit = True

        count_param = len(list_param)
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT version();"
            )

            print(f"версия сервера PostgreSQL: {cursor.fetchone()}")

        # создаем новую таблицу
        try:
            string_request = """CREATE TABLE users (id serial PRIMARY KEY, 
                                    user_id integer NOT NULL,  
                                    name varchar(50) NOT NULL,
                                    date_create date,
                                    date_pay date"""
            for i in range(count_param):
                string_request = f'{string_request}, param{i} float'
            string_request += ');'
            with connection.cursor() as cursor:
                cursor.execute(string_request)
                print("Таблица создана")
        except:
            print('Таблица уже существует')
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    # finally:
    #     if connection:
    #         connection.close()
    #         print("[INFO] PostgreSQL connection closed")

def write_user_db(id_user, first_name):
    # записываю нового пользователя, через проверку
    with connection.cursor() as cursor:
        cursor.execute(f'SELECT * FROM users WHERE user_id = {id_user};')
        if cursor.fetchone():
            print('пользователь уже записан')
        else:
            cursor.execute(
                f"INSERT INTO users (user_id, name, date_create) "
                f"VALUES ({id_user}, '{first_name}', '{date.today()}');")

def write_parametr_db(id_user, id_parametr, content):
    # записываю значения параметров
    with connection.cursor() as cursor:
        cursor.execute(f'UPDATE users SET param{id_parametr} = {content} WHERE user_id = {id_user};')
def write_pay_db(id_user):
    # ввожу дату платежа
    with connection.cursor() as cursor:
        cursor.execute(f"UPDATE users SET date_pay = '{date.today()}' WHERE user_id = {id_user};")

def read_calc_write(id_user, list_param):
    # расчет и запись в базу
    with connection.cursor() as cursor:
        # чтение параметров из базы
        count_param = len(list_param)
        string_request = 'SELECT '
        for i in range(count_param-1):
            string_request += f'param{i}, '
        string_request = f" {string_request} param{count_param-1} FROM users WHERE user_id={id_user};"
        cursor.execute(string_request)
        dict_param = dict(zip(list_param, cursor.fetchone()))
        print(dict_param)
        write_doc(dict_param)


if __name__ == '__main__':
    list_param = read_doc()
    start_db(list_param)
    read_calc_write(id_user=177378414, list_param=list_param)