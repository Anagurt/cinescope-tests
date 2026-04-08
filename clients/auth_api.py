from __future__ import annotations

from resources.user_creds import RegularUserCreds, SuperAdminCreds
from http import HTTPStatus

from requests import Session

from constants import (
    BASE_AUTH_URL,
    LOGIN_ENDPOINT,
    REGISTER_ENDPOINT,
)
from custom_requester.custom_requester import CustomRequester


class AuthAPI(CustomRequester):
    """
    Класс для работы с аутентификацией.
    """

    def __init__(self, session: Session):
        super().__init__(session=session, base_url=BASE_AUTH_URL)

    def register_user(self, user_data: dict, expected_status: HTTPStatus = HTTPStatus.CREATED):
        """
        Регистрация нового пользователя.
        :param user_data: Данные пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="POST",
            endpoint=REGISTER_ENDPOINT,
            data=user_data,
            expected_status=expected_status,
        )

    def login_user(self, login_data: dict, expected_status: HTTPStatus = HTTPStatus.OK):
        """
        Авторизация пользователя.
        :param login_data: Данные для логина.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=login_data,
            expected_status=expected_status,
        )

    def authenticate(
        self,
        user_creds: tuple[str, str] = (SuperAdminCreds.USERNAME, SuperAdminCreds.PASSWORD),
        use_regular_user: bool = False,
    ) -> None:
        """
        Логин и установка Bearer-токена в сессию.

        :param user_creds: По умолчанию — супер-админ из env
        :param use_regular_user: если True — логин под RegularUserCreds из env
        """
        if use_regular_user:
            email, password = RegularUserCreds.USERNAME, RegularUserCreds.PASSWORD
        else:
            email, password = user_creds
        login_data = {"email": email, "password": password}
        response = self.login_user(login_data).json()

        if (token := response.get("accessToken")) is None:
            raise KeyError("token is missing")

        self._update_session_headers(authorization=f"Bearer {token}")