import allure
import pytest
import time
from playwright.sync_api import sync_playwright
from resources.user_creds import RegularUserCreds



@allure.feature("Позитивные тесты для страницы логина")
class TestLoginPage:

    @pytest.mark.smoke
    @allure.story("Тест на логин пользователя")
    def test_login_user(self, login_page):
        login_page.open()
        login_page.check_login_page_elements()
        login_page.login(RegularUserCreds.USERNAME, RegularUserCreds.PASSWORD)
        login_page.wait_redirect_to_home_page()
        login_page.check_alert_text()
