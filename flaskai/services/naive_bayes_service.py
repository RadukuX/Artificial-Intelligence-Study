from flaskai.algorithms.naive_bayes_alg import NaiveBayesAlg


class NaiveBayesService:

    naive_bayes = NaiveBayesAlg()

    '''
        :returns procent_of_win, procent_of_equal, procent_of_defeat, accuarcy
    '''
    def calculate(self, my_team, oponent):
        str1 = str(my_team)
        return self.naive_bayes.calculate(str1.lower(), oponent)