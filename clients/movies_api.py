from http import HTTPStatus

from requests import Session, Response

from constants import BASE_MOVIES_URL, MOVIES_ENDPOINT
from custom_requester.custom_requester import CustomRequester
from pydantic import BaseModel
from models.base_model_movies import (
    GetMovieBadRequest,
    GetMovieConflictResponse,
    GetMovieForbiddenResponse,
    GetMovieNotFoundResponse,
    GetMovieByIdResponse,
    GetMoviesListResponse,
    MovieInfoResponse,
)

class MoviesAPI(CustomRequester):
    """
    Класс для работы с API фильмов.
    """
    ERROR_MODELS: dict[HTTPStatus, type[BaseModel]] = {
        HTTPStatus.BAD_REQUEST: GetMovieBadRequest,
        HTTPStatus.FORBIDDEN: GetMovieForbiddenResponse,
        HTTPStatus.NOT_FOUND: GetMovieNotFoundResponse,
        HTTPStatus.CONFLICT: GetMovieConflictResponse,
    }

    def __init__(self, session: Session) -> None:
        self.session = session
        super().__init__(session=session, base_url=BASE_MOVIES_URL)

    @staticmethod
    def _resolve_error_model(expected_status: HTTPStatus) -> type[BaseModel] | None:
        return MoviesAPI.ERROR_MODELS.get(expected_status)

    def get_movies(
            self,
            params: dict = None,
            expected_status: HTTPStatus = HTTPStatus.OK,
            attach_error_messages: bool = False,
            allure_attachment_name: str = "Сообщения об ошибках API",
        ) -> Response:
        """
        Получение списка афиш фильмов.
        :param params: Параметры запроса.
        :param expected_status: Ожидаемый статус-код.
        :param attach_error_messages: Прикрепить поле message в Allure.
        :param allure_attachment_name: Название вложения в Allure.
        """
        return self.send_request(
            method="GET",
            endpoint=MOVIES_ENDPOINT,
            params=params,
            expected_status=expected_status,
            success_response_model=GetMoviesListResponse,
            error_response_model=self._resolve_error_model(expected_status),
            attach_error_messages=attach_error_messages,
            allure_attachment_name=allure_attachment_name,
        )

    def post_movie(
            self,
            movie_data: dict,
            expected_status: HTTPStatus = HTTPStatus.CREATED,
            attach_error_messages: bool = False,
            allure_attachment_name: str = "Сообщения об ошибках API",
        ) -> Response:
        """
        Создание афиши фильма.
        :param movie_data: Данные афиши фильма.
        :param expected_status: Ожидаемый статус-код.
        :param attach_error_messages: Прикрепить поле message в Allure.
        :param allure_attachment_name: Название вложения в Allure.
        """
        return self.send_request(
            method="POST",
            endpoint=MOVIES_ENDPOINT,
            data=movie_data,
            expected_status=expected_status,
            success_response_model=MovieInfoResponse,
            error_response_model=self._resolve_error_model(expected_status),
            attach_error_messages=attach_error_messages,
            allure_attachment_name=allure_attachment_name,
        )

    def get_movie(
            self,
            movie_id: int,
            expected_status: HTTPStatus = HTTPStatus.OK,
            attach_error_messages: bool = False,
            allure_attachment_name: str = "Сообщения об ошибках API",
        ) -> Response:
        """
        Получение информации о фильме.
        :param movie_id: ID афиши фильма.
        :param expected_status: Ожидаемый статус-код.
        :param attach_error_messages: Прикрепить поле message в Allure.
        :param allure_attachment_name: Название вложения в Allure.
        """
        return self.send_request(
            method="GET",
            endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
            expected_status=expected_status,
            success_response_model=GetMovieByIdResponse,
            error_response_model=self._resolve_error_model(expected_status),
            attach_error_messages=attach_error_messages,
            allure_attachment_name=allure_attachment_name,
        )

    def patch_movie(
            self,
            movie_id: int,
            change_movie_data: dict,
            expected_status: HTTPStatus = HTTPStatus.OK,
            attach_error_messages: bool = False,
            allure_attachment_name: str = "Сообщения об ошибках API",
        ) -> Response:
        """
        Редактирование афиши фильма.
        :param movie_id: ID афиши фильма.
        :param change_movie_data: Данные для редактирования афиши фильма.
        :param expected_status: Ожидаемый статус-код.
        :param attach_error_messages: Прикрепить поле message в Allure.
        :param allure_attachment_name: Название вложения в Allure.
        """
        return self.send_request(
            method="PATCH",
            endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
            data=change_movie_data,
            expected_status=expected_status,
            success_response_model=MovieInfoResponse,
            error_response_model=self._resolve_error_model(expected_status),
            attach_error_messages=attach_error_messages,
            allure_attachment_name=allure_attachment_name,
        )

    def delete_movie(
            self,
            movie_id: int,
            expected_status: HTTPStatus = HTTPStatus.OK,
            attach_error_messages: bool = False,
            allure_attachment_name: str = "Сообщения об ошибках API",
        ) -> Response:
        """
        Удаление афиши фильма.
        :param movie_id: ID афиши фильма.
        :param expected_status: Ожидаемый статус-код.
        :param attach_error_messages: Прикрепить поле message в Allure.
        :param allure_attachment_name: Название вложения в Allure.
        """
        return self.send_request(
            method="DELETE",
            endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
            expected_status=expected_status,
            success_response_model=MovieInfoResponse,
            error_response_model=self._resolve_error_model(expected_status),
            attach_error_messages=attach_error_messages,
            allure_attachment_name=allure_attachment_name,
        )
