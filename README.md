# Cinescope — API-тесты

Автотесты для бэкенда Cinescope: регистрация/авторизация, пользователи, афиша фильмов

## Запуск тестов

Все тесты:
```bash
pytest tests/
```

## Allure

Для сбор отчета при прогоне тестов:
```bash
pytest tests/ --alluredir=allure-results
```

При необходимости очистить старые результаты перед прогоном:
```bash
rm -rf allure-results && pytest tests/ --alluredir=allure-results
```

## Структура проекта

Cinescope/
├── clients/                 # HTTP-клиенты API
│   ├── api_manager.py       # общая сессия и доступ к auth / user / movies
│   ├── auth_api.py
│   ├── movies_api.py
│   └── user_api.py
├── custom_requester/        # обёртка над requests (логирование, заголовки)
├── utils/
│   └── data_generator.py    # Faker и генерация тестовых данных
├── tests/
│   └── api/
│       ├── auth_api/        # позитивные и негативные тесты авторизации
│       └── movie_api/       # тесты афиши фильмов
├── constants.py             # URL эндпоинтов, загрузка .env, ADMIN_*
├── conftest.py              # фикстуры pytest
├── requirements.txt
├── requirements-dev.txt     # линтеры + allure-pytest
├── pyproject.toml
├── .flake8
└── .style.yapf

