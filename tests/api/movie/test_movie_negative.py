from http import HTTPStatus
from http.client import responses

import allure
import pytest

from models.base_model_movies import MovieInfoRequest
from clients.api_manager import ApiManager
from db_requester.db_helpers import DBHelper
from tests.constants.movie_cases import (
    INVALID_GET_MOVIES_PARAMS_CASES,
    INVALID_GET_MOVIES_PARAMS_IDS,
    INVALID_MOVIE_FIELDS_CASES,
    INVALID_MOVIE_FIELDS_IDS,
    MOVIE_METHODS_CASES,
    MOVIE_METHODS_IDS,
    ADMIN_AND_REGULAR_USER_CASES,
    ADMIN_AND_REGULAR_USER_IDS,
)
from constants import MovieMethods, MovieConstants


@allure.feature("Негативные тесты для movies API")
class TestMoviesAPINegative:

    @pytest.mark.smoke
    @pytest.mark.negative
    @allure.story(
        "Негативный тест на получение списка афиш фильмов "
        "с некорректными параметрами (под неавторизованным пользователем)"
    )
    @pytest.mark.parametrize(
        "params",
        INVALID_GET_MOVIES_PARAMS_CASES,
        ids=INVALID_GET_MOVIES_PARAMS_IDS,
    )
    def test_movies_with_invalid_params_unauthorized_user(
            self, anonymous_api_manager, params: dict):
        anonymous_api_manager.movies_api.get_movies(
            params=params, expected_status=HTTPStatus.BAD_REQUEST)

    @pytest.mark.smoke
    @pytest.mark.negative
    @allure.story(
        "Негативный тест на операции над несуществующим фильмом (под супер-админом)"
    )
    @pytest.mark.parametrize(
        "operation",
        MOVIE_METHODS_CASES,
        ids=MOVIE_METHODS_IDS,
    )
    def test_operation_with_nonexistent_movie_super_admin(
            self, super_admin, operation: str):
        movie_id = 999999999
        method = getattr(super_admin.api.movies_api, operation)
        method(movie_id, expected_status=HTTPStatus.NOT_FOUND)

    @pytest.mark.smoke
    @pytest.mark.negative
    @allure.story(
        "Негативный тест на изменение несуществующего фильма (под супер-админом)"
    )
    def test_patch_nonexistent_movie_super_admin(
            self, super_admin):
        movie_id = 999999999
        super_admin.api.movies_api.patch_movie(
            movie_id,
            MovieConstants.PATCH_MOVIE_DATA_NEGATIVE_CASES,
            expected_status=HTTPStatus.NOT_FOUND
        )

    @pytest.mark.smoke
    @pytest.mark.negative
    @allure.story(
        "Негативный тест на создание афиши фильма с некорректными данными")
    @pytest.mark.parametrize(
        "movie_data",
        INVALID_MOVIE_FIELDS_CASES,
        ids=INVALID_MOVIE_FIELDS_IDS,
    )
    def test_create_movie_with_invalid_fields(
            self,
            super_admin,
            movie_data,
            db_helper: DBHelper):
        super_admin.api.movies_api.post_movie(
            movie_data, expected_status=HTTPStatus.BAD_REQUEST)

        if db_helper.movie_exists_by_name(movie_data["name"]):
            raise AssertionError(
                f"Фильм {movie_data['name']} создан в БД, "
                "ожидалось, что фильм не будет создан"
            )

    @pytest.mark.smoke
    @pytest.mark.negative
    @allure.story(
        "Негативный тест на создание афиши фильма "
        "(под админом и авторизованным пользователем)"
    )
    @pytest.mark.parametrize(
        "email, password",
        ADMIN_AND_REGULAR_USER_CASES,
        ids=ADMIN_AND_REGULAR_USER_IDS,
    )
    def test_create_movie_by_invalid_role_user(
            self,
            api_manager: ApiManager,
            email: str,
            password: str,
            movie_data,
            db_helper: DBHelper):

        api_manager.auth_api.authenticate((email, password))
        api_manager.movies_api.post_movie(
            movie_data, expected_status=HTTPStatus.FORBIDDEN)

        if db_helper.movie_exists_by_name(movie_data.name):
            raise AssertionError(
                f"Фильм {movie_data.name} создан в БД, "
                "ожидалось, что фильм не будет создан"
            )

    @pytest.mark.smoke
    @pytest.mark.negative
    @allure.story(
        "Негативный тест на удаление афиши фильма "
        "(под админом и авторизованным пользователем)"
    )
    @pytest.mark.parametrize(
        "email, password",
        ADMIN_AND_REGULAR_USER_CASES,
        ids=ADMIN_AND_REGULAR_USER_IDS,
    )
    def test_delete_movie_by_invalid_role_user(
            self,
            api_manager: ApiManager,
            email: str,
            password: str,
            created_movie_and_cleanup,
            db_helper: DBHelper,
    ):
        if not db_helper.get_movie_by_id(created_movie_and_cleanup.id):
            raise AssertionError(
                f"Фильм {created_movie_and_cleanup.id} отсутствует в БД"
            )

        api_manager.auth_api.authenticate((email, password))
        api_manager.movies_api.delete_movie(
            created_movie_and_cleanup.id, expected_status=HTTPStatus.FORBIDDEN)

        if not db_helper.get_movie_by_id(created_movie_and_cleanup.id):
            raise AssertionError(
                f"Фильм {created_movie_and_cleanup.id} отсутствует в БД"
            )

    @pytest.mark.smoke
    @pytest.mark.negative
    @allure.story(
        "Негативный тест на изменение афиши фильма "
        "(под админом и авторизованным пользователем)"
    )
    @pytest.mark.parametrize(
        "email, password",
        ADMIN_AND_REGULAR_USER_CASES,
        ids=ADMIN_AND_REGULAR_USER_IDS,
    )
    def test_patch_movie_by_invalid_role_user(
            self,
            api_manager: ApiManager,
            email: str,
            password: str,
            created_movie_and_cleanup,
            db_helper: DBHelper,
    ):
        if not db_helper.get_movie_by_id(created_movie_and_cleanup.id):
            raise AssertionError(
                f"Фильм {created_movie_and_cleanup.id} отсутствует в БД"
            )

        api_manager.auth_api.authenticate((email, password))
        change_movie_data = MovieInfoRequest(
            **MovieConstants.PATCH_MOVIE_DATA_NEGATIVE_CASES
        )
        api_manager.movies_api.patch_movie(
            created_movie_and_cleanup.id,
            change_movie_data.model_dump(mode="json"),
            expected_status=HTTPStatus.FORBIDDEN)

        if not db_helper.movie_exists_by_name(created_movie_and_cleanup.name):
            raise AssertionError(
                f"Фильм с названием {created_movie_and_cleanup.name} отсутствует в БД"
            )

    @pytest.mark.smoke
    @pytest.mark.negative
    @allure.story(
        "Негативный тест на создание афиши фильма "
        "с теми же данными, что и уже существующего"
    )
    def test_create_same_movie_duplicated(
            self,
            super_admin,
            created_movie_and_cleanup,
            db_helper: DBHelper,
        ):
        movie_data = MovieInfoRequest(
            name=created_movie_and_cleanup.name,
            imageUrl=created_movie_and_cleanup.imageUrl,
            price=created_movie_and_cleanup.price,
            description=created_movie_and_cleanup.description,
            location=created_movie_and_cleanup.location,
            published=created_movie_and_cleanup.published,
            genreId=created_movie_and_cleanup.genreId,
        )
        super_admin.api.movies_api.post_movie(
            movie_data, expected_status=HTTPStatus.CONFLICT)

        if db_helper.movie_count_by_name(created_movie_and_cleanup.name) != 1:
            raise AssertionError(
                f"Фильмов с названием {created_movie_and_cleanup.name} "
                "в БД больше одного"
            )

    @allure.story(
        "Негативный тест на изменение афиши фильма с пустыми данными")
    @pytest.mark.parametrize(
        "change_movie_data",
        INVALID_MOVIE_FIELDS_CASES,
        ids=INVALID_MOVIE_FIELDS_IDS,
    )
    def test_change_movie_with_invalid_fields(
            self,
            super_admin,
            change_movie_data,
            created_movie_and_cleanup,
            db_helper: DBHelper,
    ):
        super_admin.api.movies_api.patch_movie(
            created_movie_and_cleanup.id,
            change_movie_data,
            expected_status=HTTPStatus.BAD_REQUEST)

        if db_helper.movie_exists_by_name(change_movie_data["name"]):
            raise AssertionError(
                f"Название фильма изменилось на {change_movie_data['name']} в БД, "
                "ожидалось, что название фильма не будет изменено"
            )
