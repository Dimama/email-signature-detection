from classifier import Classifier
from sklearn import svm, grid_search, neighbors, naive_bayes, model_selection
from sklearn.metrics import make_scorer, precision_score, recall_score, f1_score, accuracy_score

import db
import k_neighbors

import matplotlib.pyplot as plt
import numpy as np

def diagramms(precision, recall, f1):
    
    own = [precision[0]*100, recall[0]*100, f1[0]*100]
    sk = [precision[1]*100, recall[1]*100, f1[1]*100]
    n_groups = 3

    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.25
    opacity = 0.7
    
    rects1 = plt.bar(index, own, bar_width,
                 alpha=opacity,
                 color='r',
                 hatch='=',
                 label='Diploma')
 
    rects2 = plt.bar(index + bar_width, sk, bar_width,
                 alpha=opacity,
                 color='g',
                 hatch='//',
                 label='Scikit')

    plt.xlim(-0.5, 3)
    plt.axis
    plt.ylabel('%')
    plt.xticks(index, ('Точность', 'Полнота', 'F-мера'))
    plt.legend()

    for i in range(3):
        plt.text(i, own[i]+2, str(own[i])[0:2] + "    " +  str(sk[i])[0:2])

    plt.tight_layout()
    plt.show()



def methods_diagramms(precision, recall, f1):
    objects = ('SVM', 'K-neighbors', 'Naive Bayes',)

    print(precision)
 
    x = range(3)
    y = precision
    plt.bar(x, y)
    for a,b in zip(x, y):
        plt.text(a-0.1 , b, str(b)[0:4])

    plt.xticks(x, objects)
    plt.ylabel('Precision')
 
    plt.show()

    y = recall
    plt.bar(x, y)
    for a,b in zip(x, y):
        plt.text(a-0.1 , b, str(b)[0:4])

    plt.xticks(x, objects)
    plt.ylabel('Recall')
 
    plt.show()

    y = f1
    plt.bar(x, y)
    for a,b in zip(x, y):
        plt.text(a-0.1 , b, str(b)[0:4])

    plt.xticks(x, objects)
    plt.ylabel('F-measure')
 
    plt.show()

def getScores(estimator, x, y):
    yPred = estimator.predict(x)
    return (f1_score(y, yPred), 
            precision_score(y, yPred, pos_label=3, average='macro'), 
            recall_score(y, yPred, pos_label=3, average='macro'))

def my_scorer(estimator, x, y):
    a, p, r = getScores(estimator, x, y)
    #print(a, p, r)
    return a+p+r

def get_metrics_for_method(model):
    data = db.get_classifier_data()

    splitted_data = Classifier.split_on_train_and_test(data, 0.2)
    train = splitted_data['train']
    test = splitted_data['test']
    
    res = model.fit(train['features'], train['tag'])
    predicted = model.predict(test['features'])

    f1 = f1_score(test['tag'], predicted)
    pr = precision_score(test['tag'], predicted, pos_label=3, average='macro')
    re = recall_score(test['tag'], predicted, pos_label=3, average='macro')

    print(f1, pr, re)
    metrics_dict = {"precision": None,
    "recall": None,
    "f1": None
    }

    return metrics_dict



def k_neighbors_param_optimization():
    data = db.get_classifier_data()

    k = [i for i in range(3, 100) if i % 2 == 1]
    
    parameters = {'n_neighbors': k}
    KN = neighbors.KNeighborsClassifier()
    scoring='recall'
    clf = grid_search.GridSearchCV(KN, parameters, cv=10)

    clf.fit(data['features'], data['tag'])
    
    y1 = []
    for item in clf.grid_scores_:
        print(item)
        y1.append(item.mean_validation_score)

    y2 = []
    splitted_data = Classifier.split_on_train_and_test(data, 0.2)
    train = splitted_data['train']
    test = splitted_data['test']
    
    for val in k:
        classifier = k_neighbors.MyKNeighborsClassifier(val)

        classifier.fit(data['features'], data['tag'])
        predicted = classifier.predict(train['features'])
        print("\taccuracy train: ", accuracy_score(train['tag'] , predicted))
        y2.append(accuracy_score(train['tag'] , predicted))

    return k, y1, y2

def k_neighbors_graphics(x, y1, y2):
    
    plt.title("Алгоритм k-ближайших соседей")
    plt.xlabel("k")
    plt.ylabel("Accuracy")
    
    sk, own = plt.plot(x, y1, 'go:', x, y2, 'r^:',)

    plt.legend((sk, own), (u'scikit', u'diploma'), loc = 'lower right')

    plt.grid(which='minor', alpha=0.2)
    plt.grid(True, linestyle='-', color='0.75')
    plt.show()

def svm_graphics(x, y):

    plt.title("Алгоритм опорных векторов")
    plt.xlabel("C")
    plt.ylabel("recall")
    
    linear, rbf, poly, sigmoid = plt.plot(x, y['linear'], 'bD:',
                                          x, y['rbf'], 'r^:',
                                          x, y['poly'], 'go:',
                                          x, y['sigmoid'], '.:')

    plt.legend( (linear, rbf, poly, sigmoid),
                     (u'linear', u'rbf', u'poly', u'sigmoid'), loc = 'best')

    plt.grid(True, linestyle='-', color='0.75')
    plt.show()

def svm_param_optimization(k=0.2):

    data = db.get_classifier_data()

    c = [(i+1)*0.5 for i in range(20)]
    
    parameters = {'kernel':('linear', 'rbf', 'poly', 'sigmoid'), 'C':c}
    svc = svm.SVC()
    scoring='recall'
    clf = grid_search.GridSearchCV(svc, parameters, cv=10)

    clf.fit(data['features'], data['tag'])
    
    y = {'linear': [],
        'rbf': [],
        'poly': [],
        'sigmoid': []
    }

    for item in clf.grid_scores_:
        func = item.parameters['kernel']
        y[func].append(item.mean_validation_score)

    return c, y


if __name__ == '__main__':
    
    #svm_metrics = get_metrics_for_method(svm.SVC(C=5.0))
    #k_neighbors_metrics = get_metrics_for_method(neighbors.KNeighborsClassifier(n_neighbors=22))
    #bayes_metrics = get_metrics_for_method(naive_bayes.GaussianNB())

    #x, y1, y2 = k_neighbors_param_optimization()

    #k_neighbors_graphics(x, y1, y2)
    #x, y = svm_param_optimization()
    #svm_graphics(x, y)

    recall = [0.92257, 0.9154]
    precision = [0.948774, 0.92458]

    f1 = []
    for i in range(len(recall)):
        f1.append(2*recall[i]*precision[i]/(recall[i]+precision[i]))

    diagramms(precision, recall, f1)