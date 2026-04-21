from http import HTTPStatus

import allure
import pytest

from models.base_model_user import UserInfoResponse
from models.base_models_auth import RegisterUserRequest
from resources.user_creds import RegularUserCreds

from entities.user import User
from db_requester.db_helpers import DBHelper
from tests.constants.auth_cases import (
    REGULAR_USER_LOCATOR_CASES,
    REGULAR_USER_LOCATOR_IDS,
)


@allure.feature("Позитивные тесты для эндпоинта User API")
class TestUserAPIPositive:

    @pytest.mark.smoke
    @pytest.mark.flaky(reruns=2, reruns_delay=1)
    @allure.story("Тест на создание пользователя под супер-админом")
    def test_create_user(self, super_admin: User,
                         creation_user_data: RegisterUserRequest,
                         users_to_cleanup: list, db_helper: DBHelper):
        # assert not db_helper.user_exists_by_email(creation_user_data.email)
        if db_helper.user_exists_by_email(creation_user_data.email):
            raise AssertionError(
                f"Пользователь {creation_user_data.email} уже существует в БД, "
                "ожидался незарегистрированный пользователь"
            )
        response = super_admin.api.user_api.create_user(
            user_data=creation_user_data.model_dump(mode="json"))
        create_user_response = UserInfoResponse.model_validate(response.json())
        assert (
            create_user_response.email == creation_user_data.email
        ), "Email не совпадает"
        # assert db_helper.user_exists_by_email(creation_user_data.email)
        if not db_helper.user_exists_by_email(creation_user_data.email):
            raise AssertionError(
                f"Пользователь {creation_user_data.email} не существует в БД, "
                "ожидалось, что пользователь будет создан в БД"
            )
        users_to_cleanup.append(create_user_response.id)

    @pytest.mark.smoke
    @allure.story(
        "Тест на получение информации о пользователе по ID или Email под супер-админом"
    )
    @pytest.mark.parametrize(
        "user_locator",
        REGULAR_USER_LOCATOR_CASES,
        ids=REGULAR_USER_LOCATOR_IDS,
    )
    def test_get_user_by_locator(self, super_admin, user_locator,
                                 expected_status: HTTPStatus = HTTPStatus.OK):
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
                         super_admin: User,
                         common_user: User,
                         db_helper: DBHelper,
                         expected_status: HTTPStatus = HTTPStatus.OK):
        assert db_helper.user_exists_by_email(common_user.email)
        response = super_admin.api.user_api.delete_user(
            common_user.id, expected_status=expected_status)

        delete_response = UserInfoResponse.model_validate(response.json())
        assert delete_response.id == common_user.id
        assert not db_helper.user_exists_by_email(common_user.email)

    @pytest.mark.smoke
    @allure.story("Тест на удаление пользователя с пустым телом ответа")
    def test_delete_user_empty_body(
            self,
            super_admin: User,
            common_user: User,
            db_helper: DBHelper,
            expected_status: HTTPStatus = HTTPStatus.OK):
        # assert db_helper.user_exists_by_email(common_user.email)
        if not db_helper.user_exists_by_email(common_user.email):
            raise AssertionError(
                f"Пользователь {common_user.email} не существует в БД"
            )
        response = super_admin.api.user_api.delete_user(
            common_user.id, expected_status=expected_status)

        assert response.text.strip(
        ) == "", "Ожидалось пустое тело ответа после удаления"
        # assert not db_helper.user_exists_by_email(common_user.email)
        if db_helper.user_exists_by_email(common_user.email):
            raise AssertionError(
                f"Пользователь {common_user.email} существует в БД, "
                "ожидалось удаление из БД только что созданного пользователя"
            )
