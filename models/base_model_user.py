from http import HTTPStatus

from pydantic import BaseModel, EmailStr, Field, field_validator

from entities.roles import Roles
from utils.iso_datetime import validate_iso8601_datetime_string


class UserInfoResponse(BaseModel):
    """
    Универсальная модель пользователя: ответ GET/POST/DELETE
    """
    id: str
    email: EmailStr
    fullName: str = Field(min_length=1,
                          max_length=100,
                          description="Полное имя пользователя")
    roles: list[Roles]
    verified: bool
    createdAt: str = Field(
        description="Дата и время создания пользователя в формате ISO 8601")
    banned: bool

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        return validate_iso8601_datetime_string(value)


class UserForbiddenResponse(BaseModel):
    message: str = "Доступ запрещен"
    error: str = "Forbidden"
    statusCode: int = HTTPStatus.FORBIDDEN


class UserNotFoundResponse(BaseModel):
    message: str = "Not Found"
    statusCode: int = HTTPStatus.NOT_FOUND
