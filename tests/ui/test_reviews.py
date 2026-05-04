import allure
import pytest
from resources.user_creds import RegularUserCreds
from utils.data_generator import DataGenerator


@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы Movie Details")
@pytest.mark.ui
class TestMovieReviews:

    @pytest.mark.smoke
    @allure.story("Авторизованный пользователь может оставить отзыв под фильмом")
    def test_leave_review(self, login_page, movies_page, movie_details_page):
        login_page.open()
        login_page.login(RegularUserCreds.USERNAME, RegularUserCreds.PASSWORD)
        login_page.wait_redirect_to_home_page()

        movies_page.open()
        movies_page.click_first_movie_details()
        test_review_text = DataGenerator.generate_random_description_movie()
        movie_details_page.write_review(test_review_text)

        movie_details_page.check_review_is_visible(test_review_text)

        movie_details_page.delete_review(test_review_text)