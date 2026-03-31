from http import HTTPStatus

from requests import Session

from constants import BASE_MOVIES_URL, MOVIES_ENDPOINT
from custom_requester.custom_requester import CustomRequester


class MoviesAPI(CustomRequester):
    """
    Класс для работы с API фильмов.
    """

    def __init__(self, session: Session):
        super().__init__(session=session, base_url=BASE_MOVIES_URL)

    def get_movies(self, params: dict = None, expected_status: HTTPStatus = HTTPStatus.OK):
        """
        Получение списка афиш фильмов.
        :param params: Параметры запроса.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="GET",
            endpoint=MOVIES_ENDPOINT,
            params=params,
            expected_status=expected_status,
        )

    def post_movie(self, movie_data: dict, expected_status: HTTPStatus = HTTPStatus.CREATED):
        """
        Создание афиши фильма.
        :param movie_data: Данные афиши фильма.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="POST",
            endpoint=MOVIES_ENDPOINT,
            data=movie_data,
            expected_status=expected_status,
        )

    def get_movie(self, movie_id: int, expected_status: HTTPStatus = HTTPStatus.OK):
        """
        Получение информации о фильме.
        :param movie_id: ID афиши фильма.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="GET",
            endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
            expected_status=expected_status,
        )

    def patch_movie(self, movie_id: int, change_movie_data: dict, expected_status: HTTPStatus = HTTPStatus.OK):
        """
        Редактирование афиши фильма.
        :param movie_id: ID афиши фильма.
        :param change_movie_data: Данные для редактирования афиши фильма.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="PATCH",
            endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
            data=change_movie_data,
            expected_status=expected_status,
        )

    def delete_movie(self, movie_id: int, expected_status: HTTPStatus = HTTPStatus.OK):
        """
        Удаление афиши фильма.
        :param movie_id: ID афиши фильма.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="DELETE",
            endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
            expected_status=expected_status,
        )
