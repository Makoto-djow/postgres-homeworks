"""Скрипт для заполнения данными таблиц в БД Postgres."""

import psycopg2
import csv

db_connect = psycopg2.connect(
    host='localhost',
    database='north',
    user='postgres',
    password='dmaster8'
)

cursor_db = db_connect.cursor()


def open_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=',', quotechar='"')
        line_ = list(reader)
        return line_


employees = open_file('north_data/employees_data.csv')
customers = open_file('north_data/customers_data.csv')
orders = open_file('north_data/orders_data.csv')

try:
    for line in employees[1:]:
        employee_id, first_name, last_name, title, birth_date, notes = line
        cursor_db.execute('INSERT INTO employees VALUES (%s, %s, %s, %s, %s, %s)',
                          (employee_id, first_name, last_name, title, birth_date, notes))

    for line in customers[1:]:
        customer_id, company_name, contact_name = line
        cursor_db.execute('INSERT INTO customers VALUES (%s, %s, %s)',
                          (customer_id, company_name, contact_name))

    for line in orders[1:]:
        order_id, customer_id, employee_id, order_date, ship_city = line
        cursor_db.execute('INSERT INTO orders VALUES (%s, %s, %s, %s, %s)',
                          (order_id, customer_id, employee_id, order_date, ship_city))
except psycopg2.Error as e:
    print(f"Ошибка при заполнении таблицы: {e}")
finally:
    db_connect.commit()
