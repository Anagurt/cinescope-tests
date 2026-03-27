from clients.api_manager import ApiManager
from http import HTTPStatus


class TestAuthAPIPositive:
    def test_register_user(self, api_manager: ApiManager, new_user: dict, users_to_cleanup: list):
        """
        Тест на регистрацию пользователя.
        """
        response = api_manager.auth_api.register_user(new_user)
        response_data = response.json()
        user_id = response_data["id"]
        assert response_data["email"] == new_user["email"], "Email не совпадает"
        expected_keys = {"id", "email", "fullName", "roles", "verified", "createdAt", "banned"}
        assert expected_keys.issubset(response_data.keys()), "Не все ключи присутствуют в ответе"
        assert "USER" in response_data["roles"], "Роль USER должна быть у пользователя"
        users_to_cleanup.append(user_id)


    def test_login_user(self, api_manager: ApiManager, created_user_and_cleanup: dict):
        """
        Тест на авторизацию пользователя.
        """
        login_data = {
            "email": created_user_and_cleanup["email"],
            "password": created_user_and_cleanup["password"]
        }
        response = api_manager.auth_api.login_user(login_data)
        response_data = response.json()
        assert "accessToken" in response_data, "Токен доступа отсутствует в ответе"
        assert response_data["user"]["email"] == created_user_and_cleanup["email"], "Email не совпадает"


    def test_get_user_info(self, api_manager: ApiManager, created_user_and_cleanup: dict, authorized_super_admin: ApiManager):
        """
        Тест на получение информации о пользователе.
        """
        response = authorized_super_admin.user_api.get_user_info(created_user_and_cleanup["id"])
        response_data = response.json()
        assert response_data["id"] == created_user_and_cleanup["id"], "ID пользователя не совпадает"
        expected_keys = {"id", "email", "fullName", "roles", "verified", "createdAt", "banned"}
        assert expected_keys.issubset(response_data.keys()), "Не все ключи присутствуют в ответе"
        assert "USER" in response_data["roles"], "Роль USER должна быть у пользователя"


    def test_delete_user(self, api_manager: ApiManager, created_user_and_cleanup: dict, authorized_super_admin: ApiManager):
        """
        Тест на удаление пользователя.
        """
        response = authorized_super_admin.user_api.delete_user(created_user_and_cleanup["id"], expected_status=HTTPStatus.OK)
        assert response.text.strip() == "", "Ожидалось пустое тело ответа после удаления"
 
