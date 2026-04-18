import random
import string

from faker import Faker

faker = Faker()


class DataGenerator:

    @staticmethod
    def generate_random_email():
        return faker.email()

    @staticmethod
    def generate_random_name():
        return f"{faker.first_name()} {faker.last_name()}"

    @staticmethod
    def generate_random_password():
        """
        Генерация пароля, соответствующего требованиям:
        - Минимум 1 буква.
        - Минимум 1 цифра.
        - Допустимые символы.
        - Длина от 8 до 20 символов.
        """
        return faker.password(length=faker.random_int(min=8, max=20), special_chars=True, digits=True, upper_case=True, lower_case=True)

    @staticmethod
    def generate_random_name_movie():
        random_name_movie = faker.catch_phrase()
        return f"{random_name_movie}"

    @staticmethod
    def generate_random_price_movie():
        return random.randint(100, 10000)

    @staticmethod
    def generate_random_description_movie():
        random_description_movie = faker.text()
        return f"{random_description_movie}"
