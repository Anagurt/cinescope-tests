import allure
import pytest
import time

@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы Register")
@pytest.mark.ui
class TestRegisterPage:

    @pytest.mark.smoke
    @allure.story("Тест на регистрацию пользователя")
    def test_register_user(self, register_page, test_user, cleanup_registered_user_after_test):
        register_page.open()
        register_page.check_register_page_elements()
        register_page.register(
                test_user.fullName,
                test_user.email,
                test_user.password,
                test_user.passwordRepeat,
            )
        register_page.wait_redirect_to_login_page()
        register_page.check_alert_text()