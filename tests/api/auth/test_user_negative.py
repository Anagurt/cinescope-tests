from http import HTTPStatus

import allure
import pytest

from models.base_model_user import UserForbiddenResponse, UserNotFoundResponse

from entities.user import User
from db_requester.db_helpers import DBHelper
from constants import CommonConstants
from tests.constants.auth_cases import (
    INVALID_USER_LOCATOR_CASES,
    INVALID_USER_LOCATOR_IDS
)


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
        # assert db_helper.user_exists_by_email(common_user.email)
        if not db_helper.user_exists_by_email(common_user.email):
            raise AssertionError(
                f"Пользователь {common_user.email} не существует в БД"
            )
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
        "user_locator",
        INVALID_USER_LOCATOR_CASES,
        ids=INVALID_USER_LOCATOR_IDS,
    )
    def test_get_user_by_locator(self, super_admin, user_locator,
                                 expected_status: HTTPStatus = HTTPStatus.NOT_FOUND):
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
        # assert db_helper.user_exists_by_email(common_user.email)
        if not db_helper.user_exists_by_email(common_user.email):
            raise AssertionError(
                f"Пользователь {common_user.email} не существует в БД"
            )
        response = regular_user.api.user_api.delete_user(
            common_user.id, expected_status=expected_status)
        forbidden_response = UserForbiddenResponse.model_validate(
            response.json())
        assert forbidden_response.message == "Forbidden"
        # assert db_helper.user_exists_by_email(common_user.email)
        if not db_helper.user_exists_by_email(common_user.email):
            raise AssertionError(
                f"Пользователь {common_user.email} не существует в БД, "
                "ожидалось, что у пользователя нет права удалять пользователей"
            )

    @pytest.mark.smoke
    @pytest.mark.negative
    @allure.story(
        "Тест на удаление несуществующего пользователя под супер-админом")
    def test_delete_non_existent_user(
            self,
            super_admin,
            db_helper: DBHelper,
            expected_status: HTTPStatus = HTTPStatus.NOT_FOUND):
        # assert db_helper.get_user_by_id(
        #     CommonConstants.NON_EXISTENT_USER_ID) is None
        if db_helper.get_user_by_id(CommonConstants.NON_EXISTENT_USER_ID):
            raise AssertionError(
                f"Пользователь с ID {CommonConstants.NON_EXISTENT_USER_ID} существует в БД, "
                "ожидалось, что пользователь с таким ID не существует в БД"
            )    
        response = super_admin.api.user_api.delete_user(
            CommonConstants.NON_EXISTENT_USER_ID,
            expected_status=expected_status)
        not_found_response = UserNotFoundResponse.model_validate(
            response.json())
        assert not_found_response.message == "Not Found"
