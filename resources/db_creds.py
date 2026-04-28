import os

from dotenv import load_dotenv

load_dotenv()


class MoviesDbCreds:
    """
    Класс для хранения учетных данных для доступа к базе данных фильмов
    """
    HOST = os.getenv('MOVIES_DB_HOST')
    PORT = os.getenv('MOVIES_DB_PORT')
    NAME = os.getenv('MOVIES_DB_NAME')
    USER = os.getenv('MOVIES_DB_USER')
    PASSWORD = os.getenv('MOVIES_DB_PASSWORD')
