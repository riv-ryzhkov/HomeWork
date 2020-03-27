import sqlite3
import random
import string

from flask import Flask, request

app = Flask(__name__)  # __main__


def gen_password(len_password):
    chars = string.ascii_letters + string.digits + string.punctuation
    passw = ''.join([random.choice(chars) for _ in range(len_password)])
    out_put = 'Пароль для входа на эту страницу        ' + passw + '  количество символов в пароле' + str(len(passw))
    return out_put


def exec_query(query: str, params: tuple = None) -> list:

    try:
        conn = sqlite3.connect('./chinook.db')  # path to file
        cursor = conn.cursor()
        if params is None:
            cursor.execute(query)
        else:
            cursor.execute(query, params)
        result = cursor.fetchall()
    finally:
        conn.close()
    return result

# client -> request -> flask -> database -> flask -> response -> client

@app.route('/password/')
def password():
    # http://127.0.0.1:5000/password/?len_password
    try:
        len_pass = int(request.args.get('len_pass'))
        if len_pass > 0:
            result = gen_password(len_pass)
        else:
            result = 'NO PASSWORD'
    except:
        result = 'Недопустимый пароль'
    return result


@app.route('/State_City/')
def State_City():
    # http://127.0.0.1:5000/State_City/?state=NY&?city=NewYork
    state = request.args.get('state')
    city = request.args.get('city')
    if state:
        if city:
            query = f'SELECT * FROM Customers WHERE State=? AND City=?;'
            params = (state, city)
        else:
            query = f'SELECT * FROM Customers WHERE State=?;'
            params = (state,)
        result = exec_query(query, params)
    elif city:
        query = f'SELECT * FROM Customers WHERE City=?;'
        params = (city,)
        result = exec_query(query, params)
    else:
        query = f'SELECT * FROM Customers;'
        result = exec_query(query)
    return '<br>'.join(map(str, result))


@app.route('/First_Name/')
def First_Name():
    # http://127.0.0.1:5000/First_Name/
    query = f'SELECT COUNT (FirstName) FROM (SELECT * FROM customers GROUP BY FirstName);'
    result = exec_query(query)
    return '<br>'.join(map(str, result))


@app.route('/invoices/')
def invoices_items():
    # http://127.0.0.1:5000/invoices/
    query = 'SELECT SUM (UnitPrice * Quantity) FROM invoice_items;'
    result = exec_query(query)
    return str(result)

'''
1. Вью функция должна принимать параметр который регулирует количество символов (вью функция генерации 10 случайных символов)
/generate-password/?length=20 + validation, [20, 10000000000000000, -20, sefsefse]
2. Вью функция должна фильтровать таблицу кастомерс по Штату И Городу ?state=IL&city=Boston ?state=IL ?city=Boston NoParameters
3. Вью функция должна выводить количество уникальных имен (FirstName) из таблицы customers
4. Вывести общую прибыль из колонки invoice_items ((UnitPrice * Quantity) + ...)
'''