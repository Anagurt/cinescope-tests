from playwright.sync_api import Page


class CinescopeHeader:
    def __init__(self, page: Page):
        self.page = page
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

    def click_home_button(self):
        self.home_button.click()
        self.page.wait_for_url("/")
        assert self.page.url == "/", "Редирект на главную страницу не произошел"

    def click_all_movies_button(self):
        self.all_movies_button.click()
        self.page.wait_for_url("/movies")
        assert self.page.url == "/movies", "Редирект на страницу всех фильмов не произошел"

    def click_login_button(self):
        self.login_button.click()

    def click_profile_button(self):
        self.profile_button.click()
        self.page.wait_for_url("/profile")
        assert self.page.url == "/profile", "Редирект на страницу профиля не произошел"
    
    def click_logout_button(self):
        self.logout_button.click()

    def click_admin_panel_button(self):
        self.admin_panel_button.click()