from http import HTTPStatus

import allure
import pytest

from models.base_models_auth import (
    LoginUserUnauthorizedResponse,
    RegisterUserBadRequestResponse,
    RegisterUserConflictResponse,
)
from resources.user_creds import RegularUserCreds, SuperAdminCreds


@allure.feature("Негативные тесты для auth API")
class TestAuthAPINegative:

    @pytest.mark.smoke
    @pytest.mark.negative
    @allure.story(
        "Негативный тест на регистрацию пользователя с пустыми полями")
    @pytest.mark.parametrize(
        "email, fullName, password, passwordRepeat, expected_status", [
            ("", "ФИО пользователя", "asdqwe123Q!", "asdqwe123Q!",
             HTTPStatus.BAD_REQUEST),
            ("test.register0@email.com", "ФИО пользователя", "", "asdqwe123Q!",
             HTTPStatus.BAD_REQUEST),
            ("test.register1@email.com", "", "asdqwe123Q!", "asdqwe123Q!",
             HTTPStatus.BAD_REQUEST),
            ("test.register2@email.com", "ФИО пользователя", "asdqwe123Q!", "",
             HTTPStatus.BAD_REQUEST),
        ],
        ids=[
            "Пустой email", "Пустой password", "Пустой fullName",
            "Пустой passwordRepeat"
        ])
    def test_register_user_with_empty_fields(self, email, fullName, password,
                                             passwordRepeat, expected_status,
                                             api_manager, request):
        register_data = {
            "email": email,
            "fullName": fullName,
            "password": password,
            "passwordRepeat": passwordRepeat
        }
        response = api_manager.auth_api.register_user(
            user_data=register_data, expected_status=expected_status)
        register_user_response = RegisterUserBadRequestResponse.model_validate(
            response.json())
        message_response = request.node.callspec.id
        text = f"{message_response}\n\n" + "\n".join(
            f'"{m}"' for m in register_user_response.message)
        allure.attach(text,
                      name="Сообщения об ошибках API",
                      attachment_type=allure.attachment_type.TEXT)

    @pytest.mark.smoke
    @pytest.mark.negative
    @allure.story(
        "Негативный тест на регистрацию уже существующего пользователя")
    @pytest.mark.parametrize(
        "email, fullName, password, passwordRepeat, expected_status",
        [(f"{SuperAdminCreds.USERNAME}", "ФИО пользователя",
          f"{SuperAdminCreds.PASSWORD}", f"{SuperAdminCreds.PASSWORD}",
          HTTPStatus.CONFLICT),
         (f"{RegularUserCreds.USERNAME}", "ФИО пользователя",
          f"{RegularUserCreds.PASSWORD}", f"{RegularUserCreds.PASSWORD}",
          HTTPStatus.CONFLICT)],
        ids=[
            "Регистрация уже существующего супер-админа",
            "Регистрация уже существующего пользователя"
        ])
    def test_register_already_exist_user(self, email, fullName, password,
                                         passwordRepeat, expected_status,
                                         api_manager):
        register_data = {
            "email": email,
            "fullName": fullName,
            "password": password,
            "passwordRepeat": passwordRepeat
        }
        response = api_manager.auth_api.register_user(
            user_data=register_data, expected_status=expected_status)
        register_user_response = RegisterUserConflictResponse.model_validate(
            response.json())
        assert register_user_response.message == "Пользователь с таким email уже зарегистрирован"

    @pytest.mark.smoke
    @pytest.mark.negative
    @allure.story(
        "Негативный тест на регистрацию пользователя с невалидными полями")
    @pytest.mark.parametrize(
        "email, fullName, password, passwordRepeat, expected_status",
        [("test.registeremail.com", "ФИО пользователя", "asdqwe123Q!",
          "asdqwe123Q!", HTTPStatus.BAD_REQUEST),
         ("test.register@emailcom", "ФИО пользователя", "asdqwe123Q!",
          "asdqwe123Q!", HTTPStatus.BAD_REQUEST),
         ("@email.com", "ФИО пользователя", "asdqwe123Q!", "asdqwe123Q!",
          HTTPStatus.BAD_REQUEST),
         ("test.register3@email.com", "ФИО пользователя", "Qwerty7", "Qwerty7",
          HTTPStatus.BAD_REQUEST),
         ("test.register4@email.com", "ФИО пользователя",
          "QwertyuiopasdfghjklzxcvbnmQwer33X",
          "QwertyuiopasdfghjklzxcvbnmQwer33X", HTTPStatus.BAD_REQUEST)],
        ids=[
            "email без символа @", "email без точки",
            "email без локальной части", "слишком короткий password",
            "слишком длинный password"
        ])
    def test_register_user_with_invalid_fields(self, email, fullName, password,
                                               passwordRepeat, expected_status,
                                               api_manager, request):
        register_data = {
            "email": email,
            "fullName": fullName,
            "password": password,
            "passwordRepeat": passwordRepeat
        }
        response = api_manager.auth_api.register_user(
            user_data=register_data, expected_status=expected_status)
        register_user_response = RegisterUserBadRequestResponse.model_validate(
            response.json())
        message_response = request.node.callspec.id
        text = f"{message_response}\n\n" + "\n".join(
            f'"{m}"' for m in register_user_response.message)
        allure.attach(text,
                      name="Сообщения об ошибках API",
                      attachment_type=allure.attachment_type.TEXT)

    @pytest.mark.smoke
    @pytest.mark.negative
    @allure.story(
        "Негативный тест на авторизацию еще не существующего пользователя")
    def test_login_unregistered_user(
            self,
            test_user,
            api_manager,
            expected_status: HTTPStatus = HTTPStatus.UNAUTHORIZED):
        login_data = {"email": test_user.email, "password": test_user.password}
        response = api_manager.auth_api.login_user(
            login_data=login_data, expected_status=expected_status)
        login_user_response = LoginUserUnauthorizedResponse.model_validate(
            response.json())
        assert login_user_response.message == "Неверный логин или пароль"

    @pytest.mark.smoke
    @pytest.mark.negative
    @allure.story(
        "Негативный тест на авторизацию пользователя с пустыми полями")
    @pytest.mark.parametrize(
        "email, password, expected_status",
        [("", f"{RegularUserCreds.PASSWORD}", HTTPStatus.UNAUTHORIZED),
         (f"{RegularUserCreds.USERNAME}", "", HTTPStatus.UNAUTHORIZED)],
        ids=["Пустой email", "Пустой password"])
    def test_login_user_with_empty_fields(self, email, password,
                                          expected_status, api_manager):
        login_data = {"email": email, "password": password}
        response = api_manager.auth_api.login_user(
            login_data=login_data, expected_status=expected_status)
        login_user_response = LoginUserUnauthorizedResponse.model_validate(
            response.json())
        assert login_user_response.message == "Неверный логин или пароль"
