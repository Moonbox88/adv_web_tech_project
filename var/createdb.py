import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def main():
    database = "store.db"

    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                    uid integer PRIMARY KEY,
                                    firstname text NOT NULL,
                                    lastname text NOT NULL,
                                    email text NOT NULL,
                                    pwdhash text NOT NULL
                                ); """

    conn = create_connection(database)
    if conn is not None:
        create_table(conn, sql_create_users_table)
    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()
