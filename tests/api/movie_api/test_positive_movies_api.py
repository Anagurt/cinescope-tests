import pytest
from clients.api_manager import ApiManager

from http import HTTPStatus


class TestMoviesAPIPositive:
    def test_get_movies(self, api_manager: ApiManager):
        """
        Тест на получение списка афиш фильмов (под правами не авторизованного пользователя).
        """
        response = api_manager.movies_api.get_movies()
        response_data = response.json()
        assert "movies" in response_data, "Отсутствие списков фильмов в ответе"


    def test_create_movie(self, movie_data: dict, authorized_super_admin: ApiManager, movies_to_cleanup: list):
        """
        Тест на создание афиши фильма (под админскими правами).
        """
        response = authorized_super_admin.movies_api.create_movie(movie_data)
        response_data = response.json()
        movie_id = response_data["id"]
        assert "id" in response_data, "ID фильма отсутствует в ответе"
        response_movie_data = {key: response_data[key] for key in movie_data.keys()}
        assert response_movie_data == movie_data, "Данные в ответе не совпадают с отправленными"
        movies_to_cleanup.append(movie_id)


    def test_get_movie_by_super_admin(self, created_movie_and_cleanup: dict, authorized_super_admin: ApiManager):
        from datetime import datetime, timezone, timedelta

        """
        Тест на получение информации о созданной афише фильма (под админскими правами).
        """
        response = authorized_super_admin.movies_api.get_movie(created_movie_and_cleanup["id"])
        response_data = response.json()
        assert created_movie_and_cleanup["id"] == response_data["id"], "ID фильма не совпадает"
        expected_keys = {"id", "name", "price", "description", "imageUrl", "location", "published", "genreId", "createdAt", "rating", "reviews"}
        assert expected_keys.issubset(response_data.keys()), "Не все ключи присутствуют в ответе"
        created_at = datetime.fromisoformat(response_data["createdAt"].replace("Z", "+00:00"))
        assert abs(datetime.now(timezone.utc) - created_at) <= timedelta(seconds=2), "Дата создания фильма отличается от текущего времени больше чем на 2 секунды"


    def test_get_movie_by_user(self, created_movie_and_cleanup: dict, authorized_super_admin: ApiManager, authorized_registered_user: ApiManager):
        from datetime import datetime, timezone, timedelta

        """
        Тест на получение информации о созданной афише фильма (под авторизованным пользователем).
        """
        response = authorized_super_admin.movies_api.get_movie(created_movie_and_cleanup["id"])
        created_movie_id = response.json()["id"]
        response = authorized_registered_user.movies_api.get_movie(created_movie_id, expected_status=HTTPStatus.OK)
        get_movie_data = response.json()
        assert created_movie_id == get_movie_data["id"], "ID фильма не совпадает"
        expected_keys = {"id", "name", "price", "description", "imageUrl", "location", "published", "genreId", "createdAt", "rating", "reviews"}
        assert expected_keys.issubset(get_movie_data.keys()), "Не все ключи присутствуют в ответе"
        created_at = datetime.fromisoformat(get_movie_data["createdAt"].replace("Z", "+00:00"))
        assert abs(datetime.now(timezone.utc) - created_at) <= timedelta(seconds=2), "Дата создания фильма отличается от текущего времени больше чем на 2 секунды" 


    def test_change_movie_by_super_admin(self, created_movie_and_cleanup: dict, change_movie_data: dict, authorized_super_admin: ApiManager):
        """
        Тест на изменение афиши фильма (под админскими правами).
        """
        response = authorized_super_admin.movies_api.get_movie(created_movie_and_cleanup["id"])
        created_movie_data = response.json()
        created_movie_id = response.json()["id"]
        response_changed_movie = authorized_super_admin.movies_api.change_movie(created_movie_id, change_movie_data, expected_status=HTTPStatus.OK)
        changed_movie_data = response_changed_movie.json()
        assert created_movie_id == changed_movie_data["id"], "ID фильма не совпадает"
        assert created_movie_data["name"] != changed_movie_data["name"], "Название фильма совпадает"
        assert created_movie_data["description"] != changed_movie_data["description"], "Описание фильма совпадает"
        assert created_movie_data["price"] != changed_movie_data["price"], "Цена фильма совпадает"


    def test_delete_movie_by_super_admin(self, created_movie_and_cleanup: dict, authorized_super_admin: ApiManager):
        """
        Тест на удаление афиши фильма (под админскими правами).
        """
        response = authorized_super_admin.movies_api.get_movie(created_movie_and_cleanup["id"])
        created_movie_id = response.json()["id"]
        authorized_super_admin.movies_api.delete_movie(created_movie_id)
        authorized_super_admin.movies_api.get_movie(created_movie_id, expected_status=HTTPStatus.NOT_FOUND)


