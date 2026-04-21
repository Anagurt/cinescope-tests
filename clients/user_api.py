from http import HTTPStatus

from requests import Session, Response

from constants import BASE_AUTH_URL, USER_ENDPOINT
from custom_requester.custom_requester import CustomRequester


class UserAPI(CustomRequester):
    """
    Класс для работы с API пользователей
    """

    def __init__(self, session: Session) -> None:
        super().__init__(session=session, base_url=BASE_AUTH_URL)

    def get_users(self,
                  user_locator,
                  expected_status: HTTPStatus = HTTPStatus.OK) -> Response:
        """
        Получение списка пользователей
        :param user_locator: ID или Email пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(method="GET",
                                 endpoint=f"{USER_ENDPOINT}/{user_locator}",
                                 expected_status=expected_status)

    def get_user_info(self,
                      user_id: str | None = None,
                      user_email: str | None = None,
                      expected_status: HTTPStatus = HTTPStatus.OK) -> Response:
        """
        Получение информации о пользователе
        :param user_id: ID пользователя.
        :param user_email: Email пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="GET",
            endpoint=f"{USER_ENDPOINT}/{user_id if user_id else user_email}",
            expected_status=expected_status,
        )

    def delete_user(self,
                    user_id: str,
                    expected_status: HTTPStatus = HTTPStatus.OK) -> Response:
        """
        Удаление пользователя
        :param user_id: ID пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="DELETE",
            endpoint=f"{USER_ENDPOINT}/{user_id}",
            expected_status=expected_status,
        )

    def create_user(
            self,
            user_data: dict,
            expected_status: HTTPStatus = HTTPStatus.CREATED) -> Response:
        """
        Создание пользователя
        :param user_data: Данные пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(method="POST",
                                 endpoint=USER_ENDPOINT,
                                 data=user_data,
                                 expected_status=expected_status)
