import math

class MyKNeighborsClassifier():

    def __init__(self, k):
        self._k = k

    def fit(self, train_x, train_y):
        self._train_data = []

        for i in range(len(train_x)):
            self._train_data.append((train_x[i], train_y[i]))

        self._class_count = len(set(train_y))
        self._labels = list(set(train_y))

        return "My onw k-Neighbors Classifier with k={0}".format(self._k)

    def predict(self, x):
        
        res = []

        for obj in x:
            counts = [0] * len(self._labels)    
            labels = self._calculate_distances(obj)
            
            # подсчет количества объектов каждгого класса
            for label in labels:
                index = self._labels.index(label)
                counts[index] += 1

            max_elem = max(counts)
            pos_max_elem = counts.index(max_elem)

            res.append(self._labels[pos_max_elem]) 

        return res

    def _calculate_distances(self, obj):
        
        distances = []

        # поиск расстояния до всех объектов
        for item in self._train_data:
            dist = self._euclidian_distance(obj, item[0])
            distances.append((dist, item[1]))

        # сортировка по расстоянию
        distances.sort(key=lambda item: item[0])

        #print(distances)

        # отсортированные значения классов
        labels = [item[1] for item in distances]

        return labels[:self._k]

    def _euclidian_distance(self, p1, p2):
        sum = 0
        for i in range(len(p1)):
            sum += (p1[i] - p2[i])**2
        return math.sqrt(sum)
