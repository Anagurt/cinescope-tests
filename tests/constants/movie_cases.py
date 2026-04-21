from constants import MovieConstants, MovieOperations
from resources.user_creds import RegularUserCreds, AdminCreds
import pytest

GET_MOVIES_PARAMS_CASES = [
    MovieConstants.RANGE_PRICE_PARAMS,
    MovieConstants.LOCATION_PARAMS,
    MovieConstants.GENRE_ID_PARAMS,
]
GET_MOVIES_PARAMS_IDS = [
    "Фильмы в диапазоне цен",
    "Фильмы в Москве",
    "Фильмы в жанре с ID 1",
]

INVALID_GET_MOVIES_PARAMS_CASES = [
    MovieConstants.INVALID_PAGE_PARAMS,
    MovieConstants.EQUAL_PRICE_PARAMS,
    MovieConstants.INVALID_CREATED_AT_PARAMS,
    MovieConstants.INVALID_GENRE_ID_PARAMS,
]
INVALID_GET_MOVIES_PARAMS_IDS = [
    "Отрицательная страница",
    "Минимальное и максимальное значение в диапазоне цен равны",
    "Некорректный параметр createdAt",
    "Значение genreId равно 0",
]

INVALID_MOVIE_FIELDS_CASES = [
    pytest.param(
        MovieConstants.INVALID_MOVIE_DATA_WITH_EMPTY_NAME,
        marks=pytest.mark.xfail(
            reason=(
                "Баг в ответе API, ожидаемый ответ BAD_REQUEST, "
                "приходит NOT_FOUND"
            ),
            strict=False,
        ),
    ),
    pytest.param(
        MovieConstants.INVALID_MOVIE_DATA_WITH_NEGATIVE_PRICE,
        marks=pytest.mark.skip(
            reason=(
                "Баг в ответе API, ожидаемый ответ BAD_REQUEST, "
                "приходит OK"
            ),
        ),
    ),
    MovieConstants.INVALID_MOVIE_DATA_WITH_ZERO_GENRE_ID,
]

INVALID_MOVIE_FIELDS_IDS = [
    "Пустое поле name",
    "Отрицательное значение price",
    "Значение genreId равно 0",
]

HTTP_MOVIE_OPERATIONS_CASES = [
    MovieOperations.GET,
    MovieOperations.DELETE,
    MovieOperations.PATCH
]

HTTP_MOVIE_OPERATIONS_IDS = [
    "GET несуществующего фильма",
    "DELETE несуществующего фильма",
    "PATCH несуществующего фильма",
]

ADMIN_AND_REGULAR_USER_CASES = [
    (AdminCreds.USERNAME, AdminCreds.PASSWORD),
    (RegularUserCreds.USERNAME, RegularUserCreds.PASSWORD),
]
ADMIN_AND_REGULAR_USER_IDS = [
    "Под админом",
    "Под пользователем",
]
