from flaskai.algorithms.naive_bayes_alg import NaiveBayesAlg


class NaiveBayesService:

    naive_bayes = NaiveBayesAlg()

    '''
        :returns procent_of_win, procent_of_equal, procent_of_defeat, accuarcy
    '''
    def calculate(self, my_team, oponent):
        print(my_team)
        str1 = str(my_team)
        str2 = str1.replace("-", "_")
        return self.naive_bayes.calculate(str2.lower(), oponent)


n = NaiveBayesService()
print(n.calculate('Aston-Villa', 'Liverpool FC'))