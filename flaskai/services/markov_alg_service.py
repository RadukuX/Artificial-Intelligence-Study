from flaskai.algorithms.markov_alg import MarkovAlg


class MarkovService:

    markov = MarkovAlg()

    team_dictionary_pl = {'arsenal': 1, 'aston_villa': 2, 'bournemouth': 3, 'brighton': 4, 'burnley': 5, 'chelsea': 6,
                          'crystal_palace': 7, 'everton': 8, 'leicester': 9, 'liverpool': 10, 'manchester_city': 11,
                          'manchester_utd': 12, 'newcastle': 13, 'norwich': 14, 'sheffield': 15, 'southampton': 16,
                          'tottenham': 17, 'watford': 18, 'west_ham': 19, 'wolves': 20}

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
        return self.markov.markov_matrix(team_id, oponent_team)
