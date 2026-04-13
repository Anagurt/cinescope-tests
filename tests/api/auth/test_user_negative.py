from http import HTTPStatus

import allure
import pytest

from models.base_model_user import UserForbiddenResponse, UserNotFoundResponse

from entities.user import User
from db_requester.db_helpers import DBHelper

@allure.feature("Негативные тесты для эндпоинта User API")
class TestUserAPINegative:

    @pytest.mark.smoke
    @pytest.mark.negative
    @allure.story(
        "Тест на получение информации о пользователе по ID под обычным пользователем"
    )
    def test_get_user_by_id_common_user(
            self,
            common_user: User,
            db_helper: DBHelper,
            expected_status: HTTPStatus = HTTPStatus.FORBIDDEN):
        assert db_helper.user_exists_by_email(common_user.email)
        response = common_user.api.user_api.get_user_info(
            user_id=common_user.id, expected_status=expected_status)
        forbidden_response = UserForbiddenResponse.model_validate(
            response.json())
        assert forbidden_response.message == "Forbidden resource"

    @pytest.mark.smoke
    @pytest.mark.negative
    @pytest.mark.xfail(reason="API возвращает 200 вместо 404")
    @allure.story(
        "Тест на получение информации о несуществующем пользователе под супер-админом"
    )
    @pytest.mark.parametrize(
        "user_locator, expected_status",
        [("non_existent_id", HTTPStatus.NOT_FOUND),
         ("non_existent_email", HTTPStatus.NOT_FOUND)],
        ids=[
            "Получение информации по ID",
            "Получение информации по Email"
        ])
    def test_get_user_by_locator(self, super_admin, user_locator,
                                 expected_status):
        response = super_admin.api.user_api.get_user_info(
            user_id=user_locator, expected_status=expected_status)
        not_found_response = UserNotFoundResponse.model_validate(
            response.json())
        assert not_found_response.message == "Not Found"

    @pytest.mark.smoke
    @pytest.mark.negative
    @allure.story("Тест на удаление пользователя под обычным пользователем")
    def test_delete_user_common_user(
            self,
            regular_user: User,
            common_user: User,
            db_helper: DBHelper,
            expected_status: HTTPStatus = HTTPStatus.FORBIDDEN):
        assert db_helper.user_exists_by_email(common_user.email)
        response = regular_user.api.user_api.delete_user(
            common_user.id, expected_status=expected_status)
        forbidden_response = UserForbiddenResponse.model_validate(
            response.json())
        assert forbidden_response.message == "Forbidden"
        assert db_helper.user_exists_by_email(common_user.email)

    @pytest.mark.smoke
    @pytest.mark.negative
    @allure.story(
        "Тест на удаление несуществующего пользователя под супер-админом")
    def test_delete_non_existent_user(
            self,
            super_admin,
            db_helper: DBHelper,
            expected_status: HTTPStatus = HTTPStatus.NOT_FOUND):
        assert db_helper.get_user_by_id("00000000-0000-0000-0000-000000000000") is None
        response = super_admin.api.user_api.delete_user(
            "00000000-0000-0000-0000-000000000000",
            expected_status=expected_status)
        not_found_response = UserNotFoundResponse.model_validate(
            response.json())
        assert not_found_response.message == "Not Found"
