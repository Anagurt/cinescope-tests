from http import HTTPStatus

import allure
import pytest

from clients.api_manager import ApiManager
from models.base_models_auth import (
    LoginResponse,
    RegisterUserRequest,
    LoginUserRequest,
    RegisterUserResponse,
)

from db_requester.db_helpers import DBHelper
from tests.constants.auth_cases import (
    LOGIN_EXIST_USERS_CASES,
    LOGIN_EXIST_USERS_IDS
)


@allure.feature("Позитивные тесты для auth API")
class TestAuthAPIPositive:

    @pytest.mark.smoke
    @allure.story("Тест на регистрацию пользователя")
    def test_register_user(self, api_manager: ApiManager,
                           test_user: RegisterUserRequest,
                           users_to_cleanup: list, db_helper: DBHelper):
        assert not db_helper.user_exists_by_email(test_user.email)
        response = api_manager.auth_api.register_user(
            user_data=test_user.model_dump(mode="json"))
        register_user_response = RegisterUserResponse.model_validate(
            response.json())
        assert register_user_response.email == test_user.email, "Email не совпадает"
        users_to_cleanup.append(register_user_response.id)
        assert db_helper.user_exists_by_email(test_user.email)

    @pytest.mark.smoke
    @allure.story("Тест на авторизацию пользователя")
    @pytest.mark.parametrize(
        "email, password",
        LOGIN_EXIST_USERS_CASES,
        ids=LOGIN_EXIST_USERS_IDS,
    )
    def test_login_user(self, api_manager: ApiManager, email: str, password: str,
                        expected_status: HTTPStatus = HTTPStatus.OK):
        login_payload = LoginUserRequest(email=email, password=password)
        login_data = login_payload.model_dump(mode="json")

        response = api_manager.auth_api.login_user(
            login_data=login_data, expected_status=expected_status)
        body = LoginResponse.model_validate(response.json())
        assert body.user.email == email
