from http import HTTPStatus

import pytest
from pathlib import Path
from playwright.sync_api import Page

from db_requester.db_helpers import DBHelper
from entities.user import User
from models.base_models_auth import RegisterUserRequest
from page_object_models import PageAction, BasePage, CinescopeRegisterPage, CinescopeLoginPage, CinescopeMoviesPage, CinescopeMovieDetailsPage

LONG_UI_TIMEOUT = 30000
SHORT_UI_TIMEOUT = 5000


@pytest.fixture(scope="session")  # Браузер запускается один раз для всей сессии
def browser(playwright):
    browser = playwright.chromium.launch(headless=False)  # headless=True для CI/CD, headless=False для локальной разработки
    yield browser  # yield возвращает значение фикстуры, выполнение теста продолжится после yield
    browser.close()  # Браузер закрывается после завершения всех тестов


@pytest.fixture(scope="function")  # Контекст создается для каждого теста
def context(browser, request, base_url):
    context = browser.new_context(base_url=base_url)
    context.tracing.start(screenshots=True, snapshots=True, sources=True)  # Трассировка для отладки
    context.set_default_timeout(LONG_UI_TIMEOUT)  # Установка таймаута по умолчанию
    
    yield context  # yield возвращает значение фикстуры, выполнение теста продолжится после yield
    
    test_name = request.node.name
    Path("test-results").mkdir(parents=True, exist_ok=True)
    context.tracing.stop(path=f"test-results/{test_name}-trace.zip")
    context.close()  # Контекст закрывается после завершения теста


@pytest.fixture(scope="function")  # Страница создается для каждого теста
def page(context):
    page = context.new_page()
    yield page  # yield возвращает значение фикстуры, выполнение теста продолжится после yield
    page.close()  # Страница закрывается после завершения теста

@pytest.fixture
def page_action(page: Page) -> PageAction:
    return PageAction(page)

@pytest.fixture
def base_page(page: Page) -> BasePage:
    return BasePage(page)

@pytest.fixture
def register_page(page: Page) -> CinescopeRegisterPage:
    return CinescopeRegisterPage(page)

@pytest.fixture
def login_page(page: Page) -> CinescopeLoginPage:
    return CinescopeLoginPage(page)

@pytest.fixture
def movies_page(page: Page) -> CinescopeMoviesPage:
    return CinescopeMoviesPage(page)

@pytest.fixture
def movie_details_page(page: Page) -> CinescopeMovieDetailsPage:
    return CinescopeMovieDetailsPage(page)


@pytest.fixture
def cleanup_registered_user_after_test(
    test_user: RegisterUserRequest,
    super_admin: User,
    db_helper: DBHelper,
) -> None:
    """
    После UI-регистрации удаляет пользователя по email (API супер-админа + проверка в БД).
    Если пользователь не создавался (тест упал раньше) — выход.
    """
    yield
    super_admin.api.auth_api.authenticate()
    user_in_db = db_helper.get_user_by_email(test_user.email)
    if user_in_db is None:
        return
    response = super_admin.api.user_api.delete_user(str(user_in_db.id), expected_status=HTTPStatus.OK)
    if response.status_code != HTTPStatus.OK:
        raise RuntimeError(
            "cleanup_registered_user_after_test: unexpected "
            f"status {response.status_code}, body: {response.text!r}"
        )