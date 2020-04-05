from flaskai.repository.user_repository import UserRepository
from flask_bcrypt import Bcrypt


class UserService:

    team_dictionary_pl = {'Arsenal': 1, 'Aston Villa': 2, 'Bournemouth': 3, 'Brighton': 4, 'Burnley': 5, 'Chelsea': 6,
                          'Crystal Palace': 7, 'Everton': 8, 'Leicester': 9, 'Liverpool': 10, 'Manchester City': 11,
                          'Manchester United': 12, 'Newcastle': 13, 'Norwich': 14, 'Sheffield': 15, 'Southampton': 16,
                          'Tottenham': 17, 'Watford': 18, 'West Ham': 19, 'Wolves': 20}
                          
    user_repo = UserRepository()

    def login_user(self, email, password):
        return self.user_repo.login_user(email, password)

    def register_user(self, username, email, password):
        bcrypt = Bcrypt()
        hashed_password = bcrypt.generate_password_hash(str(password)).decode('utf-8')
        return self.user_repo.register_user(username, email, hashed_password, 0)

    def add_teams(self, team_list, current_user_email):
        lowercase_team_list = []
        for team in team_list:
            lowercase_team_list.append(team.lower().replace("-", "_"))
        print("team list in controller" + str(lowercase_team_list) + str(current_user_email))
        return self.user_repo.add_teams(lowercase_team_list, current_user_email)
    
    def check_subscription(self, email):
        result = self.user_repo.check_subscriptions(email)
        if not result:
            return False
        return True

    def get_your_teams(self, email):
        teams_id = self.user_repo.check_subscriptions(email)
        team_list_name = []
        key_list = list(self.team_dictionary_pl.keys())
        value_list = list(self.team_dictionary_pl.values())
        for team_id in teams_id:
            team_list_name.append(key_list[value_list.index(team_id)])
        return team_list_name
