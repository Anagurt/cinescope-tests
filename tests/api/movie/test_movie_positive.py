from http import HTTPStatus

import allure
import pytest

from models.base_model_movies import GetMoviesListResponse, GetMovieByIdResponse
from models.base_model_movies import MovieInfoResponse, MovieInfoRequest
from utils.data_generator import DataGenerator
from entities.location import Location

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


@allure.feature("Позитивные тесты для movies API")
class TestMoviesAPIPositive:
    @pytest.mark.smoke
    @allure.story("Тест на получение списка афиш фильмов (под неавторизованным пользователем)")
    @pytest.mark.parametrize(
        "params", [
            {"minPrice": 9, "maxPrice": 10},
            {"locations": "MSK"},
            {"genreId": 1}],
            ids=["Фильмы в диапазоне цен", "Фильмы в Москве", "Фильмы в жанре с ID 1"])
    def test_get_movies_unauthorized_user(self, anonymous_api_manager, params):
        response = anonymous_api_manager.movies_api.get_movies(params=params)
        data = response.json()
        movies_list_response = GetMoviesListResponse.model_validate(data)
        if "minPrice" in params and "maxPrice" in params:
            min_price, max_price = params["minPrice"], params["maxPrice"]
            assert all(
                min_price <= movie.price <= max_price
                for movie in movies_list_response.movies
                )    
        if "locations" in params:
            expected_location = params["locations"]
            assert all(
                movie.location == expected_location
                for movie in movies_list_response.movies
            )
        if "genreId" in params:
            expected_genre_id = params["genreId"]
            assert all(
                movie.genreId == expected_genre_id
                for movie in movies_list_response.movies
            )


    @pytest.mark.smoke
    @allure.story("Тест на создание афиши фильма (под админскими правами)")
    def test_create_movie_by_super_admin(self, movie_data: MovieInfoRequest, super_admin, movies_to_cleanup: list):
        response = super_admin.api.movies_api.post_movie(movie_data, expected_status=HTTPStatus.CREATED)
        created = MovieInfoResponse.model_validate(response.json())

        _assert_create_movie_echoes_request(
            movie_data.model_dump(mode="json"),
            created.model_dump(mode="json"),
            )

        movies_to_cleanup.append(created.id)


    @pytest.mark.smoke
    @allure.story("Тест на получение информации о созданной афише фильма (под админскими правами)")
    def test_get_movie_by_super_admin(self, created_movie_and_cleanup: MovieInfoResponse, super_admin):
        response = super_admin.api.movies_api.get_movie(created_movie_and_cleanup.id, expected_status=HTTPStatus.OK)
        created = GetMovieByIdResponse.model_validate(response.json())
        assert created.id == created_movie_and_cleanup.id


    @pytest.mark.smoke
    @allure.story("Тест на получение информации о созданной афише фильма (под авторизованным пользователем)")
    def test_get_movie_by_registered_user(self, created_movie_and_cleanup: MovieInfoResponse, regular_user):
        response = regular_user.api.movies_api.get_movie(created_movie_and_cleanup.id, expected_status=HTTPStatus.OK)
        created = GetMovieByIdResponse.model_validate(response.json())
        assert created.id == created_movie_and_cleanup.id


    @pytest.mark.smoke
    @allure.story("Тест на изменение афиши фильма (под админскими правами)")
    def test_change_movie_by_super_admin(self, created_movie_and_cleanup: MovieInfoResponse, super_admin):
        change_movie_data = MovieInfoRequest(
            name=DataGenerator.generate_random_name_movie(),
            imageUrl="https://example.com/image.png",
            price=DataGenerator.generate_random_price_movie(),
            description=DataGenerator.generate_random_description_movie(),
            location=Location.SPB,
            published=True,
            genreId=2,
        )
        response = super_admin.api.movies_api.patch_movie(created_movie_and_cleanup.id, change_movie_data.model_dump(mode="json"), expected_status=HTTPStatus.OK)
        changed = MovieInfoResponse.model_validate(response.json())
        assert changed.id == created_movie_and_cleanup.id
        assert changed.name == change_movie_data.name
        assert changed.name != created_movie_and_cleanup.name


    @pytest.mark.smoke
    @allure.story("Тест на удаление афиши фильма (под админскими правами)")
    def test_delete_movie_by_super_admin(self, created_movie_and_cleanup: MovieInfoResponse, super_admin):
        response = super_admin.api.movies_api.delete_movie(created_movie_and_cleanup.id, expected_status=HTTPStatus.OK)
        deleted = MovieInfoResponse.model_validate(response.json())
        assert deleted.id == created_movie_and_cleanup.id
        super_admin.api.movies_api.get_movie(created_movie_and_cleanup.id, expected_status=HTTPStatus.NOT_FOUND)