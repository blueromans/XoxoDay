import os
import sys
import sqlite3 as lite

from XoxoDay.exception import XoxoDayException

sql_path = f'{os.path.dirname(os.path.abspath(__file__))}/xoxo.sqlite'

ROOT_DIR = sys.path[1]


def initialize_sql_lite():
    try:
        with lite.connect(sql_path) as sqlite:
            cursor = sqlite.cursor()
            query = "CREATE TABLE IF NOT EXISTS jwt (token json)"
            cursor.execute(query)
            sqlite.commit()
    except Exception as e:
        raise XoxoDayException(e)


def get_cookie():
    f = open(f'{ROOT_DIR}/xoxo_cookie', "r")
    cookie = f.read()
    f.close()
    return cookie
