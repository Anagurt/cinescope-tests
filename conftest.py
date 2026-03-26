import requests
import pytest

from constants import (
    BASE_AUTH_URL,
    BASE_MOVIES_URL,
    HEADERS,
    LOGIN_ENDPOINT,
    REGISTER_ENDPOINT
)
from custom_requester.custom_requester import CustomRequester
from utils.data_generator import DataGenerator
from clients.api_manager import ApiManager

import os
from dotenv import load_dotenv
load_dotenv()
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")


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
@pytest.fixture(scope="session")
def auth_requester():
    """
    Фикстура для создания экземпляра CustomRequester для auth_API.
    """
    session = requests.Session()
    session.headers.update(HEADERS)
    return CustomRequester(session=session, base_url=BASE_AUTH_URL)


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
def registered_user(auth_requester, test_user):
    """
    Фикстура для регистрации и получения данных зарегистрированного пользователя.
    """
    response = auth_requester.send_request(
        method="POST",
        endpoint=REGISTER_ENDPOINT,
        data=test_user,
        expected_status=201
    )
    response_data = response.json()
    registered_user = test_user.copy()
    registered_user["id"] = response_data["id"]
    return registered_user


@pytest.fixture(scope="session")
def auth_session(auth_requester, registered_user):
    """
    Фикстура для авторизованного состояния пользователя.
    """
    login_data = {
        "email": registered_user["email"],
        "password": registered_user["password"]
    }
    response = auth_requester.send_request(
        method = "POST",
        endpoint = LOGIN_ENDPOINT,
        data=login_data,
        expected_status = 200
    )
    token = response.json().get("accessToken")
    session = requests.Session()
    session.headers.update(HEADERS)
    session.headers.update({"Authorization": f"Bearer {token}"})
    return session

# Фикстуры для генерации данных для негативных тестов AuthAPI
@pytest.fixture()
def empty_password_user(new_user):
    """
    Фикстура для генерации пользователя с пустым полем пароля.
    """
    new_user["password"] = ""
    new_user["passwordRepeat"] = ""
    return new_user

@pytest.fixture()
def empty_email_user(new_user):
    """
    Фикстура для генерации пользователя с пустым полем email.
    """
    new_user["email"] = ""
    return new_user

@pytest.fixture()
def user_with_email_at_less(new_user):
    """
    Фикстура для генерации пользователя с email без символа @.
    """
    new_user["email"] = "example.come"
    return new_user

@pytest.fixture()
def empty_data_user(new_user):
    """
    Фикстура для генерации пользователя с пустыми полями email и password.
    """
    new_user["email"] = ""
    new_user["password"] = ""
    return new_user

# MoviesAPI фикстуры
@pytest.fixture(scope="session")
def movies_requester():
    """
    Фикстура для создания экземпляра CustomRequester для movies_API.
    """
    session = requests.Session()
    session.headers.update(HEADERS)
    return CustomRequester(session=session, base_url=BASE_MOVIES_URL)


@pytest.fixture(scope="session")
def user_movies_requester(auth_session):
    """
    CustomRequester для movies API под обычным пользователем
    """
    return CustomRequester(session=auth_session, base_url=BASE_MOVIES_URL)


@pytest.fixture(scope="session")
def super_admin_movies_requester(auth_requester):
    """
    Фикстура с авторизацией под админскими правами и созданием экземпляра CustomRequester для movies_API
    """
    login_data = {
        "email": ADMIN_EMAIL,
        "password": ADMIN_PASSWORD,
    }
    response = auth_requester.send_request(
        method="POST",
        endpoint=LOGIN_ENDPOINT,
        data=login_data,
        expected_status=200
    )
    token = response.json()["accessToken"]
    session = requests.Session()
    session.headers.update(HEADERS)
    session.headers.update({"Authorization": f"Bearer {token}"})
    return CustomRequester(session=session, base_url=BASE_MOVIES_URL)


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
def empty_name_movie(movie_data):
    """
    Фикстура для генерации данных для афиши фильма с пустым полем name.
    """
    bad_movie_data = movie_data.copy()
    bad_movie_data["name"] = ""
    return bad_movie_data

