from flaskai.repository.repository import Repository
import numpy as np
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from collections import Counter


class NaiveBayesAlg:

    repository = Repository()

    def prepare_data(self, my_team, oponent):
        raw_data = self.repository.get_goals_result(my_team, oponent)
        for i in raw_data:
            if i[2] == 'v':
                i[2] = '1'
            elif i[2] == 'e':
                i[2] = '2'
            elif i[2] == 'd':
                i[2] = '3'
        for i in raw_data:
            i[0] = int(i[0])
            i[1] = int(i[1])
            i[2] = int(i[2])
        return np.asarray(raw_data)

    def calculate(self, my_team, oponent):
        raw_data = self.prepare_data(my_team, oponent)
        dataset = pd.DataFrame({'goals_given': raw_data[:, 0], 'goals_taken': raw_data[:, 1], 'result': raw_data[:, 2]})
        target = dataset.result
        inputs = dataset.drop('result', axis='columns')
        X_train, X_test, y_train, y_test = train_test_split(inputs, target, test_size=0.3)
        model = MultinomialNB()
        model.fit(X_train, y_train)
        list_of_predictions = model.predict(X_test)
        print(list_of_predictions)
        dictionary_of_predictions = dict(Counter(list_of_predictions))
        if dictionary_of_predictions.get(1) is None:
            nr_of_pred_wins = 0
        else:
            nr_of_pred_wins = int(str(dictionary_of_predictions.get(1)))

        if dictionary_of_predictions.get(2) is None:
            nr_of_pred_equals = 0
        else:
            nr_of_pred_equals = int(str(dictionary_of_predictions.get(2)))

        if dictionary_of_predictions.get(3) is None:
            nr_of_pred_defeats = 0
        else:
            nr_of_pred_defeats = int(str(dictionary_of_predictions.get(3)))

        total_of_games_predicted = nr_of_pred_wins + nr_of_pred_defeats + nr_of_pred_equals
        procent_of_wins = nr_of_pred_wins/total_of_games_predicted * 100
        procent_of_equals = nr_of_pred_equals/total_of_games_predicted * 100
        procent_of_defeats = nr_of_pred_defeats/total_of_games_predicted * 100
        accuarcy = model.score(X_test, y_test)

        return [procent_of_wins, procent_of_equals, procent_of_defeats, accuarcy]

