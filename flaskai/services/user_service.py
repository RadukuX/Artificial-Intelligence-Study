from flaskai.repository.user_repository import UserRepository
from flask_bcrypt import Bcrypt


class UserService:

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