from playwright.sync_api import Page
from page_object_models.base_page import BasePage

class CinescopeMovieDetailsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "/movies/{movie_id}"
        # Локаторы элементов только с которыми работаем в тесте
        self.movie_details_reviews_title = page.get_by_role("heading", name="Отзывы:")

        self.movie_details_review_rating_combobox = page.locator("div").filter(has_text="Оценка:").get_by_role("combobox")
        self.movie_details_review_text_input = page.get_by_role("textbox", name="Написать отзыв", exact=True)
        self.movie_details_review_send_button = page.get_by_role("button", name="Отправить", exact=True)
        self.movie_details_review_delete_button = page.get_by_role("menuitem", name="Удалить", exact=True)

    def open(self):
        self.open_url(self.url)

    def write_review(self, text: str, rating: str = "5"):
        self.click_on_element(self.movie_details_review_rating_combobox, "Раскрыть список оценок")
        
        rating_option = self.page.get_by_role("option", name=rating)
        self.click_on_element(rating_option, f"Выбор оценки: {rating}")
        
        self.input_text_to_element(self.movie_details_review_text_input, text, "Поле ввода отзыва")
        self.click_on_element(self.movie_details_review_send_button, "Кнопка 'Отправить отзыв'")
    
    def check_review_is_visible(self, text: str):
        review_locator = self.page.get_by_text(text)
        self.wait_for_element(review_locator, "visible", f"Блок с текстом отзыва: '{text[:10]}...'")

    def delete_review(self, text: str):
        kebab_button = self.page.locator("div").filter(has_text=text).locator("button").first
        self.click_on_element(kebab_button, "Меню действий с нашим отзывом")

        self.click_on_element(self.movie_details_review_delete_button, "Кнопка 'Удалить' отзыв")
        review_locator = self.page.get_by_text(text)
        self.wait_for_element(review_locator, "hidden", f"Удаленный отзыв: '{text[:10]}...'")
