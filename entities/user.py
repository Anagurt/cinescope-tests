from clients.api_manager import ApiManager


class User:

    def __init__(self, id: str, email: str, password: str, roles: list,
                 api: ApiManager) -> None:
        self.id = id
        self.email = email
        self.password = password
        self.roles = roles
        self.api = api

    @property
    def creds(self) -> tuple[str, str]:
        """Возвращает кортеж (email, password)"""
        return self.email, self.password
