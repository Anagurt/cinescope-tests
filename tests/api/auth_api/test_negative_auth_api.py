from clients.api_manager import ApiManager
from http import HTTPStatus


class TestAuthAPINegative:
    def test_register_user_with_empty_password(self, api_manager: ApiManager, empty_password_user: dict):
        """
        Негативный тест на регистрацию пользователя с пустым полем пароля.
        """
        api_manager.auth_api.register_user(empty_password_user, expected_status=HTTPStatus.BAD_REQUEST)

    def test_register_user_with_empty_email(self, api_manager: ApiManager, empty_email_user: dict):
        """
        Негативный тест на регистрацию пользователя с пустым полем email.
        """
        api_manager.auth_api.register_user(empty_email_user, expected_status=HTTPStatus.BAD_REQUEST)

    def test_register_user_with_email_at_less(self, api_manager: ApiManager, user_with_email_at_less: dict):
        """
        Негативный тест на регистрацию пользователя с email без символа @.
        """
        api_manager.auth_api.register_user(user_with_email_at_less, expected_status=HTTPStatus.BAD_REQUEST)

    def test_register_already_exist_user(self, api_manager: ApiManager, new_user: dict, users_to_cleanup: list):
        """
        Негативный тест на регистрацию уже существующего пользователя.
        """
        first_response = api_manager.auth_api.register_user(new_user, expected_status=HTTPStatus.CREATED)
        created_id = first_response.json()["id"]
        api_manager.auth_api.register_user(new_user, expected_status=HTTPStatus.CONFLICT)
        users_to_cleanup.append(created_id)

    def test_login_unregistered_user(self, api_manager: ApiManager, new_user: dict):
        """
        Негативный тест на авторизацию еще не существующего пользователя.
        """
        unregistered_user = {
            "email": new_user["email"],
            "password": new_user["password"]
        }
        api_manager.auth_api.login_user(unregistered_user, expected_status=HTTPStatus.UNAUTHORIZED)

    def test_login_user_with_empty_data(self, api_manager: ApiManager, empty_data_user: dict):
        """
        Негативный тест на авторизацию пользователя с пустыми полями email и password.
        """
        api_manager.auth_api.login_user(empty_data_user, expected_status=HTTPStatus.UNAUTHORIZED)
