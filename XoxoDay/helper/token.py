import os
import sys

from XoxoDay.exception import XoxoDayException
from XoxoDay.serializer import Serializer

file_path = f'{os.path.dirname(os.path.abspath(__file__))}/xoxo'

ROOT_DIR = sys.path[1]


def get_token():
    try:
        with open(file_path, "r") as file:
            token_dict = file.read()
            if token_dict is not None:
                token_dict = Serializer.loads(token_dict[0])
            file.close()
            return token_dict
    except Exception as e:
        with open(file_path, 'w') as creating_new_xoxo_file:
            return
        raise XoxoDayException(e)


def update_token(token):
    try:
        with open(file_path, "wb") as file:
            file.write(Serializer.dumps(token))
            file.close()
    except Exception as e:
        raise XoxoDayException(e)


def get_cookie():
    f = open(f'{ROOT_DIR}/xoxo_cookie', "r")
    cookie = f.read()
    f.close()
    return cookie
