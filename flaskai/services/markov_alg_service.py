from flaskai.algorithms.markov_alg import MarkovAlg


class MarkovService:

    markov = MarkovAlg()

    team_dictionary_pl = {'Arsenal': 1, 'Aston-Villa': 2, 'Bournemouth': 3, 'Brighton': 4, 'Burnley': 5, 'Chelsea': 6,
                          'Crystal-Palace': 7, 'Everton': 8, 'Leicester': 9, 'Liverpool': 10, 'Manchester-City': 11,
                          'Manchester-Utd': 12, 'Newcastle': 13, 'Norwich': 14, 'Sheffield': 15, 'Southampton': 16,
                          'Tottenham': 17, 'Watford': 18, 'West-Ham': 19, 'Wolves': 20}

    '''
        :returns wins, equals, defeats and the number of all the games 
    '''
    def informations(self, my_team, oponent_team):
        team_id = self.team_dictionary_pl.get(my_team)
        return self.markov.informations(team_id, oponent_team)

    '''
        :returns the probability matrix
    '''
    def markov_alg(self, my_team, oponent_team, result, power):
        team_id = self.team_dictionary_pl.get(my_team)
        return self.markov.markov(team_id, oponent_team, result, power)

    ''' 
        :returns markov matrix
    '''
    def markov_matrix(self, my_team, oponent_team):
        team_id = self.team_dictionary_pl.get(my_team)
        print("asd "+str(team_id)+"das")
        print(oponent_team)
        return self.markov.markov_matrix(team_id, oponent_team)
