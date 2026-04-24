from http import HTTPStatus
from typing import Callable, Generator

import pytest
import requests
from sqlalchemy.orm import Session

from clients.api_manager import ApiManager
from db_models.movies import MovieDBModel
from db_models.user import UserDBModel
from db_requester.db_client import get_db_session
from db_requester.db_helpers import DBHelper
from entities.location import Location
from entities.roles import Roles
from entities.user import User
from models.base_model_movies import MovieInfoRequest, MovieInfoResponse
from models.base_models_auth import RegisterUserRequest
from resources.user_creds import RegularUserCreds, SuperAdminCreds
from utils.data_generator import DataGenerator


@pytest.fixture
def anonymous_api_manager() -> Generator[ApiManager, None, None]:
    """
    Фикстура для создания экземпляра ApiManager без заголовков авторизации
    """
    http_session = requests.Session()
    try:
        yield ApiManager(http_session)
    finally:
        http_session.close()


@pytest.fixture
def api_manager(anonymous_api_manager: ApiManager) -> ApiManager:
    """Алиас для тестов, ожидающих имя фикстуры api_manager."""
    return anonymous_api_manager


@pytest.fixture
def user_session() -> Generator[Callable[[], ApiManager], None, None]:
    """
    Фикстура для создания сессии юзера
    """
    user_pool = []

    def _create_user_session() -> ApiManager:
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()


@pytest.fixture
def super_admin(user_session: Callable[[], ApiManager]) -> User:
    """
    Фикстура для создания супер-админа
    """
    new_session = user_session()

    super_admin = User(SuperAdminCreds.ID, SuperAdminCreds.USERNAME,
                       SuperAdminCreds.PASSWORD, [Roles.SUPER_ADMIN],
                       new_session)

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin


@pytest.fixture
def regular_user(user_session: Callable[[], ApiManager]) -> User:
    """
    Фикстура для создания обычного пользователя
    """
    new_session = user_session()

    regular_user = User(RegularUserCreds.ID, RegularUserCreds.USERNAME,
                        RegularUserCreds.PASSWORD, [Roles.USER], new_session)

    regular_user.api.auth_api.authenticate(regular_user.creds)
    return regular_user


@pytest.fixture
def test_user() -> RegisterUserRequest:
    """
    Фикстура для генерации данных для нового пользователя «сырье»
    """
    random_password = DataGenerator.generate_random_password()
    return RegisterUserRequest(email=DataGenerator.generate_random_email(),
                               fullName=DataGenerator.generate_random_name(),
                               password=random_password,
                               passwordRepeat=random_password,
                               roles=[Roles.USER])


@pytest.fixture
def creation_user_data(test_user: RegisterUserRequest) -> RegisterUserRequest:
    """
    Фикстура для генерации данных для нового пользователя (объект класса User)
    """
    updated_data = test_user.model_dump(mode="json")
    updated_data.update({"verified": True, "banned": False})
    return RegisterUserRequest.model_validate(updated_data)
# ______________

@pytest.fixture
def common_user(
        user_session: Callable[[], ApiManager],
        super_admin: User,
        creation_user_data: RegisterUserRequest,
        db_helper: DBHelper,
) -> Generator[User, None, None]:
    """
    Фикстура для создания обычного пользователя (объект класса User)
    """

    new_session = user_session()

    create_response = super_admin.api.user_api.create_user(creation_user_data)
    user_id = create_response.json()["id"]

    common_user = User(user_id, creation_user_data.email,
                       creation_user_data.password, [Roles.USER], new_session)

    common_user.api.auth_api.authenticate(common_user.creds)

    yield common_user

    super_admin.api.auth_api.authenticate()
    if db_helper.get_user_by_id(str(user_id)):
        delete_response = super_admin.api.user_api.delete_user(
            user_id, expected_status=None)
        _expect_http_ok(
            delete_response,
            f"удаление пользователя {user_id} после теста",
        )


