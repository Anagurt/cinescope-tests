from playwright.sync_api import Page
from page_object_models.base_page import BasePage

class CinescopeMoviesPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "/movies"
        self.movies_filters_place_combobox = page.get_by_role("combobox").filter(has_text="Место")
        self.movies_filters_genre_combobox = page.get_by_role("combobox").filter(has_text="Жанр")
        self.movies_filters_sorting_combobox = page.get_by_role("combobox").filter(has_text="Создано")
        self.movies_details_movie_button = page.get_by_role("link", name="Подробнее").first

    def open(self):
        self.open_url(self.url)

    def click_first_movie_details(self):
        self.click_on_element(self.movies_details_movie_button, "Кнопка 'Подробнее' первого фильма")