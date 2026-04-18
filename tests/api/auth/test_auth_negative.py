from http import HTTPStatus

import allure

from clients.api_manager import ApiManager


@allure.feature("Негативные тесты для auth API")
class TestAuthAPINegative:
    @allure.story("Негативный тест на регистрацию пользователя с пустым полем пароля")
    def test_register_user_with_empty_password(self, api_manager: ApiManager, new_user: dict):
        new_user["password"] = ""
        new_user["passwordRepeat"] = ""

        api_manager.auth_api.register_user(new_user, expected_status=HTTPStatus.BAD_REQUEST)

    @allure.story("Негативный тест на регистрацию пользователя с пустым полем email")
    def test_register_user_with_empty_email(self, api_manager: ApiManager, new_user: dict):
        new_user["email"] = ""

        api_manager.auth_api.register_user(new_user, expected_status=HTTPStatus.BAD_REQUEST)

    @allure.story("Негативный тест на регистрацию пользователя с email без символа @")
    def test_register_user_with_email_at_less(self, api_manager: ApiManager, new_user: dict):
        new_user["email"] = "example.come"

        api_manager.auth_api.register_user(new_user, expected_status=HTTPStatus.BAD_REQUEST)

    @allure.story("Негативный тест на регистрацию уже существующего пользователя")
    def test_register_already_exist_user(self, api_manager: ApiManager, new_user: dict, users_to_cleanup: list):
        first_response = api_manager.auth_api.register_user(new_user, expected_status=HTTPStatus.CREATED)
        first_data = first_response.json()
        created_id = first_data.get("id")
        assert created_id is not None, "В ответе register отсутствует поле id"

        api_manager.auth_api.register_user(new_user, expected_status=HTTPStatus.CONFLICT)
        users_to_cleanup.append(created_id)

    @allure.story("Негативный тест на авторизацию еще не существующего пользователя")
    def test_login_unregistered_user(self, api_manager: ApiManager, new_user: dict):
        unregistered_user = {
            "email": new_user["email"],
            "password": new_user["password"]
        }

        api_manager.auth_api.login_user(unregistered_user, expected_status=HTTPStatus.UNAUTHORIZED)

    @allure.story("Негативный тест на авторизацию пользователя с пустыми полями email и password")
    def test_login_user_with_empty_data(self, api_manager: ApiManager, new_user: dict):
        new_user["email"] = ""
        new_user["password"] = ""

        api_manager.auth_api.login_user(new_user, expected_status=HTTPStatus.UNAUTHORIZED)
