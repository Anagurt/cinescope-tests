# from http import HTTPStatus

# import allure
# import pytest

# from clients.api_manager import ApiManager


# @allure.feature("Негативные тесты для movies API")
# class TestMoviesAPINegative:
#     @allure.story("Негативный тест на получение списка афиш фильмов с некорректным параметром page")
#     def test_movies_with_invalid_page(self, api_manager: ApiManager):
#         api_manager.movies_api.get_movies(params={"page": -1}, expected_status=HTTPStatus.BAD_REQUEST)

#     @allure.story("Негативный тест на получение списка афиш фильмов с некорректным параметром createdAt")
#     def test_movies_with_invalid_created_at(self, api_manager: ApiManager):
#         api_manager.movies_api.get_movies(params={"createdAt": "wrong"}, expected_status=HTTPStatus.BAD_REQUEST)

#     @allure.story("Негативный тест на получение информации о несуществующем фильме")
#     def test_get_nonexistent_movie(self, api_manager: ApiManager):
#         api_manager.movies_api.get_movie(999999999, expected_status=HTTPStatus.NOT_FOUND)

#     @allure.story("Негативный тест на создание афиши фильма с пустым полем name")
#     def test_create_invalid_movie_data(self, api_manager: ApiManager, authorized_super_admin: ApiManager):
#         invalid_movie_data = {
#             "name": "",
#             "imageUrl": "",
#             "price": -1,
#             "description": "",
#             "location": "",
#             "published": False,
#             "genreId": 0,
#         }

#         authorized_super_admin.movies_api.post_movie(invalid_movie_data, expected_status=HTTPStatus.BAD_REQUEST)

#     @allure.story("Негативный тест на создание афиши фильма (под авторизованным пользователем)")
#     def test_create_movie_by_registered_user(self, authorized_registered_user: ApiManager, movie_data: dict):
#         authorized_registered_user.movies_api.post_movie(movie_data, expected_status=HTTPStatus.FORBIDDEN)

#     @allure.story("Негативный тест на создание афиши фильма с теми же данными, что и уже существующего")
#     def test_create_same_movie_duplicated(self, authorized_super_admin: ApiManager, created_movie_and_cleanup: dict):
#         authorized_super_admin.movies_api.post_movie(created_movie_and_cleanup, expected_status=HTTPStatus.CONFLICT)

#     @allure.story("Негативный тест на изменение афиши фильма с некорректными данными")
#     def test_change_movie_with_invalid_data(self, authorized_super_admin: ApiManager, created_movie_and_cleanup: dict):
#         created_movie_id = created_movie_and_cleanup["id"]
#         invalid_movie_data = {
#             "name": "",
#             "imageUrl": "",
#             "price": -1,
#             "description": "",
#             "location": "",
#             "published": False,
#             "genreId": 0,
#         }
            
#         authorized_super_admin.movies_api.patch_movie(created_movie_id, invalid_movie_data, expected_status=HTTPStatus.BAD_REQUEST)

#     @allure.story("Негативный тест на изменение афиши фильма с пустыми данными")
#     @pytest.mark.skip(reason="Баг в ответе API, ожидаемый ответ BAD_REQUEST, приходит NOT_FOUND")
#     def test_change_movie_with_empty_data(self, authorized_super_admin: ApiManager, created_movie_and_cleanup: dict):
#         created_movie_id = created_movie_and_cleanup["id"]
#         empty_name_movie_data = created_movie_and_cleanup
#         empty_name_movie_data["name"] = ""

#         authorized_super_admin.movies_api.patch_movie(created_movie_id, empty_name_movie_data, expected_status=HTTPStatus.BAD_REQUEST)

#     @allure.story("Негативный тест на изменение афиши фильма (под пользователем)")
#     def test_change_movie_by_registered_user(self, authorized_registered_user: ApiManager, created_movie_and_cleanup, movie_data: dict, registered_user: dict):
#         created_movie_id = created_movie_and_cleanup["id"]

#         authorized_registered_user.auth_api.authenticate((registered_user["email"], registered_user["password"]))

#         authorized_registered_user.movies_api.patch_movie(created_movie_id, movie_data, expected_status=HTTPStatus.FORBIDDEN)

#     @allure.story("Негативный тест на изменение информации о несуществующем фильме")
#     def test_change_nonexistent_movie(self, authorized_super_admin: ApiManager):
#         authorized_super_admin.movies_api.patch_movie(999999999, {"name": "Новый фильм"}, expected_status=HTTPStatus.NOT_FOUND)

#     @allure.story("Негативный тест на удаление афиши фильма (под пользователем)")
#     def test_delete_movie_by_registered_user(self, created_movie_and_cleanup: dict, authorized_registered_user: ApiManager, registered_user: dict):
#         created_movie_id = created_movie_and_cleanup["id"]

#         authorized_registered_user.auth_api.authenticate((registered_user["email"], registered_user["password"]))

#         authorized_registered_user.movies_api.delete_movie(created_movie_id, expected_status=HTTPStatus.FORBIDDEN)

#     @allure.story("Негативный тест на удаление афиши несуществующего фильма")
#     def test_delete_nonexistent_movie(self, authorized_super_admin: ApiManager):
#         authorized_super_admin.auth_api.authenticate()

#         authorized_super_admin.movies_api.delete_movie(999999999, expected_status=HTTPStatus.NOT_FOUND)
