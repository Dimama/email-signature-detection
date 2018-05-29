"""Модуль, выполняющий загрузку данных в БД, обучение классификатора
и его сохранение

usage: python init.py option
    option:
        --all-setup  - заполнение БД и обучение
        --setup-db - заполнение таблиц БД
        --learn - обучение классификатора
        --clear-db - очищение таблиц в бд
"""

import sys
import db
from classifier import Classifier
from const import CLASSIFIER_PATH


def all_setup():
    setup_db()
    fit()

def setup_db():
    db.setup_db()
    db.fill_tables('dataset/dataset/with/', 1, 10)
    db.fill_tables('dataset/dataset/without/', -1, 10)

    print(db.count_sig_and_non_sig_lines())

def fit():
    c = Classifier.get_classifier()
    data = db.get_classifier_data()
    Classifier.train(c, data, 0.2,  CLASSIFIER_PATH)

def clear_db():
    db.clear_tables()


if __name__ == '__main__':
    
    try:
        option = sys.argv[1]

        if option == '--all-setup':
            all_setup()
        elif option == '--setup-db':
            setup_db()
        elif option == '--learn':
            fit()
        elif option == '--clear-db':
            clear_db()
        else:
            print("Unknown option.")

    except IndexError:
        print("Set an option.")


    
