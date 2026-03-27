import requests
import pytest
from http import HTTPStatus
from utils.data_generator import DataGenerator
from clients.api_manager import ApiManager


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
def test_user():
    """
    Фикстура для генерации случайного пользователя.
    """
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
def registered_user(api_manager: ApiManager, test_user: dict):
    """
    Фикстура для регистрации и получения данных зарегистрированного пользователя.
    """
    response = api_manager.auth_api.register_user(test_user, expected_status=HTTPStatus.CREATED)
    response_data = response.json()
    registered_user = test_user.copy()
    registered_user["id"] = response_data["id"]
    return registered_user

@pytest.fixture(scope="session")
def authorized_registered_user(api_manager: ApiManager, registered_user: dict):
    api_manager.auth_api.authenticate((registered_user["email"], registered_user["password"]))
    return api_manager

@pytest.fixture(scope="session")
def authorized_super_admin(api_manager: ApiManager):
    api_manager.auth_api.authenticate_super_admin()
    return api_manager

@pytest.fixture()
def created_user_and_cleanup(api_manager: ApiManager, authorized_super_admin: ApiManager, new_user: dict):
    response = api_manager.auth_api.register_user(new_user, expected_status=HTTPStatus.CREATED)
    response_data = response.json()
    created_user = new_user.copy()
    created_user["id"] = response_data["id"]
    yield created_user
    api_manager.auth_api.authenticate_super_admin()
    try:
        authorized_super_admin.user_api.delete_user(created_user["id"], expected_status=HTTPStatus.OK)
    except ValueError:
        authorized_super_admin.user_api.delete_user(created_user["id"], expected_status=HTTPStatus.NOT_FOUND)

@pytest.fixture()
def users_to_cleanup(authorized_super_admin: ApiManager):
    created_user_ids = []
    yield created_user_ids
    for user_id in created_user_ids:
        authorized_super_admin.user_api.delete_user(user_id, expected_status=HTTPStatus.OK)


# Фикстуры для генерации данных для негативных тестов AuthAPI
@pytest.fixture()
def empty_password_user(new_user: dict):
    """
    Фикстура для генерации пользователя с пустым полем пароля.
    """
    new_user["password"] = ""
    new_user["passwordRepeat"] = ""
    return new_user

@pytest.fixture()
def empty_email_user(new_user: dict):
    """
    Фикстура для генерации пользователя с пустым полем email.
    """
    new_user["email"] = ""
    return new_user

@pytest.fixture()
def user_with_email_at_less(new_user: dict):
    """
    Фикстура для генерации пользователя с email без символа @.
    """
    new_user["email"] = "example.come"
    return new_user

@pytest.fixture()
def empty_data_user(new_user: dict):
    """
    Фикстура для генерации пользователя с пустыми полями email и password.
    """
    new_user["email"] = ""
    new_user["password"] = ""
    return new_user

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
    authorized_super_admin.auth_api.authenticate_super_admin()
    response = authorized_super_admin.movies_api.create_movie(movie_data, expected_status=HTTPStatus.CREATED)
    response_data = response.json()
    created_movie = movie_data.copy()
    created_movie["id"] = response_data["id"]
    yield created_movie
    authorized_super_admin.auth_api.authenticate_super_admin()
    try:
        authorized_super_admin.movies_api.delete_movie(
            created_movie["id"],
            expected_status=HTTPStatus.OK
        )
    except ValueError:
        authorized_super_admin.movies_api.delete_movie(
            created_movie["id"],
            expected_status=HTTPStatus.NOT_FOUND
        )

@pytest.fixture()
def movies_to_cleanup(authorized_super_admin: ApiManager):
    created_movie_ids = []
    yield created_movie_ids
    authorized_super_admin.auth_api.authenticate_super_admin()
    for movie_id in created_movie_ids:
        authorized_super_admin.movies_api.delete_movie(movie_id, expected_status=HTTPStatus.OK)

@pytest.fixture()
def change_movie_data():
    """
    Фикстура для генерации данных для изменения фильма.
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


# Фикстуры для генерации данных для негативных тестов MoviesAPI
@pytest.fixture()
def invalid_movie_data():
    """
    Фикстура для генерации некорректных данных для афиши фильма.
    """
    return {
        "name": "",
        "imageUrl": "",
        "price": -1,
        "description": "",
        "location": "",
        "published": False,
        "genreId": 0,
    }

@pytest.fixture()
def empty_name_movie(movie_data: dict):
    """
    Фикстура для генерации данных для афиши фильма с пустым полем name.
    """
    bad_movie_data = movie_data.copy()
    bad_movie_data["name"] = ""
    return bad_movie_data

