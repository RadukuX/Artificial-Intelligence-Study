from flaskai.repository.team_repository import TeamRepository


class TeamService:

    team_dictionary_pl = {'arsenal': 1, 'aston-villa': 2, 'bournemouth': 3, 'brighton': 4, 'burnley': 5, 'chelsea': 6,
                          'crystal palace': 7, 'everton': 8, 'leicester': 9, 'liverpool': 10, 'manchester-city': 11,
                          'manchester-united': 12, 'newcastle': 13, 'norwich': 14, 'sheffield': 15, 'southampton': 16,
                          'tottenham': 17, 'watford': 18, 'west-ham': 19, 'wolves': 20}

    team_repo = TeamRepository()

    def get_info(self, team_name):
        team_id = self.team_dictionary_pl[team_name]
        return self.team_repo.get_info(team_id)