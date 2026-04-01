from http import HTTPStatus

import pytest
import requests

from clients.api_manager import ApiManager
from utils.data_generator import DataGenerator

from entities.user import User
from resources.user_creds import SuperAdminCreds

from entities.roles import Roles


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


@pytest.fixture
def user_session():
    """
    Фикстура для создания сессии юзера
    """
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()


@pytest.fixture
def super_admin(user_session):
    """
    Фикстура для создания супер-админа
    """
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_session)

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin


@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    """
    Фикстура для создания обычного пользователя (объект класса User)
    """
    new_session = user_session()

    common_user = User(
        creation_user_data['email'],
        creation_user_data['password'],
        [Roles.USER.value],
        new_session)

    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user


@pytest.fixture
def new_user():
    """
    Фикстура для генерации данных для нового пользователя «сырье»
    """
    random_password = DataGenerator.generate_random_password()

    return {
        "email": DataGenerator.generate_random_email(),
        "fullName": DataGenerator.generate_random_name(),
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": [Roles.USER.value]
    }


@pytest.fixture(scope="function")
def creation_user_data(new_user):
    """
    Фикстура для генерации данных для нового пользователя (объект класса User)
    """
    updated_data = new_user.copy()
    updated_data.update({
        "verified": True,
        "banned": False
    })
    return updated_data

#___________________________________________________________


def _delete_ok_or_gone(response: requests.Response, context: str):
    if response.status_code in (HTTPStatus.OK, HTTPStatus.NOT_FOUND):
        return

    raise RuntimeError(
        f"{context}: unexpected status {response.status_code}, body: {response.text!r}"
    )


@pytest.fixture()
def created_user_and_cleanup(super_admin: User, new_user: dict):
    response = super_admin.api.auth_api.register_user(new_user, expected_status=HTTPStatus.CREATED)
    created_user = new_user.copy()
    created_user["id"] = response.json()["id"]

    yield created_user

    response = super_admin.api.user_api.delete_user(
        created_user["id"],
        expected_status=None,
    )
    _delete_ok_or_gone(response, "delete user")


@pytest.fixture()
def users_to_cleanup(super_admin: User):
    created_user_ids = []

    yield created_user_ids

    for user_id in created_user_ids:
        response = super_admin.api.user_api.delete_user(user_id, expected_status=None)
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
def created_movie_and_cleanup(super_admin: User, movie_data: dict):
    """
    Фикстура для создания фильма и удаления его после теста.
    """
    super_admin.api.auth_api.authenticate()

    response = super_admin.api.movies_api.post_movie(movie_data, expected_status=HTTPStatus.CREATED)
    response_data = response.json()

    created_movie = movie_data.copy()
    created_movie["id"] = response_data["id"]

    yield created_movie

    super_admin.api.auth_api.authenticate()

    response = super_admin.api.movies_api.delete_movie(
        created_movie["id"],
        expected_status=None,
    )
    _delete_ok_or_gone(response, "delete movie")


@pytest.fixture(scope="session")
def movies_to_cleanup(super_admin: User):
    """
    Список id фильмов на удаление в конце сессии для подчистки фильмов с меткой в name.
    """
    created_movie_ids = []

    yield created_movie_ids

    super_admin.api.auth_api.authenticate()

    for movie_id in dict.fromkeys(created_movie_ids):
        response = super_admin.api.movies_api.delete_movie(movie_id, expected_status=None)
        _delete_ok_or_gone(response, f"delete movie {movie_id} in movies_to_cleanup")
