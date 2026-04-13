from sqlalchemy import create_engine, Column, String, Boolean, DateTime, text
from sqlalchemy.orm import declarative_base, sessionmaker
from resources.db_creds import MoviesDbCreds


# Подключение к базе данных
host = MoviesDbCreds.HOST
port = MoviesDbCreds.PORT
database_name = MoviesDbCreds.NAME
username = MoviesDbCreds.USER
password = MoviesDbCreds.PASSWORD

#  движок для подключения к базе данных
engine = create_engine(
    f"postgresql+psycopg2://{MoviesDbCreds.USER}:{MoviesDbCreds.PASSWORD}@{MoviesDbCreds.HOST}:{MoviesDbCreds.PORT}/{MoviesDbCreds.NAME}",
    echo=False  # Установить True для отладки SQL запросов
)

#  создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    """Создает новую сессию БД"""
    return SessionLocal()














# import psycopg2

# from resources.db_creds import MoviesDbCreds

# def connect_to_postgres():
#     """Функция для подключения к PostgreSQL базе данных"""
#     connection = None
#     cursor = None

#     try:
#         # Подключение к базе данных
#         connection = psycopg2.connect(
#             dbname=MoviesDbCreds.NAME,
#             user=MoviesDbCreds.USER,
#             password=MoviesDbCreds.PASSWORD,
#             host=MoviesDbCreds.HOST,
#             port=MoviesDbCreds.PORT,
#         )
#         print("Подключение успешно установлено")

#         # Создание курсора
#         cursor = connection.cursor()

#         # Вывод информации о PostgreSQL сервере
#         print("Информация о сервере PostgreSQL:")
#         print(connection.get_dsn_parameters(), "\n")

#         # Выполнение SQL-запроса
#         cursor.execute("SELECT version();")

#         # Получение результата
#         record = cursor.fetchone()
#         print("Вы подключены к - ", record, "\n")

#     except psycopg2.Error as error:
#         print("Ошибка при работе с PostgreSQL:", error)

#     finally:
#         # Закрытие соединения с базой данных
#         if cursor:
#             cursor.close()
#         if connection:
#             connection.close()
#             print("Соединение с PostgreSQL закрыто")
            

# if __name__ == "__main__":
#     connect_to_postgres()