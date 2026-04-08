# from http import HTTPStatus

# import allure

# from clients.api_manager import ApiManager

# @allure.feature("Негативные тесты для эндпоинта Пользователь Auth API")
# class TestUserAPINegative:
#     @allure.story("Тест на получение информации о пользователе по ID для обычного пользователя")
#     def test_get_user_by_id_common_user(self, common_user):
#         common_user.api.user_api.get_user(common_user.email, expected_status=HTTPStatus.FORBIDDEN)