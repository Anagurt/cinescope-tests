from datetime import datetime, timedelta, timezone
from http import HTTPStatus

import allure

from clients.api_manager import ApiManager


def _assert_create_movie_echoes_request(movie_data: dict, response_data: dict):
    """
    Сравнивает поля запроса с телом ответа (при расхождении сообщение указывает конкретный ключ)
    """
    mismatches = []
    for key in movie_data:
        if key not in response_data:
            mismatches.append(f"{key}: нет в ответе")
            continue
        expected = movie_data[key]
        actual = response_data[key]
        if actual != expected:
            mismatches.append(f"{key}: ожидалось {expected!r}, в ответе {actual!r}")
    assert not mismatches, "Поля create_movie не совпадают с запросом:\n" + "\n".join(mismatches)


@allure.feature("Positive tests for movies API")
class TestMoviesAPIPositive:
    @allure.story("Тест на получение списка афиш фильмов (под неавторизованным пользователем)")
    def test_get_movies_unauthorized_user(self, anonymous_api_manager: ApiManager):
        response = anonymous_api_manager.movies_api.get_movies()
        response_data = response.json()

        assert "movies" in response_data, "Отсутствие списков фильмов в ответе"

    @allure.story("Тест на создание афиши фильма (под админскими правами)")
    def test_create_movie_by_super_admin(self, movie_data: dict, authorized_super_admin: ApiManager, movies_to_cleanup: list):
        response = authorized_super_admin.movies_api.post_movie(movie_data)
        response_data = response.json()

        movie_id = response_data.get("id")
        assert movie_id is not None, f"У только что созданного фильма с name={movie_data['name']} в ответе отсутствует id"

        _assert_create_movie_echoes_request(movie_data, response_data)

        movies_to_cleanup.append(movie_id)

    @allure.story("Тест на получение информации о созданной афише фильма (под админскими правами)")
    def test_get_movie_by_super_admin(self, created_movie_and_cleanup: dict, authorized_super_admin: ApiManager):
        response = authorized_super_admin.movies_api.get_movie(created_movie_and_cleanup["id"])
        response_data = response.json()

        response_id = response_data.get("id")
        assert response_id is not None, f"В ответе get_movie созданного фильма с name={created_movie_and_cleanup['name']} отсутствует id"
        assert created_movie_and_cleanup["id"] == response_id, f"id фильма не совпадает, ожидалось {created_movie_and_cleanup['id']}, в ответе {response_id}"
        expected_keys = {"id", "name", "price", "description", "imageUrl", "location", "published", "genreId", "createdAt", "rating", "reviews"}
        assert expected_keys.issubset(response_data.keys()), "Не все ключи присутствуют в ответе"

        created_at_raw = response_data.get("createdAt")
        assert created_at_raw is not None, "В ответе get_movie отсутствует поле createdAt"
        created_at = datetime.fromisoformat(created_at_raw.replace("Z", "+00:00"))
        assert abs(datetime.now(timezone.utc) - created_at) <= timedelta(seconds=2), "Дата создания фильма отличается от текущего времени больше чем на 2 секунды"

    @allure.story("Тест на получение информации о созданной афише фильма (под авторизованным пользователем)")
    def test_get_movie_by_registered_user(self, created_movie_and_cleanup: dict, authorized_super_admin: ApiManager, authorized_registered_user: ApiManager):
        response = authorized_super_admin.movies_api.get_movie(created_movie_and_cleanup["id"])
        created_movie_id = response.json().get("id")
        assert created_movie_id is not None, "В ответе get_movie (admin) отсутствует поле id"

        response = authorized_registered_user.movies_api.get_movie(created_movie_id)
        get_movie_data = response.json()

        get_id = get_movie_data.get("id")
        assert get_id is not None, f"В ответе get_movie созданного фильма с id={created_movie_id} отсутствует поле id"
        assert created_movie_id == get_id, f"id фильма не совпадает, ожидалось {created_movie_id}, в ответе {get_id}"
        expected_keys = {"id", "name", "price", "description", "imageUrl", "location", "published", "genreId", "createdAt", "rating", "reviews"}
        assert expected_keys.issubset(get_movie_data.keys()), "Не все ключи присутствуют в ответе"

        created_at_raw = get_movie_data.get("createdAt")
        assert created_at_raw is not None, "Поле createdAt в ответе отсутствует или null"
        created_at = datetime.fromisoformat(created_at_raw.replace("Z", "+00:00"))
        assert abs(datetime.now(timezone.utc) - created_at) <= timedelta(seconds=2), "Дата создания фильма отличается от текущего времени больше чем на 2 секунды"

    @allure.story("Тест на изменение афиши фильма (под админскими правами)")
    def test_change_movie_by_super_admin(self, created_movie_and_cleanup: dict, authorized_super_admin: ApiManager):
        response = authorized_super_admin.movies_api.get_movie(created_movie_and_cleanup["id"])
        created_movie_data = response.json()
        created_movie_id = created_movie_data.get("id")
        assert created_movie_id is not None, "В ответе get_movie отсутствует поле id"
        change_movie_data = created_movie_and_cleanup.copy()
        change_movie_data["name"] = "Новый фильм"

        response_changed_movie = authorized_super_admin.movies_api.patch_movie(created_movie_id, change_movie_data)
        changed_movie_data = response_changed_movie.json()

        changed_id = changed_movie_data.get("id")
        assert changed_id is not None, f"В ответе patch_movie созданного фильма с id={created_movie_id} отсутствует поле ID"
        assert created_movie_id == changed_id, f"id фильма не совпадает, ожидалось {created_movie_id}, в ответе {changed_id}"
        assert created_movie_data["name"] != changed_movie_data["name"], "Название фильма совпадает с измененным"
        

    @allure.story("Тест на удаление афиши фильма (под админскими правами)")
    def test_delete_movie_by_super_admin(self, movie_data: dict, authorized_super_admin: ApiManager):    
        response = authorized_super_admin.movies_api.post_movie(movie_data)
        created_movie_id = response.json().get("id")
        assert created_movie_id is not None, "В ответе get_movie отсутствует поле id"

        authorized_super_admin.movies_api.delete_movie(created_movie_id)
        authorized_super_admin.movies_api.get_movie(created_movie_id, expected_status=HTTPStatus.NOT_FOUND)
