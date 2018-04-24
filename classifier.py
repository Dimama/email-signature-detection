"""Модуль для обучения и сохранения параметров классфикаторов
"""


from sklearn.externals import joblib
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from random import shuffle

def split_on_train_and_test(data, k=0.2):

    count = len(data['features'])
    indices = list(range(count))
    shuffle(indices)
    
    X = [data['features'][i] for i in indices]
    Y = [data['tag'][i] for i in indices]

    limit = count - int(k * count)

    return {
        "train": { "features": X[:limit], "tag": Y[:limit] },
        "test": { "features": X[limit:], "tag": Y[limit:] },
    }
    
    

def train(classifier, data, filename_to_save=None):
    
    splitted_data = split_on_train_and_test(data)
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
    print("\taccuracy train: ", accuracy_score(test['tag'] , predicted))

    print(classification_report(test['tag'], predicted))
    print(confusion_matrix(test['tag'] , predicted))

def load(filename_from_load):
    try:
        return joblib.load(filename_from_load)
    except FileNotFoundError:
        print("No such file:", filename_from_load)
        return None
    except Exception:
        print("Incorrect file")
        return None
        
def get_classifier():
    return LinearSVC(C=10.0)


