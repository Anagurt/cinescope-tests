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
        if db_helper.user_exists_by_email(test_user.email):
            raise AssertionError(
                f"Пользователь {test_user.email} уже существует в БД, "
                "ожидался незарегистрированный пользователь"
            )
        response = api_manager.auth_api.register_user(
            user_data=test_user.model_dump(mode="json"), success_response_model=RegisterUserResponse)

        users_to_cleanup.append(response.validated_response.id)

        assert response.validated_response.email == test_user.email, "Email не совпадает"
        if not db_helper.user_exists_by_email(test_user.email):
            raise AssertionError(
                f"После успешной регистрации пользователь {test_user.email} "
                "должен появиться в БД"
            )

    @pytest.mark.smoke
    @allure.story("Тест на авторизацию пользователя")
    @pytest.mark.parametrize(
        "email, password",
        LOGIN_EXIST_USERS_CASES,
        ids=LOGIN_EXIST_USERS_IDS,
    )
    def test_login_user(
            self,
            api_manager: ApiManager,
            email: str,
            password: str,
            db_helper: DBHelper,
            expected_status: HTTPStatus = HTTPStatus.OK,
    ):
        login_payload = LoginUserRequest(email=email, password=password)
        login_data = login_payload.model_dump(mode="json")
        if not db_helper.user_exists_by_email(email):
            raise AssertionError(
                f"Пользователь {email} отсутствует в БД"
            )

        response = api_manager.auth_api.login_user(
            login_data=login_data, expected_status=expected_status, success_response_model=LoginResponse)

        assert response.validated_response.user.email == login_data["email"], "Email не совпадает"
