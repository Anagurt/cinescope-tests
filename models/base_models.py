from pydantic import BaseModel, Field, field_validator, EmailStr
from typing import Optional
import datetime
import re
from typing import List
from entities.roles import Roles

def _assert_iso_datetime_string(value: str) -> str:
    """Проверяем, что строка является корректной датой и временем в формате ISO 8601."""
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    datetime.datetime.fromisoformat(normalized)
    return value

class RegisterUserRequest(BaseModel):
    email: EmailStr
    fullName: str
    password: str
    passwordRepeat: str = Field(..., min_length=1, max_length=20, description="passwordRepeat должен вполностью совпадать с полем password")
    roles: list[Roles] = [Roles.USER]
    verified: Optional[bool] = None
    banned: Optional[bool] = None

    @field_validator("passwordRepeat")
    def check_password_repeat(cls, value: str, info) -> str:
        # Проверяем, совпадение паролей
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
    fullName: str = Field(min_length=1, max_length=100, description="Полное имя пользователя")
    verified: bool
    banned: bool
    roles: List[Roles]
    createdAt: str = Field(description="Дата и время создания пользователя в формате ISO 8601")

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        # Валидатор для проверки формата даты и времени (ISO 8601).
        try:
            return _assert_iso_datetime_string(value)
        except ValueError:
            raise ValueError("Некорректный формат даты и времени. Ожидается формат ISO 8601.")

    


class LoginUserRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=20)

    # @field_validator("password")
    # def check_password(cls, value: str) -> str:
    #     if not any(c.islower() for c in value):
    #         raise ValueError("нужна минимум одна строчная буква")
    #     if not any(c.isupper() for c in value):
    #         raise ValueError("нужна минимум одна заглавная буква")
    #     if not any(c.isdigit() for c in value):
    #         raise ValueError("нужна минимум одна цифра")
    #     return value


class LoginUserPayload(BaseModel):
    id: str
    email: EmailStr
    fullName: str
    roles: List[Roles]

class LoginResponse(BaseModel):
    user: LoginUserPayload
    accessToken: str
    refreshToken: str
    expiresIn: int

# Приходят те же поля и что и при удалении пользователя 
class UserInfoResponse(BaseModel):
    id: str
    email: EmailStr
    fullName: str
    roles: List[Roles]
    verified: bool
    banned: bool
    createdAt: str = Field(description="Дата и время создания пользователя в формате ISO 8601")

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        # Валидатор для проверки формата даты и времени (ISO 8601).
        try:
            return _assert_iso_datetime_string(value)
        except ValueError:
            raise ValueError("Некорректный формат даты и времени. Ожидается формат ISO 8601.")
