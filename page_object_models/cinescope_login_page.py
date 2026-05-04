from playwright.sync_api import Page, expect
from page_object_models.cinescope_header import CinescopeHeader
import allure

class CinescopeLoginPage:
    def __init__(self, page: Page):
        self.header = CinescopeHeader(page)
        self.page = page
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

    @allure.step("Переход на страницу логина")
    def open(self):
        self.page.goto(self.url)
        
    @allure.step("Ввод email")
    def input_email(self, email: str):
        self.login_email_input.fill(email)

    @allure.step("Ввод пароля")
    def input_password(self, password: str):
        self.login_password_input.fill(password)

    @allure.step("Нажатие кнопки логина")
    def click_login_button(self):
        self.login_button.click()

    @allure.step("Заполнение формы логина и отправка")
    def login(self, email: str, password: str):
        self.input_email(email)
        self.input_password(password)
        self.click_login_button()
    
    @allure.step("Ожидание редиректа на домашнюю страницу")
    def wait_redirect_to_home_page(self):
        self.page.wait_for_url("https://dev-cinescope.coconutqa.ru/")
        assert self.page.url == "https://dev-cinescope.coconutqa.ru/", "Редирект на домашнюю старницу не произошел"

    @allure.step("Проверка всплывающего сообщения после редиректа")
    def check_alert_text(self):
        notification_locator = self.page.get_by_text("Вы вошли в аккаунт")
        notification_locator.wait_for(state="visible")
        assert notification_locator.is_visible(), "Уведомление не появилось"
        
        notification_locator.wait_for(state="hidden")
        assert notification_locator.is_visible() == False, "Уведомление исчезло"

    @allure.step("Проверка отображения элементов на странице логина")
    def check_login_page_elements(self):
        expect(self.login_title).to_be_visible()
        expect(self.login_email_title).to_be_visible()
        expect(self.login_email_placeholder).to_be_visible()
        expect(self.login_password_title).to_be_visible()
        expect(self.login_password_placeholder).to_be_visible()
        expect(self.login_button).to_be_visible()
        expect(self.login_to_register_button).to_be_visible()