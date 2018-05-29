"""Модуль для обучения и сохранения параметров классфикаторов
"""


from sklearn.externals import joblib
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from random import shuffle
from features import get_features_for_email, get_features_for_line


class Classifier(object):
    """Класс, содержащий методы для определения наличия подписи в письме
    и классификации строк письма по признаку подпись/не подпись
    """

    def __init__(self, classifier_filename):
        """Загрузка обученных классификаторов из файлов
        """
        try:
            self.classifier = self._load(classifier_filename)
        except ClassifierException as e:
            raise e


    def test_classifier(self, data, classifier):
        pass

    
    def check_line_for_signature(self, line, sender):
        """Метод для определения того, является ли строка подписью
        """

        features = get_features_for_line(line, sender)
        res = self.classifier.predict([features])
        
        print("Features: ", features)
        print("Res:", res[0])
        
        if res[0] == 1:
            return True
        return False

    def _get_tag_for_features(self, features, classifier):
        """Метод, возвращающий результат работы заданного обученного
        классификатора на заданном списке признаков
        """

        return 1


    def _load(self, filename_from_load):
        try:
            return joblib.load(filename_from_load)
        except FileNotFoundError:
            raise ClassifierException("No such file '{}'".
                format(filename_from_load))
        except Exception:
            raise ClassifierException("Incorrect file '{}'".
                format(filename_from_load))

    @staticmethod
    def split_on_train_and_test(data, k=0.2):

        count = len(data['features'])
        indices = list(range(count))
        shuffle(indices)
    
        X = [data['features'][i] for i in indices]
        Y   = [data['tag'][i] for i in indices]

        limit = count - int(k * count)

        return {
            "train": { "features": X[:limit], "tag": Y[:limit] },
            "test": { "features": X[limit:], "tag": Y[limit:] },
        }
    
    @staticmethod
    def train(classifier, data, k, filename_to_save=None):
    
        splitted_data = Classifier.split_on_train_and_test(data, k)
        train = splitted_data['train']
        test = splitted_data['test']
 
        res = classifier.fit(train['features'], train['tag'])

        if filename_to_save:
            print("Classifier saved to:", filename_to_save)
            joblib.dump(classifier, filename_to_save)
        print(res)

        predicted = classifier.predict(train['features'])
        print("\taccuracy train: ", accuracy_score(train['tag'] , predicted))

        predicted = classifier.predict(test['features'])
        print("\taccuracy test: ", accuracy_score(test['tag'] , predicted))

        print(classification_report(test['tag'], predicted, target_names=['no sign', 'sign']))
        print(confusion_matrix(test['tag'] , predicted))
        
    @staticmethod
    def get_classifier():
        return LinearSVC(C=10.0)


class ClassifierException(BaseException):
    """Класс исключений, возникающих в методах класса Classifier
    """
    pass

