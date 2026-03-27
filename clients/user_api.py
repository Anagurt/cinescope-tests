import requests
from custom_requester.custom_requester import CustomRequester
from constants import BASE_AUTH_URL
from http import HTTPStatus


class UserAPI(CustomRequester):
    """
    Класс для работы с API пользователей.
    """

    def __init__(self, session: requests.Session):
        super().__init__(session=session, base_url=BASE_AUTH_URL)

    def get_user_info(self, user_id: int, expected_status: HTTPStatus = HTTPStatus.OK):
        """
        Получение информации о пользователе.
        :param user_id: ID пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="GET",
            endpoint=f"/user/{user_id}",
            expected_status=expected_status
        )

    def delete_user(self, user_id: int, expected_status: HTTPStatus = HTTPStatus.OK):
        """
        Удаление пользователя.
        :param user_id: ID пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="DELETE",
            endpoint=f"/user/{user_id}",
            expected_status=expected_status
        )
