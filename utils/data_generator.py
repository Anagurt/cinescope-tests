import random
import string
from datetime import datetime

from faker import Faker

from entities.roles import Roles
from entities.location import Location
import os
import uuid

faker = Faker()


class DataGenerator:

    @staticmethod
    def generate_random_email(prefix: str = "user") -> str:
        worker = os.environ.get("PYTEST_XDIST_WORKER", "gw0")
        return f"{prefix}.{worker}.{uuid.uuid4().hex[:8]}@email.com"

    @staticmethod
    def generate_random_name() -> str:
        return f"{faker.first_name()} {faker.last_name()}"

    @staticmethod
    def generate_random_password() -> str:
        """
        Генерация пароля, соответствующего требованиям:
        - Минимум 1 буква.
        - Минимум 1 цифра.
        - Допустимые символы.
        - Длина от 8 до 20 символов.
        """
        letters = random.choices(string.ascii_letters)
        digits = random.choices(string.digits)

        # Дополняем пароль случайными символами из допустимого набора
        special_chars = "?@#$%^&*|:"
        all_chars = string.ascii_letters + string.digits + special_chars
        remaining_length = random.randint(6, 18)  # Остальная длина пароля
        remaining_chars = random.choices(all_chars, k=remaining_length)

        # Перемешиваем пароль для рандомизации
        password = list(letters + digits + remaining_chars)
        random.shuffle(password)

        return ''.join(password)

    @staticmethod
    def generate_random_name_movie() -> str:
        random_name_movie = faker.catch_phrase()
        return f"{random_name_movie}"

    @staticmethod
    def generate_random_price_movie() -> int:
        return random.randint(100, 10000)

    @staticmethod
    def generate_random_description_movie() -> str:
        random_description_movie = faker.text()
        return f"{random_description_movie}"

    @staticmethod
    def generate_user_data() -> dict:
        """
        Генерирует данные для тестового пользователя
        """
        from uuid import uuid4

        return {
            'id': f'{uuid4()}',  # генерируем UUID как строку
            'email': DataGenerator.generate_random_email(),
            'full_name': DataGenerator.generate_random_name(),
            'password': DataGenerator.generate_random_password(),
            'created_at': datetime.now(),
            'updated_at': datetime.now(),
            'verified': False,
            'banned': False,
            'roles': [Roles.USER]
        }

    @staticmethod
    def generate_movie_data() -> dict:
        """
        Генерирует данные для тестового фильма
        """
        return {
            'id': int(random.randint(90000, 1000000)),
            'name': DataGenerator.generate_random_name_movie(),
            'price': DataGenerator.generate_random_price_movie(),
            'description': DataGenerator.generate_random_description_movie(),
            'image_url':
            f"https://example.com/image_{int(random.randint(10000, 1000000))}.png",
            'location': random.choice(list(Location)).value,
            'published': True,
            'rating': float(random.randint(1, 10)),
            'genre_id': int(random.randint(1, 5)),
            'created_at': datetime.now(),
        }
