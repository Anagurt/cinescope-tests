from http import HTTPStatus

import allure
import pytest

from models.base_model_user import UserInfoResponse
from resources.user_creds import RegularUserCreds


@allure.feature("Позитивные тесты для эндпоинта User API")
class TestUserAPIPositive:

    @pytest.mark.smoke
    @allure.story("Тест на создание пользователя под супер-админом")
    def test_create_user(self, super_admin, creation_user_data,
                         users_to_cleanup):
        response = super_admin.api.user_api.create_user(
            user_data=creation_user_data.model_dump(mode="json"))
        create_user_response = UserInfoResponse.model_validate(response.json())
        assert create_user_response.email == creation_user_data.email, "Email не совпадает"
        users_to_cleanup.append(create_user_response.id)

    @pytest.mark.smoke
    @allure.story(
        "Тест на получение информации о пользователе по ID или Email под супер-админом"
    )
    @pytest.mark.parametrize("user_locator, expected_status",
                             [(f"{RegularUserCreds.ID}", HTTPStatus.OK),
                              (f"{RegularUserCreds.USERNAME}", HTTPStatus.OK)],
                             ids=[
                                 "Получение информации о пользователе по ID",
                                 "Получение информации о пользователе по Email"
                             ])
    def test_get_user_by_locator(self, super_admin, user_locator,
                                 expected_status):
        response_by_locator = super_admin.api.user_api.get_user_info(
            user_id=user_locator, expected_status=expected_status)
        by_locator = UserInfoResponse.model_validate(
            response_by_locator.json())
        assert by_locator.id == RegularUserCreds.ID
        assert by_locator.email == RegularUserCreds.USERNAME, "Email не совпадает"

    @pytest.mark.smoke
    @pytest.mark.xfail(
        reason="API возвращает пустое тело, вместо полей согласно Swagger")
    @allure.story("Тест на удаление пользователя")
    def test_delete_user(self,
                         super_admin,
                         common_user,
                         expected_status: HTTPStatus = HTTPStatus.OK):
        response = super_admin.api.user_api.delete_user(
            common_user.id, expected_status=expected_status)

        delete_response = UserInfoResponse.model_validate(response.json())
        assert delete_response.id == common_user.id

    @pytest.mark.smoke
    @allure.story("Тест на удаление пользователя с пустым телом ответа")
    def test_delete_user_empty_body(
            self,
            super_admin,
            common_user,
            expected_status: HTTPStatus = HTTPStatus.OK):
        response = super_admin.api.user_api.delete_user(
            common_user.id, expected_status=expected_status)

        assert response.text.strip(
        ) == "", "Ожидалось пустое тело ответа после удаления"
