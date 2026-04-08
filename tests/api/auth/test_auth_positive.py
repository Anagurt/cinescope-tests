import allure

from clients.api_manager import ApiManager
from models.base_models import RegisterUserResponse, LoginResponse, LoginUserRequest, UserInfoResponse

import pytest

from resources.user_creds import SuperAdminCreds, RegularUserCreds
from http import HTTPStatus

# @pytest.mark.parametrize("email, password, expected_status", [
#     (f"{SuperAdminCreds.USERNAME}", f"{SuperAdminCreds.PASSWORD}", (200, 201)),
#     ("test_login1@email.com", "asdqwe123Q!", 500),  # Сервис не может обработать логин по незареганному юзеру
#     ("", "password", 500),
# ], ids=["Admin login", "Invalid user", "Empty username"])
# def test_login(email, password, expected_status, api_manager):
#     login_data = {
#         "email": email,
#         "password": password
#     }
#     api_manager.auth_api.login_user(login_data=login_data, expected_status=expected_status)

# def test_register_user(self, api_manager: ApiManager, test_user):
#     response = api_manager.auth_api.register_user(user_data=test_user)
#     register_user_response = RegisterUserResponse(**response.json())
#     assert register_user_response.email == test_user.email, "Email не совпадает"
# # Откуда берется registration_user_data? Можно использовать фикстуру test_user?

@allure.feature("Позитивные тесты для auth API")
class TestAuthAPIPositive:
    @pytest.mark.smoke
    @allure.story("Тест на регистрацию пользователя")
    def test_register_user(self, api_manager: ApiManager, test_user, users_to_cleanup: list):
        response = api_manager.auth_api.register_user(user_data=test_user.model_dump(mode="json"))
        register_user_response = RegisterUserResponse.model_validate(response.json())
        assert register_user_response.email == test_user.email, "Email не совпадает"
        users_to_cleanup.append(register_user_response.id)


    @pytest.mark.smoke
    @allure.story("Тест на авторизацию пользователя")
    @pytest.mark.parametrize("email, password, expected_status", [
    (f"{SuperAdminCreds.USERNAME}", f"{SuperAdminCreds.PASSWORD}", HTTPStatus.OK),
    (f"{RegularUserCreds.USERNAME}", f"{RegularUserCreds.PASSWORD}", HTTPStatus.OK) 
    ], ids=["Авторизация супер-админа","Авторизация пользователя"])
    def test_login_user(self, api_manager: ApiManager, email, password, expected_status: HTTPStatus):
        login_payload = LoginUserRequest(email=email, password=password)
        login_data = login_payload.model_dump(mode="json")
        
        response = api_manager.auth_api.login_user(
            login_data=login_data,
            expected_status=expected_status
            )
        body = LoginResponse.model_validate(response.json())
        assert body.user.email == email
        

    @pytest.mark.smoke
    @allure.story("Тест на получение информации о пользователе")
    def test_get_user_info(self, super_admin, common_user, expected_status: HTTPStatus = HTTPStatus.OK):
        response = super_admin.api.user_api.get_user_info(common_user.id, expected_status=expected_status)

        user_info_response = UserInfoResponse.model_validate(response.json())
        assert user_info_response.id == common_user.id

    
    @pytest.mark.smoke
    @pytest.mark.xfail(reason="API: DELETE возвращает пустое тело, вместо полей согласно Swagger")
    @allure.story("Тест на удаление пользователя")
    def test_delete_user(self, super_admin, common_user, expected_status: HTTPStatus = HTTPStatus.OK):
        response = super_admin.api.user_api.delete_user(common_user.id, expected_status=expected_status)

        delete_response = UserInfoResponse.model_validate(response.json())
        assert delete_response.id == common_user.id
    
    @pytest.mark.smoke
    @allure.story("Тест на удаление пользователя с пустым телом ответа")
    def test_delete_user_empty_body(self, super_admin, common_user, expected_status: HTTPStatus = HTTPStatus.OK):
        response = super_admin.api.user_api.delete_user(common_user.id, expected_status=expected_status)

        assert response.text.strip() == "", "Ожидалось пустое тело ответа после удаления"

