import allure
from playwright.sync_api import Page, expect
from page_object_models.base_page import BasePage

class CinescopeRegisterPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "/register"
        # Локаторы элементов
        self.register_title = page.get_by_role('heading', name="Регистрация")
        # ФИО
        self.register_name_title = page.get_by_text("ФИО")
        self.register_name_input = page.get_by_role("textbox", name="Имя Фамилия Отчество", exact=True)
        self.register_name_placeholder = page.get_by_placeholder("Имя Фамилия Отчество")
        # self.register_name_text_error = page.get_by_text("Неверная почта") - Баг на сайте, ошибка в тексте ошибки
        # Email
        self.register_email_title = page.get_by_text("Email")
        self.register_email_input = page.get_by_role("textbox", name="Email", exact=True)
        self.register_email_placeholder = page.get_by_placeholder("Email")
        self.register_email_text_error = page.get_by_text("Неверная почта")
        # Пароль
        self.register_password_title = page.get_by_text("Пароль", exact=True)
        self.register_password_input = page.get_by_role("textbox", name="Пароль", exact=True)
        self.register_password_placeholder = page.get_by_placeholder("Пароль", exact=True)
        self.register_password_text_error = page.get_by_text("Пароль не соответствует требованиям").first
        self.register_too_short_password_text_error = page.get_by_text("Пароль должен содержать не менее 8 символов")
        self.register_too_long_password_text_error = page.get_by_text("Пароль должен содержать не более 32 символов")
        # Требования к паролю
        self.register_requirements_button = page.get_by_role("button", name="требованиям")
        self.register_requirements_text = page.get_by_text("Пароль должен соответствовать требованиям")
        self.password_requirements_tooltip = page.locator("[data-radix-popper-content-wrapper]").filter(has_text="Не менее 8 символов")
        # Повторите пароль
        self.register_password_repeat_title = page.get_by_text("Повторите пароль", exact=True)
        self.register_password_repeat_input = page.get_by_role("textbox", name="Повторите пароль", exact=True)
        self.register_password_repeat_placeholder = page.get_by_placeholder("Повторите пароль", exact=True)
        self.register_password_repeat_text_error = (
            page.locator("form")
            .filter(has_text="Повторите пароль")
            .get_by_text("Пароль не соответствует требованиям")
        )
        self.register_password_repeat_not_match_text_error = page.get_by_text("Введенные пароли не совпадают")
        # Кнопка регистрации
        self.register_button = page.get_by_role("button", name="Зарегистрироваться")
        self.register_to_login_button = page.locator("form").get_by_role("link", name="Войти")

    def open(self):
        self.open_url(self.url)

    def input_name(self, name: str):
        self.input_text_to_element(self.register_name_input, name, "ФИО")

    def input_email(self, email: str):
        self.input_text_to_element(self.register_email_input, email, "Email")

    def input_password(self, password: str):
        self.input_text_to_element(self.register_password_input, password, "Пароль")

    def input_password_repeat(self, password: str):
        self.input_text_to_element(self.register_password_repeat_input, password, "Повторный пароль")

    def click_register_button(self):
        self.click_on_element(self.register_button, "Кнопка регистрации")
    
    def click_login_button(self):
        self.click_on_element(self.register_to_login_button, "Ссылка на страницу логина")

    def hover_requirements_button(self):
        self.hover_on_element(self.register_requirements_button, "Требования к паролю")
        self.wait_for_element(self.password_requirements_tooltip, "visible", "Тултип требований к паролю")

    def register(self, name: str, email: str, password: str, password_repeat: str):
        self.input_name(name)
        self.input_email(email)
        self.input_password(password)
        self.input_password_repeat(password_repeat)
        self.click_register_button()

    def wait_redirect_to_login_page(self):
        self.wait_for_redirect_to_url("/login")

    def check_alert_text(self):
        self.check_pop_up_element_with_text("Подтвердите свою почту")

    def check_register_page_elements(self):
        self.wait_for_element(self.register_title, "visible", "Заголовок страницы регистрации")
        self.wait_for_element(self.register_name_title, "visible", "Заголовок поля ФИО")
        self.wait_for_element(self.register_name_placeholder, "visible", "Placeholder поля ФИО")
        self.wait_for_element(self.register_email_title, "visible", "Заголовок поля Email")
        self.wait_for_element(self.register_email_placeholder, "visible", "Placeholder поля Email")
        self.wait_for_element(self.register_password_title, "visible", "Заголовок поля Пароль")
        self.wait_for_element(self.register_password_placeholder, "visible", "Placeholder поля Пароль")
        self.wait_for_element(self.register_password_repeat_title, "visible", "Заголовок поля Повторите пароль")
        self.wait_for_element(self.register_password_repeat_placeholder, "visible", "Placeholder поля Повторите пароль")
        self.wait_for_element(self.register_button, "visible", "Кнопка регистрации")
        self.wait_for_element(self.register_requirements_button, "visible", "Требования к паролю")
        self.wait_for_element(self.register_to_login_button, "visible", "Ссылка на страницу логина")