FROM python:3.11-slim

# Установка зависимостей системы
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /app

# Копирование requirements и установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода приложения
COPY . .

# Создание директорий для статики и медиа
RUN mkdir -p /static /media

# Команда по умолчанию
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn --workers=2 --bind 0.0.0.0:8000 config.wsgi:application"]
