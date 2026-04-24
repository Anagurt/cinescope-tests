from http import HTTPStatus

from requests import Session, Response

from constants import BASE_AUTH_URL, USER_ENDPOINT
from custom_requester.custom_requester import CustomRequester
from pydantic import BaseModel

class UserAPI(CustomRequester):
    """
    Класс для работы с API пользователей
    """

    def __init__(self, session: Session) -> None:
        super().__init__(session=session, base_url=BASE_AUTH_URL)

    def get_users(
                self,
                user_locator,
                expected_status: HTTPStatus = HTTPStatus.OK,
                success_response_model: type[BaseModel] | None = None,
                error_response_model: type[BaseModel] | None = None,
                attach_error_messages: bool = False,
                allure_attachment_name: str = "Сообщения об ошибках API",
            ) -> Response:
        """
        Получение списка пользователей
        :param user_locator: ID или Email пользователя.
        :param expected_status: Ожидаемый статус-код.
        :param success_response_model: Pydantic-модель для валидации успешного ответа.
        :param error_response_model: Pydantic-модель для валидации ошибочного ответа.
        :param attach_error_messages: Прикрепить поле message в Allure.
        :param allure_attachment_name: Название вложения в Allure.
        """
        return self.send_request(
                method="GET",
                endpoint=f"{USER_ENDPOINT}/{user_locator}",
                expected_status=expected_status,
                success_response_model=success_response_model,
                error_response_model=error_response_model,
                attach_error_messages=attach_error_messages,
                allure_attachment_name=allure_attachment_name,
            )

    def get_user_info(
                self,
                user_id: str | None = None,
                user_email: str | None = None,
                expected_status: HTTPStatus = HTTPStatus.OK,
                success_response_model: type[BaseModel] | None = None,
                error_response_model: type[BaseModel] | None = None,
                attach_error_messages: bool = False,
                allure_attachment_name: str = "Сообщения об ошибках API",
            ) -> Response:
        """
        Получение информации о пользователе
        :param user_id: ID пользователя.
        :param user_email: Email пользователя.
        :param expected_status: Ожидаемый статус-код.
        :param success_response_model: Pydantic-модель для валидации успешного ответа.
        :param error_response_model: Pydantic-модель для валидации ошибочного ответа.
        :param attach_error_messages: Прикрепить поле message в Allure.
        :param allure_attachment_name: Название вложения в Allure.
        """
        return self.send_request(
            method="GET",
            endpoint=f"{USER_ENDPOINT}/{user_id if user_id else user_email}",
            expected_status=expected_status,
            success_response_model=success_response_model,
            error_response_model=error_response_model,
            attach_error_messages=attach_error_messages,
            allure_attachment_name=allure_attachment_name,
        )

    def delete_user(
            self,
            user_id: str,
            expected_status: HTTPStatus = HTTPStatus.OK,
            success_response_model: type[BaseModel] | None = None,
            error_response_model: type[BaseModel] | None = None,
            attach_error_messages: bool = False,
            allure_attachment_name: str = "Сообщения об ошибках API",
        ) -> Response:
        """
        Удаление пользователя
        :param user_id: ID пользователя.
        :param expected_status: Ожидаемый статус-код.
        :param success_response_model: Pydantic-модель для валидации успешного ответа.
        :param error_response_model: Pydantic-модель для валидации ошибочного ответа.
        :param attach_error_messages: Прикрепить поле message в Allure.
        :param allure_attachment_name: Название вложения в Allure.
        """
        return self.send_request(
            method="DELETE",
            endpoint=f"{USER_ENDPOINT}/{user_id}",
            expected_status=expected_status,
            success_response_model=success_response_model,
            error_response_model=error_response_model,
            attach_error_messages=attach_error_messages,
            allure_attachment_name=allure_attachment_name,
        )

    def create_user(
            self,
            user_data: dict,
            expected_status: HTTPStatus = HTTPStatus.CREATED,
            success_response_model: type[BaseModel] | None = None,
            error_response_model: type[BaseModel] | None = None,
            attach_error_messages: bool = False,
            allure_attachment_name: str = "Сообщения об ошибках API",
        ) -> Response:
        """
        Создание пользователя
        :param user_data: Данные пользователя.
        :param expected_status: Ожидаемый статус-код.
        :param success_response_model: Pydantic-модель для валидации успешного ответа.
        :param error_response_model: Pydantic-модель для валидации ошибочного ответа.
        :param attach_error_messages: Прикрепить поле message в Allure.
        :param allure_attachment_name: Название вложения в Allure.
        """
        return self.send_request(
            method="POST",
            endpoint=USER_ENDPOINT,
            data=user_data,
            expected_status=expected_status,
            success_response_model=success_response_model,
            error_response_model=error_response_model,
            attach_error_messages=attach_error_messages,
            allure_attachment_name=allure_attachment_name,
        )
