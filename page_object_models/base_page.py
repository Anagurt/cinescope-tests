from playwright.sync_api import Page
import allure

from page_object_models.page_action import PageAction


class BasePage(PageAction):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "/"
        # Локаторы элементов
        self.home_button = page.get_by_role("link", name="Cinescope")
        self.all_movies_button = page.get_by_role("link", name="Все фильмы")
        # Не авторизованное состояние
        self.login_button = page.get_by_role("link", name="Войти")
        # Авторизованное состояние
        self.profile_icon = page.get_by_role("link", name="Профиль").locator("xpath=preceding-sibling::div[1]")
        self.profile_button = page.get_by_role("link", name="Профиль")
        # Страница профиля
        self.logout_button = page.get_by_role("button", name="Выход")
        # Страница профиля админа
        self.admin_panel_button = page.get_by_role("link", name="Админ панель")

    
    @allure.step("Переход на главную страницу, из шапки сайта")
    def go_to_home_page(self):
        self.click_on_element(self.home_button)
        self.wait_for_redirect_to_url("/")

    @allure.step("Переход на страницу 'Все фильмы, из шапки сайта'")
    def go_to_all_movies_page(self):
        self.click_on_element(self.all_movies_button)
        self.wait_for_redirect_to_url("/movies")

    @allure.step("Переход на страницу логина, из шапки сайта")
    def go_to_login_page(self):
        self.click_on_element(self.login_button)
        self.wait_for_redirect_to_url("/login")

    @allure.step("Переход на страницу профиля, из шапки сайта")
    def go_to_profile_page(self):
        self.click_on_element(self.profile_button)
        self.wait_for_redirect_to_url("/profile")

    @allure.step("Переход на страницу выхода, из шапки сайта")
    def go_to_logout_page(self):
        self.click_on_element(self.logout_button)
        self.wait_for_redirect_to_url(f"{self.url}logout") # TODO: добавить logout url

    @allure.step("Переход на страницу админ панели, из шапки сайта")
    def go_to_admin_panel_page(self):
        self.click_on_element(self.admin_panel_button)
        self.wait_for_redirect_to_url("/admin") # TODO: добавить admin panel url