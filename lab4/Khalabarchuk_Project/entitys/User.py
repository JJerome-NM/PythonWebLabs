
class User:

    def __init__(self, login: str, password: str):
        self.login = str(login)
        self.password = password

    def __eq__(self, other):
        if isinstance(other, User):
            return self.login == other.login and self.password == other.password
        return False

    def __hash__(self):
        return hash((self.login, self.password))
