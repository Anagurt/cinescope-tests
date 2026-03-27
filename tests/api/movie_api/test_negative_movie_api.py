import pytest
from clients.api_manager import ApiManager

from http import HTTPStatus


class TestMoviesAPINegative:
    def test_movies_with_invalid_page(self, api_manager: ApiManager):
        """
        Негативный тест на получение списка афиш фильмов с некорректным параметром page.
        """
        api_manager.movies_api.get_movies(params={"page": -1}, expected_status=HTTPStatus.BAD_REQUEST)

    def test_movies_with_invalid_created_at(self, api_manager: ApiManager):
        """
        Негативный тест на получение списка афиш фильмов с некорректным параметром createdAt.
        """
        api_manager.movies_api.get_movies(params={"createdAt": "wrong"}, expected_status=HTTPStatus.BAD_REQUEST)

    def test_get_nonexistent_movie(self, api_manager: ApiManager):
        """
        Негативный тест на получение информации о несуществующем фильме.
        """
        api_manager.movies_api.get_movie(999999999, expected_status=HTTPStatus.NOT_FOUND)

    def test_create_invalid_movie_data(self, api_manager: ApiManager, invalid_movie_data: dict):
        """
        Негативный тест на создание афиши фильма с пустым полем name.
        """
        api_manager.auth_api.authenticate_super_admin()
        api_manager.movies_api.create_movie(invalid_movie_data, expected_status=HTTPStatus.BAD_REQUEST)

    def test_create_movie_by_user(self, authorized_registered_user: ApiManager, movie_data: dict, registered_user: dict):
        """
        Негативный тест на создание афиши фильма (под авторизованным пользователем).
        """
        authorized_registered_user.auth_api.authenticate((registered_user["email"], registered_user["password"]))
        authorized_registered_user.movies_api.create_movie(movie_data, expected_status=HTTPStatus.FORBIDDEN)

    def test_create_same_movie(self, authorized_super_admin: ApiManager, movie_data: dict, movies_to_cleanup: list):
        """
        Негативный тест на создание афиши фильма с теми же данными, что и уже существующего.
        """
        authorized_super_admin.auth_api.authenticate_super_admin()
        response = authorized_super_admin.movies_api.create_movie(movie_data)
        created_movie_id = response.json()["id"]
        authorized_super_admin.movies_api.create_movie(movie_data, expected_status=HTTPStatus.CONFLICT)
        movies_to_cleanup.append(created_movie_id)

    def test_change_movie_with_invalid_data(self, authorized_super_admin: ApiManager, movie_data: dict, invalid_movie_data: dict, movies_to_cleanup: list):
        """
        Негативный тест на изменение афиши фильма с некорректными данными.
        """
        response = authorized_super_admin.movies_api.create_movie(movie_data)
        created_movie_id = response.json()["id"]
        authorized_super_admin.movies_api.get_movie(created_movie_id, expected_status=HTTPStatus.OK)
        authorized_super_admin.movies_api.change_movie(created_movie_id, invalid_movie_data, expected_status=HTTPStatus.BAD_REQUEST)
        movies_to_cleanup.append(created_movie_id)

    @pytest.mark.skip(reason="Баг в ответе API, ожидаемый ответ BAD_REQUEST, приходит NOT_FOUND")
    def test_change_movie_with_empty_data(self, authorized_super_admin: ApiManager, movie_data: dict, empty_name_movie: dict, movies_to_cleanup: list):
        """
        Негативный тест на изменение афиши фильма с пустыми данными.
        """
        response = authorized_super_admin.movies_api.create_movie(movie_data)
        created_movie_id = response.json()["id"]
        authorized_super_admin.movies_api.get_movie(created_movie_id, expected_status=HTTPStatus.OK)
        authorized_super_admin.movies_api.change_movie(created_movie_id, empty_name_movie, expected_status=HTTPStatus.BAD_REQUEST)
        movies_to_cleanup.append(created_movie_id)

    def test_change_movie_by_user(self, authorized_registered_user: ApiManager, created_movie_and_cleanup, movie_data: dict, registered_user: dict):
        """
        Негативный тест на изменение афиши фильма (под пользователем).
        """
        created_movie_id = created_movie_and_cleanup["id"]
        authorized_registered_user.auth_api.authenticate((registered_user["email"], registered_user["password"]))
        authorized_registered_user.movies_api.change_movie(created_movie_id, movie_data, expected_status=HTTPStatus.FORBIDDEN)

    def test_change_nonexistent_movie(self, authorized_super_admin: ApiManager):
        """
        Негативный тест на изменение информации о несуществующем фильме.
        """
        authorized_super_admin.auth_api.authenticate_super_admin()
        authorized_super_admin.movies_api.change_movie(999999999, {"name": "Новый фильм"}, expected_status=HTTPStatus.NOT_FOUND)

    def test_delete_movie_by_user(self, created_movie_and_cleanup: dict, authorized_registered_user: ApiManager, registered_user: dict):
        """
        Негативный тест на удаление афиши фильма (под пользователем).
        """
        created_movie_id = created_movie_and_cleanup["id"]
        authorized_registered_user.auth_api.authenticate((registered_user["email"], registered_user["password"]))
        authorized_registered_user.movies_api.delete_movie(created_movie_id, expected_status=HTTPStatus.FORBIDDEN)

    def test_delete_movie_with_invalid_id(self, authorized_super_admin: ApiManager):
        """
        Негативный тест на удаление афиши несуществующего фильма.
        """
        authorized_super_admin.auth_api.authenticate_super_admin()
        authorized_super_admin.movies_api.delete_movie(999999999, expected_status=HTTPStatus.NOT_FOUND)