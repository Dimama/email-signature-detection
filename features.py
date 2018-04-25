"""Модуль для получения векторов признаков, используемых для 
обучения и работы нейронной сети
"""

import re
import unicodedata
from functools import reduce

MAX_SIGNATURE_LINE_LEN = 60
HEADWORD_PERCENT = 66

RE_EMAIL = re.compile(r'[a-zA-Z0-9_.#$&!\'=/^?~{|}+-]'
                      r'+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

RE_URL = re.compile(r'(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?')

RE_SEPARATOR = re.compile(r'^[\s]*[-]{1,10}[\s]*$')

RE_SPEC_SYMBOLS = re.compile(r'^[\s]*([\*]|#|[\+]|[\^]|-|[\~]|[\&]|[\$]|_|[\!]'
                             r'|[\/]|[\%]|[\:]|[\=]){10,}[\s]*$')

RE_TEL_NUMBER = re.compile(r'(((\+?[\d]{,1}\s?\(?[\d]{3,4}\)?\s?)|'
    r'([\d]\-[\d]{3}\-))[\d]{2,3}[\s-]?[\d]{2}[\s-]?[\d]{2})|'
    r'(\(? ?[\d]{2,3} ?\)?[.\- ]{,1})[\d]{2,3}[.\- ]{,1}[\d]{2,4}')

RE_STANDART_SING_WORDS = re.compile(r'(T|t)hank.*,|(B|b)est|(R|r)egards|'
        r'^sent[ ]{1}from[ ]{1}my[\s,!\w]*$|BR|(S|s)incerely|'
        r'(C|c)orporation|Group|(О|o)тправлено\sс*|(С|с)\s(У|у)важением|'
        r'(У|y)дачного|(Х|х)орошего|(В|в)ам|доброго|(С|с)пасибо')

RE_NAME = re.compile(r'([A-Z][a-z]+\s\s?[A-Z][\.]?\s\s?[A-Z][a-z]+)'
    r'|[A-Z][a-z]+\s\s?[A-Z][a-z]+'
    r'|([А-ЯЁ][а-яё]+[\-\s]?){2,}'
    r'|([А-ЯЁ][а-яё]+\s[А-ЯЁ]\.?\s?[А-ЯЁ]\.?)'
    r'|([А-ЯЁ]\.?\s?[А-ЯЁ]\.?)\s[А-ЯЁ][а-яё]+')

STANDART_NAMES = ['gmail', 'mail', 'yandex', 'yahoo',
                 'com', 'ru', 'net', 'org']


def headword_percent(s):
    """Процент слов с заглавной буквы в строке
    """

    words = s.split()
    words = [w for w in words if w.strip() and len(w) > 2]
    valid_count = 0
    headword_count = 0
    for word in words:
        if not re.match(r'\(|\+|[\d]', word):
            valid_count += 1
            if word[0].isupper() and not word[1].isupper():
                headword_count += 1
    if valid_count > 0 and len(words) > 1:
        return 100 * float(headword_count) / valid_count

    return 0


def headword_more_than(s):
    return 1 if headword_percent(s) >= HEADWORD_PERCENT else 0


def categories_percent(s, catagories):
    """Процент символов заданных категорий
    """

    count = 0
    for c in s:
        if unicodedata.category(c) in catagories:
            count += 1
    return 100 * float(count) / len(s)


def punct_percent(s):
    """Процент пунктуационных символов
    """

    return categories_percent(s, ['Po'])


def extract_names(sender):
    """Извлекает имена из заголовка 'From:'
    """

    sender = ''.join([c if c.isalpha() else ' ' for c in sender])
    names = [name for name in sender.split() if len(name) > 1 and name not in STANDART_NAMES]
    names = list(set(names))

    return names


def is_contain_sender_name(sender):
    """Возвращает функцию для поиска имени отправителя
    """
    names = [name.capitalize() for name in extract_names(sender)]
    names += extract_names(sender)
    names = list(set(names))

    names_re = '( |$)|'.join(names)

    if names_re != '':
        return regex_search(re.compile(names_re))
    return lambda s: 0
    

def regex_search(pattern):
    return lambda x: 1 if pattern.search(x) else 0


def get_features_func_list(sender=''):
    """Возвращает список функций для признаков
    """

    return [
        regex_search(RE_EMAIL),
        regex_search(RE_URL),
        regex_search(RE_SEPARATOR),
        regex_search(RE_SPEC_SYMBOLS),
        regex_search(RE_TEL_NUMBER),
        regex_search(RE_NAME),
        regex_search(RE_STANDART_SING_WORDS),
        headword_more_than,
        lambda s: 1 if punct_percent(s) > 50 else 0,
        lambda s: 1 if punct_percent(s) > 90 else 0,
        lambda s: 0 if len(s) > MAX_SIGNATURE_LINE_LEN else 1,
        is_contain_sender_name(sender)
    ]


def get_features_for_line(line, sender=''):
    """Функция получения вектора признаков для строки
    """ 
    
    res =  [f(line) for f in get_features_func_list(sender)]
    
    #print("------------")
    #print("Sender:", sender)
    #print("Line:", line)
    #print(res)
    #print("------------")

    return res


def get_features_for_email(lines, count=10, sender=''):
    """Функция получения вектора признаков для письма
    Используется для определения, содержится ли подпись в письме

        lines {[list]} -- [список строк электронного письма]
        count {[int]} -- [количество последних строк письма, используемых для выделения признаков]
        sender {[str]} -- [имя отправителя] (default: {None})
    
    Return:
        список признаков
    """

    lines = [l for l in lines if l.strip()] 
    lines = lines[-count:]
    
    features_for_lines = [get_features_for_line(line, sender) for line in lines]

    return reduce(lambda x, y: [i + j for i,j in zip(x, y)], features_for_lines)
