# autotests-api

Фреймворк API-автотестов на Python для демо-приложения LMS. Проект реализует клиентскую архитектуру поверх HTTPX, валидацию контрактов через Pydantic и JSON Schema, фикстуры pytest с цепочкой зависимостей и отчётность Allure.

**Тестируемое API:** [qa-automation-engineer-api-course](https://github.com/Nikita-Filonov/qa-automation-engineer-api-course)  
**Базовый URL по умолчанию:** `http://localhost:8000`

---

## Содержание

- [Технологический стек](#технологический-стек)
- [Архитектура](#архитектура)
- [Структура проекта](#структура-проекта)
- [Требования](#требования)
- [Установка и настройка](#установка-и-настройка)
- [Запуск тестов](#запуск-тестов)
- [Маркировка тестов](#маркировка-тестов)
- [Отчётность Allure](#отчётность-allure)
- [CI/CD](#cicd)
- [Принципы разработки](#принципы-разработки)

---

## Технологический стек

| Инструмент | Назначение |
|---|---|
| **Python 3.12** | Язык реализации |
| **HTTPX** | HTTP-клиент (Sync API) |
| **Pydantic** | Модели запросов/ответов, валидация данных |
| **pydantic-settings** | Конфигурация из `.env` |
| **jsonschema** | Валидация JSON-ответов по схеме |
| **pytest** | Тестовый раннер, фикстуры, маркеры, параметризация |
| **pytest-xdist** | Параллельный запуск тестов |
| **pytest-rerunfailures** | Повторный запуск нестабильных тестов |
| **Allure Report** | Структурированная отчётность |
| **Faker** | Генерация тестовых данных |

---

## Архитектура

Проект построен на паттерне **API Client** с разделением на публичные и приватные эндпоинты:

```
Schemas  →  API Clients  →  Assertions  →  Tests
                ↑
         HTTP Builders + Fixtures
```

| Слой | Ответственность | Пример |
|---|---|---|
| **Schemas** | Pydantic-модели запросов и ответов | `CreateUserRequestSchema`, `LoginResponseSchema` |
| **API Clients** | HTTP-взаимодействие с API | `PublicUsersClient`, `CoursesClient` |
| **HTTP Builders** | Создание настроенных `httpx.Client` | `get_public_http_client`, `get_private_http_client` |
| **Assertions** | Проверки статус-кодов, полей, схем | `assert_create_user_response`, `validate_json_schema` |
| **Fixtures** | Подготовка клиентов и тестовых сущностей | `function_user`, `function_course` |
| **Tests** | Сценарии проверки бизнес-логики | `TestUsers`, `TestCourses` |

### Публичный и приватный доступ

| Тип клиента | Аутентификация | Примеры эндпоинтов |
|---|---|---|
| **Public** | Без токена | Регистрация пользователя, логин |
| **Private** | Bearer-токен (получается через `AuthenticationClient.login`) | CRUD курсов, упражнений, файлов, профиль пользователя |

Приватный клиент кэшируется через `@lru_cache` по паре `email` / `password`, что исключает повторную авторизацию в рамках одного тестового прогона.

### Event Hooks

Каждый HTTP-клиент подключает event hooks:

- генерация и прикрепление **cURL-команды** к Allure-отчёту;
- логирование запросов и ответов;
- шаги Allure на уровне методов `APIClient` (`GET`, `POST`, `PATCH`, `DELETE`).

### Цепочка фикстур

Тестовые данные создаются каскадно:

```
function_user  →  function_file  →  function_course  →  function_exercise
```

Каждая фикстура возвращает объект с полями `request` и `response`, что упрощает проверки и переиспользование данных между тестами.

---

## Структура проекта

```
autotests-api/
├── clients/                     # HTTP-клиенты API
│   ├── api_client.py            # Базовый клиент (GET/POST/PATCH/DELETE)
│   ├── public_http_builder.py   # Клиент без авторизации
│   ├── private_http_builder.py  # Клиент с Bearer-токеном
│   ├── event_hooks.py           # cURL, логирование, Allure-вложения
│   ├── errors_schema.py         # Схемы ошибок API
│   ├── authentication/          # Клиент и схемы аутентификации
│   ├── users/                   # Public/Private клиенты пользователей
│   ├── courses/                 # CRUD курсов
│   ├── exercises/               # CRUD упражнений
│   └── files/                   # Загрузка и управление файлами
├── fixtures/                    # Pytest-фикстуры
│   ├── authentication.py
│   ├── users.py
│   ├── files.py
│   ├── courses.py
│   ├── exercises.py
│   └── allure.py
├── tests/                       # Тестовые сценарии
│   ├── authentication/
│   ├── users/
│   ├── courses/
│   ├── exercises/
│   └── files/
├── tools/
│   ├── allure/                  # Таксономия Allure (epic, feature, story, tags)
│   ├── assertions/              # Доменные и базовые проверки
│   ├── http/                    # Утилиты (генерация cURL)
│   ├── fakers.py                # Генератор тестовых данных
│   ├── routes.py                # Константы маршрутов API
│   └── logger.py
├── testdata/files/              # Тестовые файлы
├── config.py                    # Настройки приложения (pydantic-settings)
├── conftest.py
├── pytest.ini
├── requirements.txt
├── .env                         # Переменные окружения
└── .github/workflows/tests.yml  # CI-пайплайн
```

---

## Требования

- Python 3.12
- Запущенный экземпляр тестового API-сервера
- Git

---

## Установка и настройка

### 1. Клонирование репозитория

```bash
git clone https://github.com/prikhodkomihail/autotests-api.git
cd autotests-api
```

### 2. Создание виртуального окружения

```bash
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate         # Windows
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

Зависимости проекта:

```
allure-pytest==2.15.2
email_validator==2.3.0
Faker==38.0.0
httpx==0.28.1
jsonschema==4.25.1
pydantic==2.12.4
pydantic-settings==2.12.0
pytest==9.0.1
pytest-rerunfailures==15.0
pytest-xdist==3.8.0
```

### 4. Запуск тестового API-сервера

```bash
git clone https://github.com/Nikita-Filonov/qa-automation-engineer-api-course.git
cd qa-automation-engineer-api-course
pip install -r requirements.txt

export APP_HOST="http://localhost:8000"
export DATABASE_URL="sqlite+aiosqlite:///./local.db"
export JWT_ALGORITHM="HS256"
export JWT_SECRET_KEY="qa-automation-engineer-api-course-secret-key"
export JWT_ACCESS_TOKEN_EXPIRE=1800
export JWT_REFRESH_TOKEN_EXPIRE=5184000

uvicorn main:app --host 0.0.0.0 --port 8000
```

### 5. Конфигурация окружения

Скопируйте `.env.example` в `.env` и при необходимости измените значения:

```env
TEST_DATA.IMAGE_PNG_FILE='./testdata/files/image.png'

HTTP_CLIENT.URL='http://localhost:8000'
HTTP_CLIENT.TIMEOUT=100
```

| Переменная | Описание |
|---|---|
| `HTTP_CLIENT.URL` | Базовый URL API |
| `HTTP_CLIENT.TIMEOUT` | Таймаут HTTP-запросов (секунды) |
| `TEST_DATA.IMAGE_PNG_FILE` | Путь к тестовому изображению для загрузки файлов |

---

## Запуск тестов

### Все регрессионные тесты

```bash
pytest -m regression
```

### Параллельный запуск

```bash
pytest -m regression --numprocesses 2
```

### По функциональной области

```bash
pytest tests/authentication/
pytest tests/users/
pytest tests/courses/
pytest tests/exercises/
pytest tests/files/
```

### По маркерам

```bash
pytest -m users
pytest -m authentication
pytest -m courses
pytest -m exercises
pytest -m files
pytest -m "regression and courses"
```

### Конкретный тест

```bash
pytest tests/users/test_users.py::TestUsers::test_create_user
```

---

## Маркировка тестов

Маркеры определены в `pytest.ini`:

| Маркер | Назначение |
|---|---|
| `users` | Операции с пользователями |
| `files` | Загрузка и управление файлами |
| `courses` | CRUD курсов |
| `exercises` | CRUD упражнений |
| `authentication` | Аутентификация и токены |
| `regression` | Регрессионный набор |

---

## Отчётность Allure

Тесты аннотированы иерархией Allure:

- **Epic** — система (`LMS system`, `Student system`, `Administration system`)
- **Feature** — функциональная область (`Users`, `Courses`, `Authentication` и др.)
- **Story** — пользовательский сценарий (`CREATE_ENTITY`, `GET_ENTITY`, `LOGIN` и др.)
- **Severity** — критичность (`BLOCKER`, `CRITICAL`, `NORMAL`)
- **Tags** — дополнительные метки для фильтрации

### Генерация и просмотр отчёта

```bash
pytest -m regression --alluredir=allure-results
allure serve allure-results
```

В отчёт автоматически попадают:

- cURL-команда каждого HTTP-запроса;
- файл `environment.properties` с параметрами окружения, ОС и версией Python;
- шаги Allure на уровне HTTP-методов и assertion-функций.

---

## CI/CD

Проект содержит GitHub Actions workflow (`.github/workflows/tests.yml`):

1. Checkout репозитория автотестов.
2. Клонирование и запуск тестового API-сервера на `localhost:8000`.
3. Установка зависимостей из `requirements.txt`.
4. Запуск `pytest -m regression --alluredir=allure-results --numprocesses 2`.
5. Публикация Allure-отчёта на GitHub Pages с сохранением истории прогонов.

---

## Принципы разработки

### Добавление нового эндпоинта

1. Описать Pydantic-схемы в `clients/{domain}/{domain}_schema.py`.
2. Добавить маршрут в `tools/routes.py`.
3. Реализовать методы клиента в `clients/{domain}/{domain}_client.py`:
   - `*_api()` — возвращает `httpx.Response` (для проверки статус-кода и схемы);
   - типизированный метод — парсит ответ через `model_validate_json`.
4. Добавить доменные assertion-функции в `tools/assertions/{domain}.py`.
5. При необходимости — фикстуру в `fixtures/{domain}.py`.
6. Написать тест с маркерами и Allure-аннотациями.

### Соглашения по именованию

| Объект | Паттерн | Пример |
|---|---|---|
| Тестовый класс | `Test{Feature}` | `TestUsers` |
| Тестовый метод | `test_{scenario}` | `test_create_user` |
| API-клиент | `{Domain}Client` | `CoursesClient` |
| Схема запроса | `{Action}{Domain}RequestSchema` | `CreateUserRequestSchema` |
| Схема ответа | `{Action}{Domain}ResponseSchema` | `CreateUserResponseSchema` |
| Метод с Response | `{action}_{domain}_api` | `create_user_api` |
| Фикстура сущности | `function_{entity}` | `function_user` |
| Фикстура клиента | `{domain}_client` | `courses_client` |

### Пример теста

```python
def test_create_user(self, domain: str, public_users_client: PublicUsersClient):
    request = CreateUserRequestSchema(email=fake.email(domain=domain))
    response = public_users_client.create_user_api(request)
    response_data = CreateUserResponseSchema.model_validate_json(response.text)

    assert_status_code(response.status_code, HTTPStatus.OK)
    assert_create_user_response(request, response_data)
    validate_json_schema(response.json(), response_data.model_json_schema())
```

### Покрытие API

| Область | Сценарии |
|---|---|
| **Authentication** | Логин с корректными credentials |
| **Users** | Создание пользователя (параметризация по домену email), получение профиля `/me` |
| **Files** | Загрузка, получение, обновление, удаление файлов |
| **Courses** | Создание, получение, обновление, удаление курсов |
| **Exercises** | CRUD упражнений в рамках курса |

### Маршруты API

| Маршрут | Назначение |
|---|---|
| `/api/v1/users` | Управление пользователями |
| `/api/v1/authentication` | Аутентификация и обновление токена |
| `/api/v1/files` | Работа с файлами |
| `/api/v1/courses` | Управление курсами |
| `/api/v1/exercises` | Управление упражнениями |

