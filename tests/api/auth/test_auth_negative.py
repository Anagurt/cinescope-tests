from http import HTTPStatus

import allure
import pytest

from models.base_models_auth import (
    RegisterUserRequest,
    LoginUserUnauthorizedResponse,
    RegisterUserBadRequestResponse,
    RegisterUserConflictResponse,
)

from db_requester.db_helpers import DBHelper
from clients.api_manager import ApiManager
from tests.constants.auth_cases import (
    REGISTER_EMPTY_FIELDS_CASES,
    REGISTER_EMPTY_FIELDS_IDS,
    REGISTER_ALREADY_EXISTS_CASES,
    REGISTER_ALREADY_EXISTS_IDS,
    REGISTER_INVALID_FIELDS_CASES,
    REGISTER_INVALID_FIELDS_IDS,
    LOGIN_EMPTY_FIELDS_CASES,
    LOGIN_EMPTY_FIELDS_IDS,
)


@allure.feature("Негативные тесты для auth API")
class TestAuthAPINegative:

    @pytest.mark.smoke
    @pytest.mark.negative
    @allure.story(
        "Негативный тест на регистрацию пользователя с пустыми полями")
    @pytest.mark.parametrize(
        "email, full_name, password, password_repeat",
        REGISTER_EMPTY_FIELDS_CASES,
        ids=REGISTER_EMPTY_FIELDS_IDS,
    )
    def test_register_user_with_empty_fields(
            self,
            email: str,
            full_name: str,
            password: str,
            password_repeat: str,
            api_manager,
            db_helper: DBHelper,
            expected_status: HTTPStatus = HTTPStatus.BAD_REQUEST
    ):
        register_data = {
            "email": email,
            "fullName": full_name,
            "password": password,
            "passwordRepeat": password_repeat
        }
        api_manager.auth_api.register_user(
            user_data=register_data,
            expected_status=expected_status,
            response_model=RegisterUserBadRequestResponse,
            attach_error_messages=True,
        )
        if db_helper.user_exists_by_email(email):
            raise AssertionError(
                f"Пользователь {email} зарегистрирован в БД, "
                "ожидалось, что пользователь не сможет зарегистрироваться"
            )
        # assert not db_helper.user_exists_by_email(email)

    @pytest.mark.smoke
    @pytest.mark.negative
    @allure.story(
        "Негативный тест на регистрацию уже существующего пользователя")
    @pytest.mark.parametrize(
        "email, full_name, password, password_repeat",
        REGISTER_ALREADY_EXISTS_CASES,
        ids=REGISTER_ALREADY_EXISTS_IDS,
    )
    def test_register_already_exist_user(
            self,
            email: str,
            full_name: str,
            password: str,
            password_repeat: str,
            api_manager: ApiManager,
            db_helper: DBHelper,
            expected_status: HTTPStatus = HTTPStatus.CONFLICT,
    ):
        register_data = {
            "email": email,
            "fullName": full_name,
            "password": password,
            "passwordRepeat": password_repeat
        }
        if not db_helper.user_exists_by_email(email):
            raise AssertionError(
                f"Пользователь {email} не существует в БД, "
                "ожидался существующий пользователь"
            )
        # assert db_helper.user_exists_by_email(email)
        response = api_manager.auth_api.register_user(
            user_data=register_data, expected_status=expected_status)
        register_user_response = RegisterUserConflictResponse.model_validate(
            response.json())
        assert register_user_response.message == (
            "Пользователь с таким email уже зарегистрирован"
        ), "Сообщение об ошибке не совпадает с ожидаемым"

        # assert db_helper.user_count_by_email(email) == 1
        if db_helper.user_count_by_email(email) != 1:
            raise AssertionError(
                f"Пользователь {email} должен быть зарегистрирован в БД, "
                "но количество пользователей с таким email должно быть равно 1"
            )

    @pytest.mark.smoke
    @pytest.mark.negative
    @allure.story(
        "Негативный тест на регистрацию пользователя с невалидными полями")
    @pytest.mark.parametrize(
        "email, full_name, password, password_repeat",
        REGISTER_INVALID_FIELDS_CASES,
        ids=REGISTER_INVALID_FIELDS_IDS,
    )
    def test_register_user_with_invalid_fields(
            self,
            email: str,
            full_name: str,
            password: str,
            password_repeat: str,
            api_manager,
            db_helper: DBHelper,
            expected_status: HTTPStatus = HTTPStatus.BAD_REQUEST
    ):
        register_data = {
            "email": email,
            "fullName": full_name,
            "password": password,
            "passwordRepeat": password_repeat
        }
        api_manager.auth_api.register_user(
            user_data=register_data,
            expected_status=expected_status,
            response_model=RegisterUserBadRequestResponse,
            attach_error_messages=True,
        )
        # assert not db_helper.user_exists_by_email(email)
        if db_helper.user_exists_by_email(email):
            raise AssertionError(
                f"После неуспешной регистрации пользователь {email} "
                "не должен появиться в БД"
            )

    @pytest.mark.smoke
    @pytest.mark.negative
    @allure.story(
        "Негативный тест на авторизацию еще не существующего пользователя")
    def test_login_unregistered_user(
            self,
            test_user: RegisterUserRequest,
            api_manager: ApiManager,
            db_helper: DBHelper,
            expected_status: HTTPStatus = HTTPStatus.UNAUTHORIZED):
        if db_helper.user_exists_by_email(test_user.email):
            raise AssertionError(
                f"Пользователь {test_user.email} уже существует в БД, "
                "ожидался незарегистрированный пользователь"
            )
        login_data = {"email": test_user.email, "password": test_user.password}

        response = api_manager.auth_api.login_user(
            login_data=login_data, expected_status=expected_status)
        login_user_response = LoginUserUnauthorizedResponse.model_validate(
            response.json())

        assert login_user_response.message == (
            "Неверный логин или пароль"
        ), "Сообщение об ошибке не совпадает с ожидаемым"
        if db_helper.user_exists_by_email(test_user.email):
            raise AssertionError(
                f"После неуспешного логина пользователь {test_user.email} "
                "не должен появиться в БД"
            )

    @pytest.mark.smoke
    @pytest.mark.negative
    @allure.story(
        "Негативный тест на авторизацию пользователя с пустыми полями")
    @pytest.mark.parametrize(
        "email, password",
        LOGIN_EMPTY_FIELDS_CASES,
        ids=LOGIN_EMPTY_FIELDS_IDS,
    )
    def test_login_user_with_empty_fields(
            self,
            email,
            password,
            api_manager,
            expected_status: HTTPStatus = HTTPStatus.UNAUTHORIZED,
    ):
        login_data = {"email": email, "password": password}

        response = api_manager.auth_api.login_user(
            login_data=login_data, expected_status=expected_status)
        login_user_response = LoginUserUnauthorizedResponse.model_validate(
            response.json())

        assert login_user_response.message == (
            "Неверный логин или пароль"
        ), "Сообщение об ошибке не совпадает с ожидаемым"
