HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}

BASE_AUTH_URL = "https://auth.dev-cinescope.coconutqa.ru"
BASE_MOVIES_URL = "https://api.dev-cinescope.coconutqa.ru"

LOGIN_ENDPOINT = "/login"
REGISTER_ENDPOINT = "/register"
MOVIES_ENDPOINT = "/movies"
USER_ENDPOINT = "/user"

GREEN = '\033[32m'
RED = '\033[31m'
RESET = '\033[0m'


class CommonConstants:
    EMPTY_STR = ""
    FULL_NAME_DEFAULT = "ФИО пользователя"
    EMAIL_VALID = "test.register0123456789@email.com"
    PASSWORD_VALID = "asdqwe123Q!"
    NON_EXISTENT_ID = "non_existent_id"
    NON_EXISTENT_EMAIL = "non_existent_email"
    NON_EXISTENT_USER_ID = "00000000-0000-0000-0000-000000000000"
    NON_EXISTENT_MOVIE_ID = 999999999

    INVALID_EMAIL_WITHOUT_AT = "test.registeremail.com"
    INVALID_EMAIL_DOMAIN_NO_DOT = "test.register@emailcom"
    INVALID_EMAIL_EMPTY_LOCAL = "@email.com"

    PASSWORD_SHORT = "Qwerty7"
    PASSWORD_LONG = "QwertyuiopasdfghjklzxcvbnmQwer33X"


class MovieConstants:
    RANGE_PRICE_PARAMS = {"minPrice": 9, "maxPrice": 10}
    LOCATION_PARAMS = {"locations": "MSK"}
    GENRE_ID_PARAMS = {"genreId": 1}

    PATCH_MOVIE_DATA_NEGATIVE_CASES = {
        "name": "Любое название фильма",
        "description": "Рандомное описание фильма",
        "price": 1,
        "location": "SPB",
        "imageUrl": "https://example.com/x.png",
        "published": True,
        "genreId": 1
    }

    INVALID_PAGE_PARAMS = {"page": -1}
    EQUAL_PRICE_PARAMS = {"minPrice": 10, "maxPrice": 10}
    INVALID_CREATED_AT_PARAMS = {"createdAt": "wrong"}
    INVALID_GENRE_ID_PARAMS = {"genreId": 0}

    INVALID_MOVIE_DATA_WITH_EMPTY_NAME = {
        "name": "",
        "imageUrl": "https://example.com/image.png",
        "price": 10,
        "description": "Описание фильма",
        "location": "SPB",
        "published": True,
        "genreId": 1
    }
    INVALID_MOVIE_DATA_WITH_NEGATIVE_PRICE = {
        "name": "Невалидный фильм",
        "imageUrl": "https://example.com/image.png",
        "price": -1,
        "description": "Описание фильма",
        "location": "SPB",
        "published": True,
        "genreId": 1
    }

    INVALID_MOVIE_DATA_WITH_ZERO_GENRE_ID = {
        "name": "Невалидный фильм",
        "imageUrl": "https://example.com/image.png",
        "price": 10,
        "description": "Описание фильма",
        "location": "SPB",
        "published": True,
        "genreId": 0
    }


class MovieMethods:
    GET = "get_movie"
    DELETE = "delete_movie"
    PATCH = "patch_movie"
