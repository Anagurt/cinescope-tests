from clients.api_manager import ApiManager


class TestMoviesAPI:
    def test_get_movies(self, api_manager: ApiManager):
        """
        Тест на получение списка афиш фильмов (под правами не авторизованного пользователя).
        """
        response = api_manager.movies_api.get_movies()
        response_data = response.json()
        assert "movies" in response_data, "Отсутствие списков фильмов в ответе"


    def test_create_movie(self, api_manager: ApiManager, movie_data):
        """
        Тест на создание афиши фильма (под админскими правами).
        """
        api_manager.auth_api.authenticate_super_admin()
        response = api_manager.movies_api.create_movie(movie_data)
        response_data = response.json()
        movie_id = response_data["id"]
        assert "id" in response_data, "ID фильма отсутствует в ответе"
        assert response_data["name"] == movie_data["name"], "Название фильма не совпадает"
        assert response_data["imageUrl"] == movie_data["imageUrl"], "URL изображения фильма не совпадает"
        assert response_data["price"] == movie_data["price"], "Цена фильма не совпадает"
        assert response_data["description"] == movie_data["description"], "Описание фильма не совпадает"
        assert response_data["location"] == movie_data["location"], "Местоположение фильма не совпадает"
        assert response_data["published"] == movie_data["published"], "Публикация фильма не совпадает"
        assert response_data["genreId"] == movie_data["genreId"], "ID жанра фильма не совпадает"

        api_manager.movies_api.delete_movie(movie_id)
        

    def test_get_created_movie_by_super_admin(self, api_manager: ApiManager, movie_data):
        from datetime import datetime, timezone, timedelta

        """
        Тест на получение информации о созданной афише фильма (под админскими правами).
        """
        api_manager.auth_api.authenticate_super_admin()
        response = api_manager.movies_api.create_movie(movie_data)
        created_movie_id = response.json()["id"]
        response = api_manager.movies_api.get_movie(created_movie_id)
        response_data = response.json()
        assert created_movie_id == response_data["id"], "ID фильма не совпадает"
        assert "name" in response_data, "Название фильма отсутствует в ответе"
        assert "price" in response_data, "Цена фильма отсутствует в ответе"
        assert "description" in response_data, "Описание фильма отсутствует в ответе"
        assert "imageUrl" in response_data, "URL изображения фильма отсутствует в ответе"
        assert "location" in response_data, "Местоположение фильма отсутствует в ответе"
        assert "published" in response_data, "Публикация фильма отсутствует в ответе"
        assert "genreId" in response_data, "ID жанра фильма отсутствует в ответе"
        assert "createdAt" in response_data, "Дата создания фильма отсутствует в ответе"
        assert "rating" in response_data, "Рейтинг фильма отсутствует в ответе"
        assert "reviews" in response_data, "Отзывы фильма отсутствуют в ответе"

        created_at_str = response_data["createdAt"]
        created_at_utc = datetime.fromisoformat(created_at_str.replace("Z", "+00:00"))
        now_utc = datetime.now(timezone.utc)
        assert abs(now_utc - created_at_utc) <= timedelta(seconds=2), "Дата создания фильма отличается от текущего времени больше чем на 2 секунды"

        api_manager.movies_api.delete_movie(created_movie_id)

    def test_get_created_movie_by_user(self, api_manager: ApiManager, movie_data, registered_user):
        from datetime import datetime, timezone, timedelta

        """
        Тест на получение информации о созданной афише фильма (под авторизованным пользователем).
        """
        api_manager.auth_api.authenticate_super_admin()
        response = api_manager.movies_api.create_movie(movie_data)
        created_movie_id = response.json()["id"]

        api_manager.auth_api.authenticate((registered_user["email"], registered_user["password"]))
        response = api_manager.movies_api.get_movie(created_movie_id)
        response_data = response.json()
        assert created_movie_id == response_data["id"], "ID фильма не совпадает"
        assert "name" in response_data, "Название фильма отсутствует в ответе"
        assert "price" in response_data, "Цена фильма отсутствует в ответе"
        assert "description" in response_data, "Описание фильма отсутствует в ответе"
        assert "imageUrl" in response_data, "URL изображения фильма отсутствует в ответе"
        assert "location" in response_data, "Местоположение фильма отсутствует в ответе"
        assert "published" in response_data, "Публикация фильма отсутствует в ответе"
        assert "genreId" in response_data, "ID жанра фильма отсутствует в ответе"
        assert "createdAt" in response_data, "Дата создания фильма отсутствует в ответе"
        assert "rating" in response_data, "Рейтинг фильма отсутствует в ответе"
        assert "reviews" in response_data, "Отзывы фильма отсутствуют в ответе"

        created_at_str = response_data["createdAt"]
        created_at_utc = datetime.fromisoformat(created_at_str.replace("Z", "+00:00"))
        now_utc = datetime.now(timezone.utc)
        assert abs(now_utc - created_at_utc) <= timedelta(seconds=2), "Дата создания фильма отличается от текущего времени больше чем на 2 секунды"

        api_manager.auth_api.authenticate_super_admin()
        api_manager.movies_api.delete_movie(created_movie_id)

    def test_patch_change_movie_by_super_admin(self, api_manager: ApiManager, movie_data, change_movie_data):
        """
        Тест на изменение афиши фильма (под админскими правами).
        """
        api_manager.auth_api.authenticate_super_admin()
        response = api_manager.movies_api.create_movie(movie_data)
        created_movie_data = response.json()
        created_movie_id = created_movie_data["id"]

        response_changed_movie = api_manager.movies_api.change_movie(created_movie_id, change_movie_data)
        changed_movie_data = response_changed_movie.json()
  
        assert created_movie_id == changed_movie_data["id"], "ID фильма не совпадает"
        assert created_movie_data["name"] != changed_movie_data["name"], "Название фильма совпадает"
        assert created_movie_data["description"] != changed_movie_data["description"], "Описание фильма совпадает"
        assert created_movie_data["price"] != changed_movie_data["price"], "Цена фильма совпадает"

        api_manager.movies_api.delete_movie(created_movie_id)


    def test_delete_movie_by_super_admin(self, api_manager: ApiManager, movie_data):
        """
        Тест на удаление афиши фильма (под админскими правами).
        """
        api_manager.auth_api.authenticate_super_admin()
        response = api_manager.movies_api.create_movie(movie_data)
        created_movie_id = response.json()["id"]

        api_manager.movies_api.delete_movie(created_movie_id)
        api_manager.movies_api.get_movie(created_movie_id, expected_status=404)



