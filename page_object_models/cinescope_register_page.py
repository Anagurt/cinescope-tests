import allure
from playwright.sync_api import Page, expect
from page_object_models.cinescope_header import CinescopeHeader

class CinescopeRegisterPage:
    def __init__(self, page: Page):
        self.header = CinescopeHeader(page)
        self.page = page
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

    @allure.step("Переход на страницу регистрации")
    def open(self):
        self.page.goto(self.url)

    @allure.step("Ввод ФИО")
    def input_name(self, name: str):
        self.register_name_input.fill(name)

    @allure.step("Ввод email")
    def input_email(self, email: str):
        self.register_email_input.fill(email)

    @allure.step("Ввод пароля")
    def input_password(self, password: str):
        self.register_password_input.fill(password)

    @allure.step("Ввод повторного пароля")
    def input_password_repeat(self, password: str):
        self.register_password_repeat_input.fill(password)

    @allure.step("Нажатие кнопки регистрации")
    def click_register_button(self):
        self.register_button.click()
    
    @allure.step("Переход на страницу логина")
    def click_login_button(self):
        self.register_to_login_button.click()

    @allure.step("Наведение на требования и проверка тултипа")
    def hover_requirements_button(self):
        self.register_requirements_button.hover()
        expect(self.password_requirements_tooltip).to_be_visible()

    @allure.step("Заполнение формы регистрации и отправка")
    def register(self, name: str, email: str, password: str, password_repeat: str):
        self.input_name(name)
        self.input_email(email)
        self.input_password(password)
        self.input_password_repeat(password_repeat)
        self.click_register_button()

    @allure.step("Ожидание редиректа на страницу логина")
    def wait_redirect_to_login_page(self):
        self.page.wait_for_url("https://dev-cinescope.coconutqa.ru/login")
        assert self.page.url == "https://dev-cinescope.coconutqa.ru/login", "Редирект на домашнюю старницу не произошел"


    @allure.step("Проверка всплывающего сообщения о подтверждении почты")
    def check_alert_text(self):
        notification_locator = self.page.get_by_text("Подтвердите свою почту")
        notification_locator.wait_for(state="visible")

        assert notification_locator.is_visible(), "Уведомление не появилось"
        notification_locator.wait_for(state="hidden")
        assert notification_locator.is_visible() == False, "Уведомление исчезло"


    @allure.step("Проверка отображения элементов на странице регистрации")
    def check_register_page_elements(self):
        expect(self.register_title).to_be_visible()
        expect(self.register_name_title).to_be_visible()
        expect(self.register_name_placeholder).to_be_visible()
        expect(self.register_email_title).to_be_visible()
        expect(self.register_email_placeholder).to_be_visible()
        expect(self.register_password_title).to_be_visible()
        expect(self.register_password_placeholder).to_be_visible()
        expect(self.register_password_repeat_title).to_be_visible()
        expect(self.register_password_repeat_placeholder).to_be_visible()
        expect(self.register_button).to_be_visible()
        expect(self.register_requirements_button).to_be_visible()
        expect(self.register_to_login_button).to_be_visible()