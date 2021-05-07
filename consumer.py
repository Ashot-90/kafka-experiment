from kafka import KafkaConsumer
from json import loads
import os
import sys
import psycopg2


def create_table():
    # Establishing the connection
    conn = psycopg2.connect(
        dbname='mydb',
        user='postgres',
        password='postgres',
        host='db',
        port='5432'
    )
    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # Doping availability table if already exists.
    cursor.execute("DROP TABLE IF EXISTS availability")
    # Creating table as per requirement
    sql = '''CREATE TABLE availability(
        url VARCHAR ( 20 ) NOT NULL,
        time BIGINT NOT NULL,
        response_time FLOAT,
        response_code INT,
        regexp VARCHAR ( 20 ) NOT NULL,
        regexp_found BOOLEAN,
        id SERIAL PRIMARY KEY
    )'''
    cursor.execute(sql)
    conn.commit()
    print("Table created successfully........")

    # Closing the connection
    conn.close()


def insert_data(url, time, response_time, response_code, regexp, regexp_found):
    # Establishing the connection
    conn = psycopg2.connect(
        dbname='mydb',
        user='postgres',
        password='postgres',
        host='db',
        port='5432'
    )
    # Setting auto commit false
    #conn.autocommit = True

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # Preparing SQL queries to INSERT a record into the database.
    cursor.execute("INSERT INTO availability (url, time, response_time, response_code, regexp, regexp_found) VALUES ('{}', {}, {}, {}, '{}', {})".format(url, time, response_time, response_code, regexp, regexp_found))

    # Commit your changes in the database
    conn.commit()
    print("Records inserted........")

    # Closing the connection
    conn.close()


def start_consumer():
    try:
        create_table()
    except Exception:
        print("Error: Table has not been created\n", file=sys.stderr)
        sys.exit(1)
    try:
        topic = os.environ['TOPIC']
    except KeyError:
        print("Error: Environment variable has not found\n", file=sys.stderr)
        sys.exit(1)
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=['kafka:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group',
        value_deserializer=lambda x: loads(x.decode('utf-8')))
    for message in consumer:
        dict_message = dict(message.value)
        print('URL is :', dict_message.get('url'))
        print('TIME is :', dict_message.get('time'))
        print('RESPONSE_CODE is :', dict_message.get('response_code'))
        print('RESPONSE_TIME is :', dict_message.get('response_time'))
        print('REGEXP is :', dict_message.get('regexp'))
        print('REGEXP_FOUND is :', dict_message.get('regexp_found'))
        insert_data(url=dict_message.get('url'),
                    time=dict_message.get('time'),
                    response_time=dict_message.get('response_time'),
                    response_code=dict_message.get('response_code'),
                    regexp=dict_message.get('regexp'),
                    regexp_found=dict_message.get('regexp_found')
                    )


if __name__ == '__main__':
    start_consumer()
