from http import HTTPStatus

from pydantic import BaseModel, EmailStr, Field, field_validator

from entities.roles import Roles
from utils.iso_datetime import validate_iso8601_datetime_string


class RegisterUserRequest(BaseModel):
    email: EmailStr
    fullName: str
    password: str
    passwordRepeat: str = Field(
        ...,
        min_length=1,
        max_length=20,
        description="passwordRepeat должен вполностью совпадать с полем password",
    )
    roles: list[Roles] = [Roles.USER]
    verified: bool | None = None
    banned: bool | None = None

    @field_validator("passwordRepeat")
    def check_password_repeat(cls, value: str, info) -> str:
        if "password" in info.data and value != info.data["password"]:
            raise ValueError("Пароли не совпадают")
        return value

    # Добавляем кастомный JSON-сериализатор для Enum
    class Config:
        json_encoders = {
            Roles: lambda v: v.value  # Преобразуем Enum в строку
        }


class RegisterUserResponse(BaseModel):
    id: str
    email: EmailStr
    fullName: str = Field(min_length=1,
                          max_length=100,
                          description="Полное имя пользователя")
    verified: bool
    banned: bool
    roles: list[Roles]
    createdAt: str = Field(
        description="Дата и время создания пользователя в формате ISO 8601")

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        return validate_iso8601_datetime_string(value)


class RegisterUserBadRequestResponse(BaseModel):
    message: list[str]
    error: str = "Bad Request"
    statusCode: int = HTTPStatus.BAD_REQUEST


class RegisterUserConflictResponse(BaseModel):
    message: str = "Пользователь с таким email уже зарегистрирован"
    error: str = "Conflict"
    statusCode: int = HTTPStatus.CONFLICT


class LoginUserRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=20)

    @field_validator("password")
    def check_password(cls, value: str) -> str:
        if not any(c.islower() for c in value):
            raise ValueError("нужна минимум одна строчная буква")
        if not any(c.isupper() for c in value):
            raise ValueError("нужна минимум одна заглавная буква")
        if not any(c.isdigit() for c in value):
            raise ValueError("нужна минимум одна цифра")
        return value


class LoginUserPayload(BaseModel):
    id: str
    email: EmailStr
    fullName: str
    roles: list[Roles]


class LoginResponse(BaseModel):
    user: LoginUserPayload
    accessToken: str
    refreshToken: str
    expiresIn: int


class LoginUserUnauthorizedResponse(BaseModel):
    message: str = "Неверный логин или пароль"
    error: str = "Unauthorized"
    statusCode: int = HTTPStatus.UNAUTHORIZED
