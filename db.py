"""Module for work with DB
"""


import peewee
from features import get_features_for_email
from os import listdir
from os.path import isfile, join
import hashlib

db = peewee.SqliteDatabase('signature.db')

class UntaggedData(peewee.Model):
    """Модель таблицы, содержащий тексты электронных писем, отправителей,
       списки признаков и значения для обучения
    """

    id = peewee.TextField(primary_key=True)
    text = peewee.TextField()
    sender = peewee.TextField()
    features = peewee.TextField(null=True) # строка признаков через запятую
    tag = peewee.IntegerField() # выходное значение: 1 - есть подпись, 0 - нет подписи

    class Meta:
        database = db


def setup_db():
    try:
        UntaggedData.create_table()
    except peewee.OperationalError:
        print("UntaggedData table already exist!")

def fill_untagged_data_table(dir, is_sign, count):
    """Заполнение таблицы электронных пием
    
        dir -- папка, содержащая письма
        is_sign -- признак того, есть ли в письмах подписи
        count -- количество последних строк письма, используемых для выделения признаков

    """

    files = [dir + f for f in listdir(dir) if isfile(join(dir, f)) and not f.count("_sender")]
    for file in files:
        with open(file, "r") as f_body, open(file + "_sender") as f_sender:
            body = f_body.readlines()
            sender = f_sender.readline()
            features = [str(item) for item in get_features_for_email(body, count, sender)]
            features = ','.join(features)
        md5_hash = md5(file)
        try:
            UntaggedData.create(id=md5_hash, text=body, sender=sender, features=features, tag=is_sign)
        except peewee.IntegrityError: # возникает при вставке тех же значений
            pass


def get_classifier_data(first=True):
    """Извлечение данных из таблицы для обучения классификатора
    """

    data = {"features": [], "tag": []}

    if first:
        selected_data = UntaggedData.select(UntaggedData.features, UntaggedData.tag).tuples()
    else:
        pass # данные для второго классификатора

    for feature, tag in selected_data:
        data["features"].append([int(x) for x in feature.split(',')])
        data["tag"].append(tag)

    return data

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

if __name__ == '__main__':
    setup_db()
    fill_untagged_data_table('dataset/with/', 1, 10)
    fill_untagged_data_table('dataset/without/', 0, 10)
    

    


