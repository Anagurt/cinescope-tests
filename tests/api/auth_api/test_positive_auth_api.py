from http import HTTPStatus

import allure

from clients.api_manager import ApiManager

@allure.feature("Positive tests for auth API")
class TestAuthAPIPositive:
    @allure.story("Тест на регистрацию пользователя")
    def test_register_user(self, api_manager: ApiManager, new_user: dict, users_to_cleanup: list):
        response = api_manager.auth_api.register_user(new_user)
        response_data = response.json()
        user_id = response_data.get("id")
        assert user_id is not None, "В ответе register отсутствует поле ID"

        expected_keys = {"id", "email", "fullName", "roles", "verified", "createdAt", "banned"}
        assert expected_keys.issubset(response_data.keys()), "Не все ключи присутствуют в ответе"


        assert response_data["email"] == new_user["email"], "Email не совпадает"
        assert response_data["fullName"] == new_user["fullName"], "Full Name не совпадает"

        users_to_cleanup.append(user_id)

    @allure.story("Тест на авторизацию пользователя")
    def test_login_user(self, api_manager: ApiManager, created_user_and_cleanup: dict):
        login_data = {
            "email": created_user_and_cleanup["email"],
            "password": created_user_and_cleanup["password"]
        }

        response = api_manager.auth_api.login_user(login_data)
        response_data = response.json()

        expected_keys = {"user", "accessToken", "refreshToken", "expiresIn"}
        assert expected_keys.issubset(response_data.keys()), "Не все ключи присутствуют в ответе"

        user_data = response_data.get("user")
        assert user_data is not None, "В ответе login отсутствует объект user"

        login_user_keys = {"id", "email", "fullName", "roles"}
        assert login_user_keys.issubset(user_data.keys()), "В user ответа login не все ожидаемые поля"

        access_token = response_data.get("accessToken")
        refresh_token = response_data.get("refreshToken")
        assert access_token, "В ответе login отсутствует или пустой accessToken"
        assert refresh_token, "В ответе login отсутствует или пустой refreshToken"
        assert response_data.get("expiresIn") is not None, "В ответе login отсутствует expiresIn"

        assert user_data.get("email") == created_user_and_cleanup["email"], "Email не совпадает"
    
    @allure.story("Тест на получение информации о пользователе")
    def test_get_user_info(self, api_manager: ApiManager, created_user_and_cleanup: dict, authorized_super_admin: ApiManager):
        response = authorized_super_admin.user_api.get_user_info(created_user_and_cleanup["id"])
        response_data = response.json()

        expected_keys = {"id", "email", "fullName", "roles", "verified", "createdAt", "banned"}
        assert expected_keys.issubset(response_data.keys()), "Не все ключи присутствуют в ответе"

        assert response_data.get("id") == created_user_and_cleanup["id"], "ID пользователя не совпадает"
        roles = response_data.get("roles")
        assert roles is not None, "В ответе get_user_info отсутствует поле roles"
        assert "USER" in roles, "Роль USER должна быть у пользователя"

    @allure.story("Тест на удаление пользователя")
    def test_delete_user(self, api_manager: ApiManager, created_user_and_cleanup: dict, authorized_super_admin: ApiManager):
        response = authorized_super_admin.user_api.delete_user(created_user_and_cleanup["id"])

        assert response.text.strip() == "", "Ожидалось пустое тело ответа после удаления"
