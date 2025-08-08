# Book Library SPA API

REST API для управления библиотекой, разработанное с использованием Django, Django REST Framework и контейнеризованное с помощью Docker.


[![Django](https://img.shields.io/badge/Django-3.2.18-blue?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Django REST](https://img.shields.io/badge/DRF-3.16.0-red?logo=json&logoColor=white)](https://www.django-rest-framework.org/)
[![SimpleJWT](https://img.shields.io/badge/Simple_JWT-5.2.2-ff69b4?logo=jsonwebtokens&logoColor=white)](https://django-rest-framework-simplejwt.readthedocs.io/)
[![Python](https://img.shields.io/badge/Python-3.11+-yellow?logo=python&logoColor=white)](https://www.python.org/)
[![drf-yasg](https://img.shields.io/badge/drf--yasg-1.21.6-brightgreen?logo=swagger&logoColor=white)](https://drf-yasg.readthedocs.io/en/stable/readme.html#usage)
[![django-cors-headers](https://img.shields.io/badge/django--cors--headers-4.3.1-success?logo=cors&logoColor=white)](https://pypi.org/project/django-cors-headers/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-24.0+-blue?logo=docker&logoColor=white)](https://docs.docker.com/)
[![Docker Compose](https://img.shields.io/badge/Docker_Compose-2.23+-blue?logo=docker&logoColor=white)](https://docs.docker.com/compose/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue?logo=postgresql&logoColor=white)](https://hub.docker.com/_/postgres)


---
## 📋 Описание

Этот проект предоставляет API для:
*   Управления книгами и авторами.
*   Регистрации и аутентификации пользователей (JWT).
*   Отслеживания выдачи и возврата книг пользователям.

---

## 🚀 Начало работы

Эти инструкции помогут вам запустить проект локально для разработки или тестирования.

### 📦 Необходимые компоненты

*   `Docker`
*   `Docker Compose`

### 🛠️ Установка и запуск

1.  **Клонируйте репозиторий:**
    ```bash
    git clone <URL_вашего_репозитория>
    cd Book-Library-SPA
    ```

2.  **Настройте переменные окружения:**
    Создайте файл `.env` в корне проекта, скопировав `.env.example` (если он есть) и заполнив необходимые значения.
    Пример `.env`:
    ```env
    POSTGRES_DB=book_library_spa
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=ваш_пароль_postgres
    POSTGRES_HOST=db
    POSTGRES_PORT=5432

    SECRET_KEY=ваш_секретный_ключ_django
    DEBUG=True

    CORS_ALLOW_ALL_ORIGINS=True
    # Другие переменные при необходимости...
    ```

3.  **Запустите приложение:**

    *   **Для локальной разработки (с горячей перезагрузкой):**
        ```bash
        docker compose up --build
        ```
        Приложение будет доступно:
        *   Django dev server: `http://localhost:8000`
        *   Swagger UI (документация API): `http://localhost:8000/swagger/`
        *   Через Nginx: `http://localhost:8001`

    *   **Для режима, близкого к продакшену (только через Nginx) или для деплоя:**
    
        ```bash
        docker compose -f docker-compose.yml up --build
        ```
        Приложение будет доступно:
        *   Через Nginx: `http://localhost` (порт 80)


4.  **Остановка приложения:**
    ```bash
    # Для режима разработки
    docker compose down
    # Или с удалением volumes (осторожно, данные БД будут потеряны)
    docker compose down -v

    # Для режима продакшена
    docker compose -f docker-compose.yml down
    # Или с удалением volumes
    docker compose -f docker-compose.yml down -v
    ```

---

## 📡 API Endpoints

### Авторы
*   `GET /api/library/authors/` - Получить список авторов.
*   `POST /api/library/authors/` - Создать нового автора (только для администраторов).
*   `GET /api/library/authors/{id}/` - Получить информацию об авторе.
*   `PUT /api/library/authors/{id}/` - Обновить информацию об авторе (только для администраторов).
*   `DELETE /api/library/authors/{id}/` - Удалить автора (только для администраторов).

### Книги
*   `GET /api/library/books/` - Получить список книг. Поддерживает фильтрацию (см. ниже).
*   `POST /api/library/books/` - Создать новую книгу (только для администраторов).
*   `GET /api/library/books/{id}/` - Получить информацию о книге.
*   `PUT /api/library/books/{id}/` - Обновить информацию о книге (только для администраторов).
*   `DELETE /api/library/books/{id}/` - Удалить книгу (только для администраторов).

#### Фильтрация книг
При запросе `GET /api/library/books/` можно использовать параметры строки запроса:
*   `?title=часть_названия` - Поиск по названию книги.
*   `?author=фамилия_автора` - Поиск по фамилии автора.
*   `?genre=жанр` - Поиск по жанру.
*   `?available=true` - Только доступные книги.
*   `?available=false` - Только недоступные книги.

Пример: `http://localhost:8000/api/library/books/?title=Война&author=Толстой&available=true`

### Выдача книг
*   `GET /api/library/book-issues/` - Получить список выдач (пользователь видит только свои, администраторы - все).
*   `POST /api/library/book-issues/` - Создать запись о выдаче книги (только для персонала/администраторов).
*   `GET /api/library/book-issues/{id}/` - Получить информацию о конкретной выдаче.
*   `PUT /api/library/book-issues/{id}/` - Обновить информацию о выдаче (например, отметить возврат) (только для персонала/администраторов).

### Аутентификация и управление пользователями
*   `POST /api/accounts/register/` - Регистрация нового пользователя.
*   `POST /api/accounts/token/` - Получение JWT токенов (логин).
*   `POST /api/accounts/token/refresh/` - Обновление Access токена.
*   `GET /api/accounts/me/` - Получить информацию о текущем пользователе.
*   `PUT /api/accounts/me/` - Обновить информацию о текущем пользователе.
*   `GET /api/accounts/users/` - Получить список всех пользователей (только для администраторов).
*   `GET /api/accounts/users/{id}/` - Получить информацию о пользователе (только для администраторов).
*   `PUT /api/accounts/users/{id}/` - Обновить информацию о пользователе (только для администраторов).
*   `DELETE /api/accounts/users/{id}/` - Удалить пользователя (только для администраторов).

---

## 📚 Документация API

Документация API доступна в формате Swagger UI:
*   В режиме разработки: `http://localhost:8000/swagger/`
*   В режиме продакшена: `http://localhost/swagger/` (или просто `http://<ваш_домен>/swagger/`)

---

## 🏗️ Технический стек

*   **Backend:** Python, Django, Django REST Framework (DRF)
*   **Аутентификация:** JWT (SimpleJWT)
*   **База данных:** PostgreSQL
*   **Контейнеризация:** Docker, Docker Compose
*   **Документация API:** drf-yasg (OpenAPI/Swagger)
*   **Веб-сервер:** Nginx (в режиме продакшена)
*   **WSGI-сервер:** Gunicorn (в режиме продакшена)
*   **Дополнительно:** CORS, Django Filter

---

## 📁 Структура проекта

*   `accounts/` - Приложение для управления пользователями.
*   `library/` - Основное приложение для управления книгами, авторами и выдачами.
*   `config/` - Настройки Django проекта.
*   `Dockerfile` - Инструкции для сборки Docker-образа бэкенда.
*   `docker-compose.yml` - Основной файл Docker Compose для продакшена.
*   `docker-compose.override.yml` - Переопределения для локальной разработки.
*   `nginx.conf` - Конфигурация Nginx.
*   `requirements.txt` - Зависимости Python.
*   `.env` - Файл переменных окружения.
*   `.dockerignore` - Файлы и папки, игнорируемые при сборке Docker-образа.

---

## 📄 _Лицензия_
- MIT License © 2025
