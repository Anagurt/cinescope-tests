from http import HTTPStatus

import allure
import pytest

from clients.api_manager import ApiManager
from models.base_models_auth import (
    LoginResponse,
    LoginUserRequest,
    RegisterUserResponse,
)
from resources.user_creds import RegularUserCreds, SuperAdminCreds


@allure.feature("Позитивные тесты для auth API")
class TestAuthAPIPositive:

    @pytest.mark.smoke
    @allure.story("Тест на регистрацию пользователя")
    def test_register_user(self, api_manager: ApiManager, test_user,
                           users_to_cleanup: list):
        response = api_manager.auth_api.register_user(
            user_data=test_user.model_dump(mode="json"))
        register_user_response = RegisterUserResponse.model_validate(
            response.json())
        assert register_user_response.email == test_user.email, "Email не совпадает"
        users_to_cleanup.append(register_user_response.id)

    @pytest.mark.smoke
    @allure.story("Тест на авторизацию пользователя")
    @pytest.mark.parametrize(
        "email, password, expected_status",
        [(f"{SuperAdminCreds.USERNAME}", f"{SuperAdminCreds.PASSWORD}",
          HTTPStatus.OK),
         (f"{RegularUserCreds.USERNAME}", f"{RegularUserCreds.PASSWORD}",
          HTTPStatus.OK)],
        ids=["Авторизация супер-админа", "Авторизация пользователя"])
    def test_login_user(self, api_manager: ApiManager, email, password,
                        expected_status: HTTPStatus):
        login_payload = LoginUserRequest(email=email, password=password)
        login_data = login_payload.model_dump(mode="json")

        response = api_manager.auth_api.login_user(
            login_data=login_data, expected_status=expected_status)
        body = LoginResponse.model_validate(response.json())
        assert body.user.email == email
