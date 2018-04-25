"""Модуль, выполняющий загрузку данных в БД, обучение классификаторов
и их сохранение

usage: python init.py option
    option:
        --all-setup  - заполнение БД и обучение
        --setup-db - заполнение таблиц БД
        --learn - обучение классификаторов
        --learn-classifier - обучение первого классификатора
        --learn-extractor - обучение второго классификатора
        --clear-db - очищение таблиц в бд
"""

import sys
import db
from classifier import Classifier
from const import CLASSIFIER_PATH, EXTRACTOR_PATH


def all_setup():
    setup_db()
    learn()

def setup_db():
    db.setup_db()
    db.fill_tables('dataset/dataset/with/', 1, 10)
    db.fill_tables('dataset/dataset/without/', -1, 10)

    print(db.count_sig_and_non_sig_lines())

def learn():
    learn_classifier()
    learn_extractor()


def learn_classifier():
    c = Classifier.get_classifier()
    data = db.get_classifier_data()
    Classifier.train(c, data, 0.5,  CLASSIFIER_PATH)

def learn_extractor():
    c = Classifier.get_classifier()
    data = db.get_classifier_data(for_email=False)
    Classifier.train(c, data, 0.5, CLASSIFIER_PATH)


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
            learn()
        elif option == '--learn-classifier':
            learn_classifier()
        elif option == '--learn-extractor':
            learn_extractor()
        elif option == '--clear-db':
            clear_db()
        else:
            print("Unknown option.")

    except IndexError:
        print("Set an option.")


    
