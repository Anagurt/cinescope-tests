from playwright.sync_api import Page
from page_object_models.base_page import BasePage

class CinescopeLoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "/login"
        # Локаторы элементов
        self.login_title = page.get_by_role("heading", name="Войти")
        # Email
        self.login_email_title = page.get_by_text("Email", exact=True)
        self.login_email_input = page.get_by_role("textbox", name="Email", exact=True)
        self.login_email_placeholder = page.get_by_placeholder("Email", exact=True)
        self.login_email_empty_error = page.locator("form").get_by_text("Поле email не может быть пустым", exact=True)
        # Пароль
        self.login_password_title = page.get_by_text("Пароль", exact=True)
        self.login_password_input = page.get_by_role("textbox", name="Пароль", exact=True)
        self.login_password_placeholder = page.get_by_placeholder("Пароль", exact=True)
        self.login_password_empty_error = page.locator("form").get_by_text("Поле пароль не может быть пустым", exact=True)
        # Кнопка логина
        self.login_button = page.locator('form').get_by_role("button", name="Войти")
        self.login_to_register_button = page.locator("form").get_by_role("link", name="Зарегистрироваться")
        # сообщение об ошибке при вводе некорректных данных
        self.login_text_error = page.get_by_text("Неверная почта или пароль")

    def open(self):
        self.open_url(self.url)

    def input_email(self, email: str):
        self.input_text_to_element(self.login_email_input, email, "Email")

    def input_password(self, password: str):
        self.input_text_to_element(self.login_password_input, password, "Пароль")

    def click_login_button(self):
        self.click_on_element(self.login_button, "Кнопка логина")

    def login(self, email: str, password: str):
        self.input_email(email)
        self.input_password(password)
        self.click_login_button()
    
    def wait_redirect_to_home_page(self):
        self.wait_for_redirect_to_url("/")

    def check_alert_text(self):
        self.check_pop_up_element_with_text("Вы вошли в аккаунт")

    def check_login_page_elements(self):
        self.wait_for_element(self.login_title, "visible", "Заголовок страницы логина")
        self.wait_for_element(self.login_email_title, "visible", "Заголовок поля Email")
        self.wait_for_element(self.login_email_placeholder, "visible", "Placeholder поля Email")
        self.wait_for_element(self.login_password_title, "visible", "Заголовок поля Пароль")
        self.wait_for_element(self.login_password_placeholder, "visible", "Placeholder поля Пароль")
        self.wait_for_element(self.login_button, "visible", "Кнопка логина")
        self.wait_for_element(self.login_to_register_button, "visible", "Ссылка на страницу регистрации")