# Негативные тесты MoviesAPI
    def test_movies_with_invalid_page(self, api_manager: ApiManager):
        """
        Негативный тест на получение списка афиш фильмов с некорректным параметром page.
        """
        api_manager.movies_api.get_movies(params={"page": -1}, expected_status=400)


    def test_movies_with_invalid_created_at(self, api_manager: ApiManager):
        """
        Негативный тест на получение списка афиш фильмов с некорректным параметром createdAt.
        """
        api_manager.movies_api.get_movies(params={"createdAt": "wrong"}, expected_status=400)


    def test_get_nonexistent_movie(self, api_manager: ApiManager):
        """
        Негативный тест на получение информации о несуществующем фильме.
        """
        api_manager.movies_api.get_movie(999999999, expected_status=404)


    def test_create_invalid_movie_data(self, api_manager: ApiManager, invalid_movie_data):
        """
        Негативный тест на создание афиши фильма с пустым полем name.
        """
        api_manager.auth_api.authenticate_super_admin()
        api_manager.movies_api.create_movie(invalid_movie_data, expected_status=400)


    def test_create_movie_by_user(self, api_manager: ApiManager, movie_data, registered_user):
        """
        Негативный тест на создание афиши фильма (под авторизованным пользователем).
        """
        api_manager.auth_api.authenticate((registered_user["email"], registered_user["password"]))
        api_manager.movies_api.create_movie(movie_data, expected_status=403)


    def test_create_same_movie(self, api_manager: ApiManager, movie_data):
        """
        Негативный тест на создание афиши фильма с теми же данными, что и уже существующего.
        """
        api_manager.auth_api.authenticate_super_admin()
        response = api_manager.movies_api.create_movie(movie_data)
        created_movie_id = response.json()["id"]
        api_manager.movies_api.create_movie(movie_data, expected_status=409)

        api_manager.movies_api.delete_movie(created_movie_id)


    def test_patch_movie_with_invalid_data(self, api_manager: ApiManager, movie_data, invalid_movie_data):
        """
        Негативный тест на изменение афиши фильма с некорректными данными.
        """
        api_manager.auth_api.authenticate_super_admin()
        response = api_manager.movies_api.create_movie(movie_data)
        created_movie_id = response.json()["id"]
        api_manager.movies_api.get_movie(created_movie_id, expected_status=200)
        api_manager.movies_api.change_movie(created_movie_id, invalid_movie_data, expected_status=400)

        api_manager.movies_api.delete_movie(created_movie_id)


    def test_patch_movie_by_user(self, api_manager: ApiManager, movie_data, registered_user):
        """
        Негативный тест на изменение афиши фильма (под пользователем).
        """
        api_manager.auth_api.authenticate((registered_user["email"], registered_user["password"]))
        api_manager.movies_api.create_movie(movie_data, expected_status=403)


    def test_patch_nonexistent_movie(self, api_manager: ApiManager):
        """
        Негативный тест на изменение информации о несуществующем фильме.
        """
        api_manager.auth_api.authenticate_super_admin()
        api_manager.movies_api.change_movie(999999999, {"name": "Новый фильм"}, expected_status=404)


    def test_delete_movie_by_user(self, api_manager: ApiManager, movie_data, registered_user):
        """
        Негативный тест на удаление афиши фильма (под пользователем).
        """
        api_manager.auth_api.authenticate_super_admin()
        response = api_manager.movies_api.create_movie(movie_data)
        created_movie_id = response.json()["id"]

        api_manager.auth_api.authenticate((registered_user["email"], registered_user["password"]))
        api_manager.movies_api.delete_movie(created_movie_id, expected_status=403)


    def test_delete_movie_with_invalid_id(self, api_manager: ApiManager):
        """
        Негативный тест на удаление афиши несуществующего фильма.
        """
        api_manager.auth_api.authenticate_super_admin()
        api_manager.movies_api.delete_movie(999999999, expected_status=404)