from http import HTTPStatus

import allure
import pytest

from models.base_model_movies import GetMovieBadRequest, GetMovieNotFoundResponse, GetMovieForbiddenResponse, MovieInfoRequest, GetMovieConflictResponse
from clients.api_manager import ApiManager
from resources.user_creds import RegularUserCreds, AdminCreds
from utils.data_generator import DataGenerator
from entities.location import Location
from db_requester.db_helpers import DBHelper

@allure.feature("Негативные тесты для movies API")
class TestMoviesAPINegative:

    @pytest.mark.smoke
    @pytest.mark.negative
    @allure.story("Негативный тест на получение списка афиш фильмов с некорректными параметрами (под неавторизованным пользователем)")
    @pytest.mark.parametrize(
        "params, expected_status", [
            ({"page": -1}, HTTPStatus.BAD_REQUEST),
            ({"minPrice": 10, "maxPrice": 10}, HTTPStatus.BAD_REQUEST),
            ({"createdAt": "wrong"}, HTTPStatus.BAD_REQUEST),
            ({"genreId": 0}, HTTPStatus.BAD_REQUEST),
        ],
        ids=["Отрицательная страница", "Минимальное и максимальное значение в диапазоне цен равны", "Некорректный параметр createdAt", "Значение genreId равно 0"])
    def test_movies_with_invalid_params_unauthorized_user(self, anonymous_api_manager, params, expected_status):
        response = anonymous_api_manager.movies_api.get_movies(params=params, expected_status=expected_status)
        GetMovieBadRequest.model_validate(response.json())


    @pytest.mark.smoke
    @pytest.mark.negative
    @allure.story("Негативный тест на операции над несуществующим фильмом (под супер-админом)")
    @pytest.mark.parametrize(
        "operation, expected_status",
        [("get", HTTPStatus.NOT_FOUND), ("delete", HTTPStatus.NOT_FOUND), ("patch", HTTPStatus.NOT_FOUND)],
        ids=["GET несуществующего фильма", "DELETE несуществующего фильма", "PATCH несуществующего фильма"],
    )
    def test_operation_with_nonexistent_movie_super_admin(self, super_admin, operation, expected_status, db_helper: DBHelper):
        movie_id = 999999999
        assert not db_helper.get_movie_by_id(movie_id)

        if operation == "get":
            response = super_admin.api.movies_api.get_movie(movie_id, expected_status=expected_status)
        if operation == "delete":
            response = super_admin.api.movies_api.delete_movie(movie_id, expected_status=expected_status)
        if operation == "patch":
            response = super_admin.api.movies_api.patch_movie(
                movie_id,
                {"name": "Название фильма", "description": "Описание фильма", "price": 1, "location": "SPB",
                "imageUrl": "https://example.com/x.png", "published": True, "genreId": 1},
                expected_status=expected_status,
            )
        GetMovieNotFoundResponse.model_validate(response.json())


    @pytest.mark.smoke
    @pytest.mark.negative
    @allure.story("Негативный тест на создание афиши фильма с некорректными данными")
    @pytest.mark.parametrize(
        "movie_data, expected_status", [
            ({"name": "", "imageUrl": "https://example.com/image.png", "price": 10, "description": "Описание фильма", "location": "SPB", "published": True, "genreId": 1}, HTTPStatus.BAD_REQUEST),
            pytest.param({"name": "Невалидный фильм", "imageUrl": "https://example.com/image.png", "price": -1, "description": "Описание фильма", "location": "SPB", "published": True, "genreId": 1}, HTTPStatus.BAD_REQUEST, marks=pytest.mark.skip(reason="Баг в ответе API, ожидаемый ответ BAD_REQUEST, приходит OK")),
            ({"name": "Невалидный фильм", "imageUrl": "https://example.com/image.png", "price": 10, "description": "Описание фильма", "location": "SPB", "published": True, "genreId": 0}, HTTPStatus.BAD_REQUEST),
        ],
        ids=["Пустое поле name", "Отрицательное значение price", "Значение genreId равно 0"])
    def test_create_movie_with_invalid_fields(self, super_admin, movie_data, expected_status):
        response = super_admin.api.movies_api.post_movie(movie_data, expected_status=expected_status)
        GetMovieBadRequest.model_validate(response.json())


    @pytest.mark.smoke
    @pytest.mark.negative
    @allure.story("Негативный тест на создание афиши фильма (под админом и авторизованным пользователем)")
    @pytest.mark.parametrize(
        "email, password, expected_status",[
        (f"{AdminCreds.USERNAME}", f"{AdminCreds.PASSWORD}", HTTPStatus.FORBIDDEN),
        (f"{RegularUserCreds.USERNAME}", f"{RegularUserCreds.PASSWORD}", HTTPStatus.FORBIDDEN)
        ], ids=["Создание фильма под админом", "Создание фильма под пользователем"])
    def test_create_movie_by_invalid_role_user(self, api_manager: ApiManager, email, password, movie_data, expected_status, db_helper: DBHelper):
        api_manager.auth_api.authenticate((email, password))
        response = api_manager.movies_api.post_movie(movie_data, expected_status=expected_status)
        GetMovieForbiddenResponse.model_validate(response.json())
        assert not db_helper.movie_exists_by_name(movie_data.name)

    @pytest.mark.smoke
    @pytest.mark.negative
    @allure.story("Негативный тест на удаление афиши фильма (под админом и авторизованным пользователем)")
    @pytest.mark.parametrize(
        "email, password, expected_status",[
        (f"{AdminCreds.USERNAME}", f"{AdminCreds.PASSWORD}", HTTPStatus.FORBIDDEN),
        (f"{RegularUserCreds.USERNAME}", f"{RegularUserCreds.PASSWORD}", HTTPStatus.FORBIDDEN)
        ], ids=["Удаление фильма под админом", "Удаление фильма под пользователем"])
    def test_delete_movie_by_invalid_role_user(self, api_manager: ApiManager, email, password, created_movie_and_cleanup, expected_status, db_helper: DBHelper):
        assert db_helper.get_movie_by_id(created_movie_and_cleanup.id)
        api_manager.auth_api.authenticate((email, password))
        response = api_manager.movies_api.delete_movie(created_movie_and_cleanup.id, expected_status=expected_status)
        GetMovieForbiddenResponse.model_validate(response.json())
        assert db_helper.get_movie_by_id(created_movie_and_cleanup.id)


    @pytest.mark.smoke
    @pytest.mark.negative
    @allure.story("Негативный тест на изменение афиши фильма (под админом и авторизованным пользователем)")
    @pytest.mark.parametrize(
        "email, password, expected_status",[
        (f"{AdminCreds.USERNAME}", f"{AdminCreds.PASSWORD}", HTTPStatus.FORBIDDEN),
        (f"{RegularUserCreds.USERNAME}", f"{RegularUserCreds.PASSWORD}", HTTPStatus.FORBIDDEN)
        ], ids=["Изменение фильма под админом", "Изменение фильма под пользователем"])
    def test_patch_movie_by_invalid_role_user(self, api_manager: ApiManager, email, password, created_movie_and_cleanup, expected_status, db_helper: DBHelper):
        assert db_helper.get_movie_by_id(created_movie_and_cleanup.id)
        api_manager.auth_api.authenticate((email, password))
        change_movie_data = MovieInfoRequest(
            name=DataGenerator.generate_random_name_movie(),
            imageUrl="https://example.com/image.png",
            price=DataGenerator.generate_random_price_movie(),
            description=DataGenerator.generate_random_description_movie(),
            location=Location.SPB,
            published=True,
            genreId=2,
        )
        response = api_manager.movies_api.patch_movie(created_movie_and_cleanup.id, change_movie_data.model_dump(mode="json"), expected_status=expected_status)
        GetMovieForbiddenResponse.model_validate(response.json())
        assert db_helper.movie_exists_by_name(created_movie_and_cleanup.name)


    @pytest.mark.smoke
    @pytest.mark.negative
    @allure.story("Негативный тест на создание афиши фильма с теми же данными, что и уже существующего")
    def test_create_same_movie_duplicated(self, super_admin, created_movie_and_cleanup, db_helper: DBHelper):
        assert db_helper.movie_exists_by_name(created_movie_and_cleanup.name)
        movie_data = MovieInfoRequest(
            name=created_movie_and_cleanup.name,
            imageUrl=created_movie_and_cleanup.imageUrl,
            price=created_movie_and_cleanup.price,
            description=created_movie_and_cleanup.description,
            location=created_movie_and_cleanup.location,
            published=created_movie_and_cleanup.published,
            genreId=created_movie_and_cleanup.genreId,
        )
        response = super_admin.api.movies_api.post_movie(movie_data, expected_status=HTTPStatus.CONFLICT)
        GetMovieConflictResponse.model_validate(response.json())
        assert db_helper.movie_count_by_name(created_movie_and_cleanup.name) == 1


    @allure.story("Негативный тест на изменение афиши фильма с пустыми данными")
    @pytest.mark.parametrize(
        "change_movie_data, expected_status", [
            pytest.param({"name": "", "imageUrl": "https://example.com/image.png", "price": 10, "description": "Описание фильма", "location": "SPB", "published": True, "genreId": 1}, HTTPStatus.BAD_REQUEST, marks=pytest.mark.skip(reason="Баг в ответе API, ожидаемый ответ BAD_REQUEST, приходит NOT_FOUND")),
            pytest.param({"name": "Невалидный фильм", "imageUrl": "https://example.com/image.png", "price": -1, "description": "Описание фильма", "location": "SPB", "published": True, "genreId": 1}, HTTPStatus.BAD_REQUEST, marks=pytest.mark.skip(reason="Баг в ответе API, ожидаемый ответ BAD_REQUEST, приходит OK")),
            ({"name": "Невалидный фильм", "imageUrl": "https://example.com/image.png", "price": 10, "description": "Описание фильма", "location": "SPB", "published": True, "genreId": 0}, HTTPStatus.BAD_REQUEST),
        ],
        ids=["Пустое поле name", "Отрицательное значение price", "Значение genreId равно 0"])
    def test_change_movie_with_invalid_fields(self, super_admin, change_movie_data, created_movie_and_cleanup, expected_status):
        response = super_admin.api.movies_api.patch_movie(created_movie_and_cleanup.id, change_movie_data, expected_status=expected_status)
        GetMovieBadRequest.model_validate(response.json())
