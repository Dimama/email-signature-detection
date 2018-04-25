"""Module for work with DB
"""


import hashlib
import re
from os import listdir
from os.path import isfile, join
import peewee
from const import DB_NAME
from features import get_features_for_email, get_features_for_line

db = peewee.SqliteDatabase(DB_NAME)

class EMailTable(peewee.Model):
    """Модель таблицы, содержащей тексты электронных писем, отправителей,
       списки признаков и значения для обучения
    """

    id = peewee.TextField(primary_key=True)
    body = peewee.TextField()
    sender = peewee.TextField()
    features = peewee.TextField() # строка признаков через запятую
    tag = peewee.IntegerField() # выходное значение: 1 - есть подпись, -1 - нет подписи

    class Meta:
        database = db

class LinesTable(peewee.Model):
    """Модель таблицы, содержащей строки электронных писем,
       списки признаков и значения для обучения
    """
    line = peewee.TextField(primary_key=True)
    features = peewee.TextField()
    tag = peewee.IntegerField()

    class Meta:
        database = db


def setup_db():
    try:
        EMailTable.create_table()
    except peewee.OperationalError:
        print("EMailTable table already exist!")

    try:
        LinesTable.create_table()
    except peewee.OperationalError:
        print("Lines table already exist!")


def fill_lines_table(lines, sender):
    for line in lines:
        
        if re.match(r'#sig#', line):
            line = re.sub(r'#sig#', '', line)
            tag = 1
        else:
            tag = -1

        features = [str(item) for item in get_features_for_line(line, sender)]
        features = ','.join(features)
        
        try:
            LinesTable.create(line=line, features=features, tag=tag)
        except peewee.IntegrityError:
            pass
            #print("IntegrityError", line)


def count_sig_and_non_sig_lines():
    """Возвращает количество строк с подписью и без
    """

    return (
        LinesTable.select().where(LinesTable.tag == 1).count(),
        LinesTable.select().where(LinesTable.tag == -1).count()
    )


def fill_tables(dir, is_sign, count):
    """Заполнение таблиц в бд
    
        dir -- папка, содержащая письма
        is_sign -- признак того, есть ли в письмах подписи
        count -- количество последних строк письма, используемых для выделения признаков

    """

    files = [dir + f for f in listdir(dir) if isfile(join(dir, f)) and not f.count("_sender")]
    for file in files:
        with open(file, "r") as f_body, open(file + "_sender") as f_sender:
            body = f_body.read().split('\n')
            sender = f_sender.readline()

            non_empty_lines = [l for l in body if l.strip()]
            fill_lines_table(non_empty_lines, sender)
            
            if is_sign == 1:
                body = [re.sub(r'#sig#', '', line) for line in body]
            features = [str(item) for item in get_features_for_email(body, count, sender)]
            features = ','.join(features)

        md5_hash = md5(file)
        try:
            EMailTable.create(id=md5_hash, body=body, sender=sender, features=features, tag=is_sign)
        except peewee.IntegrityError: # возникает при вставке тех же значений
            pass
            #print("IntegrityError")


def get_classifier_data(for_email=True):
    """Извлечение данных из таблицы для обучения классификатора
    """

    data = {"features": [], "tag": []}

    if for_email:
        selected_data = EMailTable.select(EMailTable.features, EMailTable.tag).tuples()
    else:
        selected_data = LinesTable.select(LinesTable.features, LinesTable.tag).tuples()

    for feature, tag in selected_data:
        data["features"].append([int(x) for x in feature.split(',')])
        data["tag"].append(tag)

    return data


def clear_tables():
    EMailTable.drop_table()
    LinesTable.drop_table()


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

