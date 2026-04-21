from http import HTTPStatus

from pydantic import BaseModel, Field, field_validator

from entities.location import Location
from utils.iso_datetime import validate_iso8601_datetime_string


class MovieInfoRequest(BaseModel):
    """
    Запрос на создание/обновление фильма
    """
    name: str
    imageUrl: str
    price: int = Field(..., ge=1, description="Цена фильма")
    description: str
    location: Location = Field(..., description="Местоположение фильма")
    published: bool
    genreId: int = Field(..., description="ID жанра")


class MovieGenrePayload(BaseModel):
    name: str


class MovieInfoResponse(BaseModel):
    """
    Универсальная модель фильма: элемент списка GET /movies, ответ POST/DELETE/PATCH
    """
    id: int
    name: str
    description: str
    genreId: int
    imageUrl: str | None = None
    price: int
    rating: float
    location: Location
    published: bool
    createdAt: str = Field(
        description="Дата и время создания записи в формате ISO 8601")
    genre: MovieGenrePayload

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        return validate_iso8601_datetime_string(value)


class GetMoviesListResponse(BaseModel):
    """
    Ответ GET /movies
    """
    movies: list[MovieInfoResponse]
    count: int
    page: int
    pageSize: int
    pageCount: int


class MovieReviewUserPayload(BaseModel):
    """
    Пользователь, оставивший отзыв
    """
    fullName: str


class MovieReviewItem(BaseModel):
    """
    Отзыв на фильм
    """
    userId: str
    rating: int
    text: str
    createdAt: str = Field(
        description="Дата и время отзыва в формате ISO 8601")
    user: MovieReviewUserPayload

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        return validate_iso8601_datetime_string(value)


class GetMovieByIdResponse(MovieInfoResponse):
    """
    Ответ GET /movies/{id}
    """
    reviews: list[MovieReviewItem]


class GetMovieBadRequest(BaseModel):
    message: str | list[str]
    error: str = "Bad Request"
    statusCode: int = HTTPStatus.BAD_REQUEST


class GetMovieNotFoundResponse(BaseModel):
    message: str = "Фильм не найден"
    error: str = "Not Found"
    statusCode: int = HTTPStatus.NOT_FOUND


class GetMovieForbiddenResponse(BaseModel):
    message: str = "Forbidden resource"
    error: str = "Forbidden"
    statusCode: int = HTTPStatus.FORBIDDEN


class GetMovieConflictResponse(BaseModel):
    message: str = "Фильм с таким названием уже существует"
    error: str = "Conflict"
    statusCode: int = HTTPStatus.CONFLICT