def _expect_http_ok(response: requests.Response, context: str) -> None:
    if response.status_code == HTTPStatus.OK:
        return
    raise RuntimeError(
        f"{context}: unexpected status {response.status_code}, body: {response.text!r}"
    )


@pytest.fixture
def users_to_cleanup(
        super_admin: User,
        db_helper: DBHelper,
) -> Generator[list[str], None, None]:
    created_user_ids = []

    yield created_user_ids

    super_admin.api.auth_api.authenticate()
    for user_id in dict.fromkeys(created_user_ids):
        if not db_helper.get_user_by_id(str(user_id)):
            continue
        response = super_admin.api.user_api.delete_user(
            user_id, expected_status=None)
        _expect_http_ok(
            response,
            f"delete user {user_id} in users_to_cleanup",
        )

# _______________________________________________________________________________
# Фикстуры для MoviesAPI


@pytest.fixture
def movie_data() -> MovieInfoRequest:
    """
    Фикстура для генерации случайного фильма.
    """

    return MovieInfoRequest(
        name=DataGenerator.generate_random_name_movie(),
        imageUrl="https://example.com/image.png",
        price=DataGenerator.generate_random_price_movie(),
        description=DataGenerator.generate_random_description_movie(),
        location=Location.SPB,
        published=True,
        genreId=1,
    )


@pytest.fixture
def created_movie_and_cleanup(
        super_admin: User, movie_data: MovieInfoRequest,
        db_helper: DBHelper,
) -> Generator[MovieInfoResponse, None, None]:
    """
    Фикстура для создания фильма и удаления его после теста.
    """

    super_admin.api.auth_api.authenticate()

    response = super_admin.api.movies_api.post_movie(
        movie_data, expected_status=HTTPStatus.CREATED,
        success_response_model=MovieInfoResponse)

    created = response.validated_response

    yield created

    super_admin.api.auth_api.authenticate()
    if not db_helper.get_movie_by_id(created.id):
        return
    response = super_admin.api.movies_api.delete_movie(
        created.id,
        expected_status=None,
    )
    _expect_http_ok(response, "delete movie")


@pytest.fixture
def movies_to_cleanup(
        super_admin: User,
        db_helper: DBHelper,
) -> Generator[list[int], None, None]:
    """
    Список id фильмов на удаление в конце сессии для подчистки фильмов с меткой в name.
    """

    created_movie_ids = []

    yield created_movie_ids

    super_admin.api.auth_api.authenticate()
    for movie_id in dict.fromkeys(created_movie_ids):
        if not db_helper.get_movie_by_id(movie_id):
            continue
        response = super_admin.api.movies_api.delete_movie(
            movie_id, expected_status=None)
        _expect_http_ok(
            response,
            f"delete movie {movie_id} in movies_to_cleanup",
        )


# Фикстуры для работы с БД (SQLAlchemy)


@pytest.fixture(scope="module")
def db_session() -> Generator[Session, None, None]:
    """
    Фикстура, которая создает и возвращает сессию для работы с базой данных
    После завершения тестов сессия автоматически закрывается
    """
    db_session = get_db_session()

    yield db_session

    db_session.close()


@pytest.fixture
def db_helper(db_session: Session) -> DBHelper:
    """
    Фикстура для экземпляра хелпера
    """
    db_helper = DBHelper(db_session)
    return db_helper


@pytest.fixture
def created_test_user(db_helper: DBHelper) -> Generator[UserDBModel, None, None]:
    """
    Фикстура, которая создает тестового пользователя в БД
    и удаляет его после завершения теста
    """

    user = db_helper.create_test_user(DataGenerator.generate_user_data())

    yield user

    if db_helper.get_user_by_id(user.id):
        db_helper.delete_user(user)


@pytest.fixture
def created_test_movie(db_helper: DBHelper) -> Generator[MovieDBModel, None, None]:
    """
    Фикстура, которая создает тестовый фильм в БД
    и удаляет его после завершения теста
    """

    movie = db_helper.create_movie(DataGenerator.generate_movie_data())

    yield movie

    if db_helper.get_movie_by_id(movie.id):
        db_helper.delete_movie(movie)
