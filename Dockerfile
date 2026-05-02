# ─────────────────────────────────────────────────────────────────────────────
# AURA — Dockerfile
# Базовый образ: Python 3.12 slim (Debian Bookworm)
# ─────────────────────────────────────────────────────────────────────────────
FROM python:3.12-slim AS base

# Системные зависимости: libpq для psycopg2, gcc для компиляции C-расширений
RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq-dev \
        gcc \
    && rm -rf /var/lib/apt/lists/*

# Создаём непривилегированного пользователя
RUN groupadd --system appgroup && useradd --system --gid appgroup appuser

WORKDIR /app

# ─── Зависимости (отдельный слой — кэшируется при неизменном requirements.txt)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ─── Исходный код
COPY --chown=appuser:appgroup . .

# ─── Папка для Gunicorn-логов
RUN mkdir -p /app/logs && chown -R appuser:appgroup /app/logs

# ─── Сборка статики (переменные нужны только для collectstatic)
ARG SECRET_KEY=build-dummy-secret-key-not-used-in-prod
ARG DB_ENGINE=django.db.backends.sqlite3
ENV SECRET_KEY=${SECRET_KEY} \
    DB_ENGINE=${DB_ENGINE} \
    DJANGO_SETTINGS_MODULE=aura_project.settings

RUN python manage.py collectstatic --noinput

# Переключаемся на непривилегированного пользователя
USER appuser

EXPOSE 8000

CMD ["gunicorn", "aura_project.wsgi:application", "--config", "gunicorn.conf.py"]
