from __future__ import annotations

from http import HTTPStatus

from requests import Session, Response
from pydantic import BaseModel

from constants import (
    BASE_AUTH_URL,
    LOGIN_ENDPOINT,
    REGISTER_ENDPOINT,
)
from custom_requester.custom_requester import CustomRequester
from resources.user_creds import RegularUserCreds, SuperAdminCreds
from models.base_models_auth import (
    LoginResponse,
    LoginUserUnauthorizedResponse,
    RegisterUserBadRequestResponse,
    RegisterUserConflictResponse,
    RegisterUserResponse,
)

class AuthAPI(CustomRequester):
    """
    Класс для работы с аутентификацией.
    """

    def __init__(self, session: Session) -> None:
        super().__init__(session=session, base_url=BASE_AUTH_URL)

    @staticmethod
    def _resolve_error_model(
        expected_status: HTTPStatus,
        status_to_model: dict[HTTPStatus, type[BaseModel]],
    ) -> type[BaseModel] | None:
        return status_to_model.get(expected_status)


    def register_user(
            self,
            user_data: dict,
            expected_status: HTTPStatus = HTTPStatus.CREATED,
            attach_error_messages: bool = False,
            allure_attachment_name: str = "Сообщения об ошибках API",
    ) -> Response:
        """
        Регистрация нового пользователя.
        :param user_data: Данные пользователя.
            data=user_data,
            expected_status=expected_status,
            attach_error_messages=attach_error_messages,
            allure_attachment_name=allure_attachment_name,

        """
        return self.send_request(
            method="POST",
            endpoint=REGISTER_ENDPOINT,
            data=user_data,
            expected_status=expected_status,
            success_response_model=RegisterUserResponse,
            error_response_model=self._resolve_error_model(
                expected_status,
                {
                    HTTPStatus.BAD_REQUEST: RegisterUserBadRequestResponse,
                    HTTPStatus.CONFLICT: RegisterUserConflictResponse,
                },
            ),
            attach_error_messages=attach_error_messages,
            allure_attachment_name=allure_attachment_name,
        )

    def login_user(
            self, 
            login_data: dict,
            expected_status: HTTPStatus = HTTPStatus.OK,
            attach_error_messages: bool = False,
            allure_attachment_name: str = "Сообщения об ошибках API",
        ) -> Response:
        """
        Авторизация пользователя.
        :param login_data: Данные для логина.
        :param expected_status: Ожидаемый статус-код.
        :param attach_error_messages: Прикрепить поле message в Allure.
        :param allure_attachment_name: Название вложения в Allure.
        """
        return self.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=login_data,
            expected_status=expected_status,
            success_response_model=LoginResponse,
            error_response_model=self._resolve_error_model(
                expected_status,
                {
                    HTTPStatus.UNAUTHORIZED: LoginUserUnauthorizedResponse,
                },
            ),
            attach_error_messages=attach_error_messages,
            allure_attachment_name=allure_attachment_name,
        )

    def authenticate(
        self,
        user_creds: tuple[str, str] = (SuperAdminCreds.USERNAME,
                                       SuperAdminCreds.PASSWORD),
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
        response = self.login_user(
            login_data,
            expected_status=HTTPStatus.OK,
        ).json()

        if (token := response.get("accessToken")) is None:
            raise KeyError("token is missing")

        self._update_session_headers(authorization=f"Bearer {token}")
