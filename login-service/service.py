class LoginService:
    def __init__(self, login_repository):
        self.login_repository = login_repository

    def add_user(self, user) -> bool:
        return self.login_repository.add_user(user)

    def check_credentials(self, user) -> bool:
        return self.login_repository.check_credentials(user)
