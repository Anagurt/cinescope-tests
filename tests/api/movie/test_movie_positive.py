from http import HTTPStatus

import allure
import pytest

from clients.api_manager import ApiManager
from models.base_model_movies import GetMoviesListResponse, GetMovieByIdResponse
from models.base_model_movies import MovieInfoResponse, MovieInfoRequest
from utils.data_generator import DataGenerator
from entities.location import Location
from db_requester.db_helpers import DBHelper
from tests.constants.movie_cases import (
    GET_MOVIES_PARAMS_CASES,
    GET_MOVIES_PARAMS_IDS,
)
from tests.constants.auth_cases import (
    LOGIN_EXIST_USERS_CASES,
    LOGIN_EXIST_USERS_IDS
)
from constants import MovieConstants


def _assert_create_movie_echoes_request(movie_data: dict,
                                        response_data: dict) -> None:
    """
    Сравнивает поля запроса с телом ответа.
    При расхождении сообщение указывает конкретный ключ.
    """
    mismatches = []
    for key in movie_data:
        if key not in response_data:
            mismatches.append(f"{key}: нет в ответе")
            continue
        expected = movie_data[key]
        actual = response_data[key]
        if actual != expected:
            mismatches.append(
                f"{key}: ожидалось {expected!r}, в ответе {actual!r}")
    assert not mismatches, "Поля create_movie не совпадают с запросом:\n" + "\n".join(
        mismatches)


@allure.feature("Позитивные тесты для movies API")
class TestMoviesAPIPositive:

    @pytest.mark.smoke
    @allure.story(
        "Тест на получение списка афиш фильмов (под неавторизованным пользователем)"
    )
    @pytest.mark.parametrize(
        "params",
        GET_MOVIES_PARAMS_CASES,
        ids=GET_MOVIES_PARAMS_IDS,
    )
    def test_get_movies_unauthorized_user(self, anonymous_api_manager, params):
        response = anonymous_api_manager.movies_api.get_movies(params=params)
        data = response.json()
        movies_list_response = GetMoviesListResponse.model_validate(data)
        if params is MovieConstants.RANGE_PRICE_PARAMS:
            min_price = MovieConstants.RANGE_PRICE_PARAMS["minPrice"]
            max_price = MovieConstants.RANGE_PRICE_PARAMS["maxPrice"]
            assert all(min_price <= movie.price <= max_price
                       for movie in movies_list_response.movies)
        if params is MovieConstants.LOCATION_PARAMS:
            expected_location = MovieConstants.LOCATION_PARAMS["locations"]
            assert all(movie.location == expected_location
                       for movie in movies_list_response.movies)
        if params is MovieConstants.GENRE_ID_PARAMS:
            expected_genre_id = MovieConstants.GENRE_ID_PARAMS["genreId"]
            assert all(movie.genreId == expected_genre_id
                       for movie in movies_list_response.movies)

    @pytest.mark.smoke
    @allure.story("Тест на создание афиши фильма (под админскими правами)")
    def test_create_movie_by_super_admin(self, movie_data: MovieInfoRequest,
                                         super_admin, movies_to_cleanup: list,
                                         db_helper: DBHelper):
        assert not db_helper.movie_exists_by_name(movie_data.name)
        response = super_admin.api.movies_api.post_movie(
            movie_data, expected_status=HTTPStatus.CREATED)
        created = MovieInfoResponse.model_validate(response.json())

        _assert_create_movie_echoes_request(
            movie_data.model_dump(mode="json"),
            created.model_dump(mode="json"),
        )
        assert db_helper.movie_exists_by_name(movie_data.name)

        movies_to_cleanup.append(created.id)

    @pytest.mark.smoke
    @allure.story("Тест на получение информации о созданной афише фильма")
    @pytest.mark.parametrize(
        "email, password",
        LOGIN_EXIST_USERS_CASES,
        ids=LOGIN_EXIST_USERS_IDS,
    )
    def test_get_movie_by_id(self,
                             created_movie_and_cleanup: MovieInfoResponse,
                             email, password,
                             db_helper: DBHelper, api_manager: ApiManager,
                             expected_status: HTTPStatus = HTTPStatus.OK):
        assert db_helper.movie_exists_by_name(created_movie_and_cleanup.name)
        api_manager.auth_api.authenticate((email, password))
        response = api_manager.movies_api.get_movie(
            created_movie_and_cleanup.id, expected_status=expected_status)
        created = GetMovieByIdResponse.model_validate(response.json())
        assert created.id == created_movie_and_cleanup.id

    @pytest.mark.smoke
    @allure.story("Тест на изменение афиши фильма (под админскими правами)")
    def test_change_movie_by_super_admin(
            self, created_movie_and_cleanup: MovieInfoResponse, super_admin,
            db_helper: DBHelper):
        assert db_helper.movie_exists_by_name(created_movie_and_cleanup.name)
        change_movie_data = MovieInfoRequest(
            name=DataGenerator.generate_random_name_movie(),
            imageUrl="https://example.com/image.png",
            price=DataGenerator.generate_random_price_movie(),
            description=DataGenerator.generate_random_description_movie(),
            location=Location.SPB,
            published=True,
            genreId=2,
        )
        response = super_admin.api.movies_api.patch_movie(
            created_movie_and_cleanup.id,
            change_movie_data.model_dump(mode="json"),
            expected_status=HTTPStatus.OK)
        changed = MovieInfoResponse.model_validate(response.json())
        assert changed.id == created_movie_and_cleanup.id
        assert changed.name == change_movie_data.name
        assert changed.name != created_movie_and_cleanup.name
        assert db_helper.movie_exists_by_name(change_movie_data.name)

    @pytest.mark.smoke
    @allure.story("Тест на удаление афиши фильма (под админскими правами)")
    def test_delete_movie_by_super_admin(
            self, created_movie_and_cleanup: MovieInfoResponse, super_admin,
            db_helper: DBHelper):
        assert db_helper.movie_exists_by_name(created_movie_and_cleanup.name)
        response = super_admin.api.movies_api.delete_movie(
            created_movie_and_cleanup.id, expected_status=HTTPStatus.OK)
        deleted = MovieInfoResponse.model_validate(response.json())
        assert deleted.id == created_movie_and_cleanup.id
        super_admin.api.movies_api.get_movie(
            created_movie_and_cleanup.id, expected_status=HTTPStatus.NOT_FOUND)
        assert not db_helper.movie_exists_by_name(
            created_movie_and_cleanup.name)
