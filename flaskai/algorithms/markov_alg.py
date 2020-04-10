from flaskai.repository.repository import Repository
import numpy as np


class MarkovAlg:

    repo = Repository()

    def informations(self, team_id, opponent):
        first_states = self.repo.get_results_for_a_specific_team(team_id, opponent)
        result_dict = {'wins': 0, 'equals': 0, 'defeats': 0}
        nr_of_wins = 0
        nr_of_equals = 0
        nr_of_defeats = 0
        for t in first_states:
            if t[5] == 'v':
                nr_of_wins = nr_of_wins + 1
                result_dict['wins'] = nr_of_wins
            elif t[5] == 'e':
                nr_of_equals = nr_of_equals + 1
                result_dict['equals'] = nr_of_equals
            elif t[5] == 'd':
                nr_of_defeats = nr_of_defeats + 1
                result_dict['defeats'] = nr_of_defeats
        return result_dict, len(first_states)

    def calculate_percentage(self, team_id, oponent):
        result_dict = self.informations(team_id, oponent)[0]
        length = self.informations(team_id, oponent)[1]
        proc_of_wins = (result_dict['wins'] / length)
        proc_of_equals = (result_dict['equals'] / length)
        proc_of_defeats = (result_dict['defeats'] / length)
        t = (round(proc_of_wins, 2), round(proc_of_equals, 2), round(proc_of_defeats, 2))
        return t

    def get_chains(self, team_id, oponent):
        result = []
        for t in self.repo.get_results_for_a_specific_team(team_id, oponent):
            result.append(t[5])
        reversed_result = result[::-1]
        dictionary = {'v': '', 'e': '', 'd': ''}
        string1 = ''
        string2 = ''
        string3 = ''
        for i in range(len(reversed_result) - 1):
            if reversed_result[i] == 'v':
                string1 = string1 + reversed_result[i + 1]
            elif reversed_result[i] == 'e':
                string2 = string2 + reversed_result[i + 1]
            elif reversed_result[i] == 'd':
                string3 = string3 + reversed_result[i + 1]
        dictionary['v'] = string1
        dictionary['e'] = string2
        dictionary['d'] = string3
        return dictionary

    def markov_matrix(self, team_id, oponent):
        arr = []
        proc_of_wins = 0
        proc_of_equals = 0
        proc_of_defeats = 0
        dicty = self.get_chains(team_id, oponent)
        print(dicty)
        for key in dicty:
            nr_of_wins = 0
            nr_of_equals = 0
            nr_of_defeats = 0
            lg = 0
            for elem in dicty[key]:
                lg = lg + 1
                if elem == 'v':
                    nr_of_wins = nr_of_wins + 1
                elif elem == 'd':
                    nr_of_defeats = nr_of_defeats + 1
                elif elem == 'e':
                    nr_of_equals = nr_of_equals + 1
                proc_of_wins = (nr_of_wins / lg)
                proc_of_equals = (nr_of_equals / lg)
                proc_of_defeats = (nr_of_defeats / lg)
            list_of_proc = [round(proc_of_wins, 5), round(proc_of_equals, 5), round(proc_of_defeats, 5)]
            arr.append(list_of_proc)
            print('lista'+ str(list_of_proc))
        return np.asmatrix(arr).transpose()

    def first_state_matrix(self, the_result):
        first_state = []
        if the_result == 'v':
            win_state = [1]
            equal_state = [0]
            defeat_state = [0]
            first_state.append(win_state)
            first_state.append(equal_state)
            first_state.append(defeat_state)
            return np.asmatrix(first_state)
        elif the_result == 'e':
            win_state = [0]
            equal_state = [1]
            defeat_state = [0]
            first_state.append(win_state)
            first_state.append(equal_state)
            first_state.append(defeat_state)
            return np.asmatrix(first_state)
        elif the_result == 'd':
            win_state = [0]
            equal_state = [0]
            defeat_state = [1]
            first_state.append(win_state)
            first_state.append(equal_state)
            first_state.append(defeat_state)
            return np.asmatrix(first_state)

    def markov(self, team_id, oponent, result, power):
        raised_matrix = np.linalg.matrix_power(self.markov_matrix(team_id, oponent), power)
        first_matrix = self.first_state_matrix(result)
        return np.matmul(raised_matrix, first_matrix)
