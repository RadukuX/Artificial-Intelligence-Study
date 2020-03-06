from flaskai.repository.user_repository import UserRepository


class UserService:

    user_repo = UserRepository()

    def login_user(self, email, password):
        return self.user_repo.login_user(email, password)

    def register_user(self, username, email, password):
        return self.user_repo.register_user(username, email,password)