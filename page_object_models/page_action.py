from playwright.sync_api import Page, Locator
import allure

class PageAction:
    def __init__(self, page: Page):
        self.page = page

    @allure.step("Переход на страницу: {url}")
    def open_url(self, url: str):
        self.page.goto(url)

    @allure.step("Ввод текста '{text}' в поле '{name}'")
    def input_text_to_element(self, locator: Locator, text: str, name: str="Без имени"):
        locator.fill(text)

    @allure.step("Клик по элементу '{name}'")
    def click_on_element(self, locator: Locator, name: str="Без имени"):
        locator.click()

    @allure.step("Наведение курсора на элемент '{name}'")
    def hover_on_element(self, locator: Locator, name: str="Без имени"):
        locator.hover()
        
    @allure.step("Ожидание загрузки страницы: {url}")
    def wait_for_redirect_to_url(self, url: str):
        self.page.wait_for_url(url)

    @allure.step("Получение текста элемента: {name}")
    def get_element_text(self, locator: Locator, name: str="Без имени") -> str:
        return locator.text_content()
    
    @allure.step("Ожидание появления или исчезновения элемента: {name}, state = {state}")
    def wait_for_element(self, locator: Locator, state: str = "visible", name: str="Без имени"):
        locator.wait_for(state=state)

    @allure.step("Скриншот текущей страиницы")
    def make_screenshot_and_attach_to_allure(self):
        screenshot_path = "screenshot.png"
        self.page.screenshot(path=screenshot_path, full_page=True)  # full_page=True для скриншота всей страницы

        # Прикрепление скриншота к Allure-отчёту
        with open(screenshot_path, "rb") as file:
            allure.attach(file.read(), name="Screenshot after redirect", attachment_type=allure.attachment_type.PNG)

    @allure.step("Проверка всплывающего сообщения c текстом: {text}")
    def check_pop_up_element_with_text(self, text: str) -> bool:

        with allure.step("Проверка появления алерта с текстом: '{text}'"):
            notification_locator = self.page.get_by_text(text)
             # Ждем появления элемента
            notification_locator.wait_for(state="visible") 
            assert notification_locator.is_visible(), "Уведомление не появилось"

        with allure.step("Проверка исчезновения алерта с текстом: '{text}'"):
             # Ждем, пока алерт исчезнет
            notification_locator.wait_for(state="hidden") 
            assert notification_locator.is_visible() == False, "Уведомление не исчезло"