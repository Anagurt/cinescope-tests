from http import HTTPStatus

import pytest
import requests

from clients.api_manager import ApiManager
from utils.data_generator import DataGenerator


@pytest.fixture(scope="session")
def session():
    """
    Фикстура для создания HTTP-сессии.
    """
    http_session = requests.Session()

    yield http_session

    http_session.close()


@pytest.fixture(scope="session")
def api_manager(session):
    """
    Фикстура для создания экземпляра ApiManager.
    """
    return ApiManager(session)


@pytest.fixture()
def anonymous_api_manager():
    """
    Фикстура для создания экземпляра ApiManager без заголовков авторизации
    """
    http_session = requests.Session()
    try:
        yield ApiManager(http_session)
    finally:
        http_session.close()


# AuthAPI фикстуры
@pytest.fixture()
def new_user():
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"]
    }


@pytest.fixture(scope="session")
def registered_user(api_manager: ApiManager):
    """
    Фикстура для регистрации и получения данных зарегистрированного пользователя.
    """
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()
    user_data = {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"]
    }

    response = api_manager.auth_api.register_user(user_data, expected_status=HTTPStatus.CREATED)
    response_data = response.json()
    user = user_data.copy()
    user["id"] = response_data["id"]
    return user


@pytest.fixture(scope="session")
def authorized_registered_user(api_manager: ApiManager, registered_user: dict):
    api_manager.auth_api.authenticate((registered_user["email"], registered_user["password"]))

    return api_manager


@pytest.fixture(scope="session")
def authorized_super_admin(api_manager: ApiManager):
    api_manager.auth_api.authenticate()

    return api_manager


def _delete_ok_or_gone(response: requests.Response, context: str):
    if response.status_code in (HTTPStatus.OK, HTTPStatus.NOT_FOUND):
        return

    raise RuntimeError(
        f"{context}: unexpected status {response.status_code}, body: {response.text!r}"
    )


@pytest.fixture()
def created_user_and_cleanup(api_manager: ApiManager, authorized_super_admin: ApiManager, new_user: dict):
    response = api_manager.auth_api.register_user(new_user, expected_status=HTTPStatus.CREATED)
    response_data = response.json()

    created_user = new_user.copy()
    created_user["id"] = response_data["id"]

    yield created_user

    authorized_super_admin.auth_api.authenticate()

    response = authorized_super_admin.user_api.delete_user(
        created_user["id"],
        expected_status=None,
    )
    _delete_ok_or_gone(response, "delete user")


@pytest.fixture()
def users_to_cleanup(authorized_super_admin: ApiManager):
    created_user_ids = []

    yield created_user_ids

    authorized_super_admin.auth_api.authenticate()

    for user_id in created_user_ids:
        response = authorized_super_admin.user_api.delete_user(user_id, expected_status=None)
        _delete_ok_or_gone(response, f"delete user {user_id} in users_to_cleanup")


# Фикстуры для MoviesAPI
@pytest.fixture()
def movie_data():
    """
    Фикстура для генерации случайного фильма.
    """
    return {
        "name": DataGenerator.generate_random_name_movie(),
        "imageUrl": "https://example.com/image.png",
        "price": DataGenerator.generate_random_price_movie(),
        "description": DataGenerator.generate_random_description_movie(),
        "location": "SPB",
        "published": True,
        "genreId": 1,
    }


@pytest.fixture()
def created_movie_and_cleanup(authorized_super_admin: ApiManager, movie_data: dict):
    """
    Фикстура для создания фильма и удаления его после теста.
    """
    authorized_super_admin.auth_api.authenticate()

    response = authorized_super_admin.movies_api.post_movie(movie_data, expected_status=HTTPStatus.CREATED)
    response_data = response.json()

    created_movie = movie_data.copy()
    created_movie["id"] = response_data["id"]

    yield created_movie

    authorized_super_admin.auth_api.authenticate()

    response = authorized_super_admin.movies_api.delete_movie(
        created_movie["id"],
        expected_status=None,
    )
    _delete_ok_or_gone(response, "delete movie")


@pytest.fixture(scope="session")
def movies_to_cleanup(authorized_super_admin: ApiManager):
    """
    Список id фильмов на удаление в конце сессии для подчистки фильмов с меткой в name.
    """
    created_movie_ids = []

    yield created_movie_ids

    authorized_super_admin.auth_api.authenticate()

    for movie_id in dict.fromkeys(created_movie_ids):
        response = authorized_super_admin.movies_api.delete_movie(movie_id, expected_status=None)
        _delete_ok_or_gone(response, f"delete movie {movie_id} in movies_to_cleanup")
