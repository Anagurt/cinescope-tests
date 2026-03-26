from clients.api_manager import ApiManager


class TestAuthAPI:
    def test_register_user(self, api_manager: ApiManager, new_user):
        """
        Тест на регистрацию пользователя.
        """
        response = api_manager.auth_api.register_user(new_user)
        response_data = response.json()
        # Проверки
        assert response_data["email"] == new_user["email"], "Email не совпадает"
        assert "id" in response_data, "ID пользователя отсутствует в ответе"
        assert "roles" in response_data, "Роли пользователя отсутствуют в ответе"
        assert "USER" in response_data["roles"], "Роль USER должна быть у пользователя"

        # Удаляем пользователя после регистрации
        user_id = response_data["id"]
        login_data = {
            "email": new_user["email"],
            "password": new_user["password"],
        }
        api_manager.auth_api.login_user(login_data)
        api_manager.auth_api.authenticate((new_user["email"], new_user["password"]))
        api_manager.user_api.delete_user(user_id)


    def test_login_user(self, api_manager: ApiManager, registered_user):
        """
        Тест на регистрацию и авторизацию пользователя.
        """
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
        response = api_manager.auth_api.login_user(login_data)
        response_data = response.json()
        user_id = response_data["user"]["id"]
        # Проверки
        assert "accessToken" in response_data, "Токен доступа отсутствует в ответе"
        assert response_data["user"]["email"] == registered_user["email"], "Email не совпадает"

        # Удаляем пользователя после авторизации
        api_manager.auth_api.authenticate((registered_user["email"], registered_user["password"]))
        api_manager.user_api.delete_user(user_id)

    def test_get_user_info(self, api_manager: ApiManager, registered_user, new_user):
        """
        Тест на получение информации о пользователе под авторизованным пользователем.
        """
        api_manager.auth_api.authenticate_super_admin()

        response = api_manager.auth_api.register_user(new_user)
        user_id = response.json()["id"]

        response = api_manager.user_api.get_user_info(user_id)
        response_data = response.json()
        # Проверки
        assert "id" in response_data, "ID пользователя отсутствует в ответе"
        assert "email" in response_data, "Email не совпадает"
        assert "fullName" in response_data, "Имя не совпадает"
        assert "roles" in response_data, "Роли пользователя не совпадают"
        assert "USER" in response_data["roles"], "Роль USER должна быть у пользователя"

        # Удаляем пользователя после авторизации
        api_manager.user_api.delete_user(user_id)



    def test_delete_user(self, api_manager: ApiManager, registered_user, new_user):
        """
        Тест на удаление пользователя.
        """
        api_manager.auth_api.authenticate_super_admin()
        response = api_manager.auth_api.register_user(new_user)
        user_id = response.json()["id"]

        # Удаляем пользователя после получения информации о нем
        response = api_manager.user_api.delete_user(user_id)
        assert response.status_code == 200, "Ошибка при удалении пользователя"
        

# Негативные проверки

    def test_register_user_with_empty_password(self, api_manager: ApiManager, empty_password_user):
        """
        Негативный тест на регистрацию пользователя с пустым полем пароля.
        """
        response = api_manager.auth_api.register_user(empty_password_user, expected_status=400)


    def test_register_user_with_empty_email(self, api_manager: ApiManager, empty_email_user):
        """
        Негативный тест на регистрацию пользователя с пустым полем email.
        """
        response = api_manager.auth_api.register_user(empty_email_user, expected_status=400)


    def test_register_user_with_email_at_less(self, api_manager: ApiManager, user_with_email_at_less):
        """
        Негативный тест на регистрацию пользователя с email без символа @.
        """
        response = api_manager.auth_api.register_user(user_with_email_at_less, expected_status=400)


    def test_register_already_exist_user(self, api_manager: ApiManager, registered_user):
        """
        Негативный тест на регистрацию уже существующего пользователя.
        """
        response = api_manager.auth_api.register_user(registered_user)
        response = api_manager.auth_api.register_user(registered_user, expected_status=409)


    def test_login_unregistered_user(self, api_manager: ApiManager, new_user):
        """
        Негативный тест на авторизацию еще не существующего пользователя.
        """
        unregistered_user = {
            "email": new_user["email"],
            "password": new_user["password"]
        }
        response = api_manager.auth_api.login_user(unregistered_user, expected_status=401)


    def test_login_user_with_empty_data(self, api_manager: ApiManager, empty_data_user):
        """
        Негативный тест на авторизацию пользователя с пустыми полями email и password.
        """
        response = api_manager.auth_api.login_user(empty_data_user, expected_status=401)
