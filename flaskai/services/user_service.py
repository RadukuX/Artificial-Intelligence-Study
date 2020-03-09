from flaskai.repository.user_repository import UserRepository
from flask_bcrypt import Bcrypt


class UserService:

    user_repo = UserRepository()

    def login_user(self, email, password):
        return self.user_repo.login_user(email, password)

    def register_user(self, username, email, password):
        bcrypt = Bcrypt()
        hashed_password = bcrypt.generate_password_hash(str(password)).decode('utf-8')
        return self.user_repo.register_user(username, email, hashed_password)