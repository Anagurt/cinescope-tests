import os

from dotenv import load_dotenv

load_dotenv()


class SuperAdminCreds:
    """
    Класс для хранения учетных данных супер-администратора
    """
    ID = os.getenv('SUPER_ADMIN_ID')
    USERNAME = os.getenv('SUPER_ADMIN_USERNAME')
    PASSWORD = os.getenv('SUPER_ADMIN_PASSWORD')

class AdminCreds:
    """
    Класс для хранения учетных данных администратора
    """
    ID = os.getenv('ADMIN_ID')
    USERNAME = os.getenv('ADMIN_USERNAME')
    PASSWORD = os.getenv('ADMIN_PASSWORD')

class RegularUserCreds:
    """
    Класс для хранения учетных данных тестового пользователя
    """
    ID = os.getenv('REGULAR_USER_ID')
    USERNAME = os.getenv('REGULAR_USER_USERNAME')
    PASSWORD = os.getenv('REGULAR_USER_PASSWORD')
