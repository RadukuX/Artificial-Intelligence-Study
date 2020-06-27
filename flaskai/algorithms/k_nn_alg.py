from sklearn import neighbors
from sklearn.model_selection import train_test_split

import numpy as np
import pandas as pd


class KNearestNeighbors:

    def knn(self, investments, medium_age, wins, equals, defeats, goals):
        df = pd.read_excel(r"D:\Artificial Intelligence Study\flaskai\excel_data\extra_data\Extra Data Liverpool.xlsx")
        df.drop(['Year'], 1, inplace=True)
        X = np.array(df.drop(['Place'], 1))
        y = np.array(df['Place'])

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        clf = neighbors.KNeighborsClassifier()
        clf.fit(X_train, y_train)
        accuarcy = clf.score(X_train, y_train)

        prediction = np.array([investments, medium_age, wins, equals, defeats, goals])
        result = clf.predict([prediction])
        return [int(result), accuarcy]

#l= KNearestNeighbors()
#print(l.knn(46000000, 21.4, 30, 8, 10, 57))