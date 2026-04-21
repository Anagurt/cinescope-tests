from requests import Session

from clients.auth_api import AuthAPI
from clients.movies_api import MoviesAPI
from clients.user_api import UserAPI


class ApiManager:
    """
    Класс для управления API-классами с единой HTTP-сессией.
    """

    def __init__(self, session: Session) -> None:
        """
        Инициализация ApiManager.
        :param session: HTTP-сессия, используемая всеми API-классами.
        """
        self.session = session

        self.auth_api = AuthAPI(session)
        self.user_api = UserAPI(session)
        self.movies_api = MoviesAPI(session)

    def close_session(self) -> None:
        self.session.close()
