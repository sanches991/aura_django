# ─── 1. БАЗОВЫЙ ОБРАЗ ────────────────────────────────────────────────────────
FROM python:3.12-slim

# Системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq-dev \
        gcc \
    && rm -rf /var/lib/apt/lists/*

# Создаём пользователя
RUN groupadd --system appgroup && useradd --system --gid appgroup appuser

WORKDIR /app

# ─── 2. ЗАВИСИМОСТИ ──────────────────────────────────────────────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ─── 3. ИСХОДНЫЙ КОД И ПРАВА ─────────────────────────────────────────────────
# Копируем проект
COPY --chown=appuser:appgroup . .

# Переключаемся на root, чтобы создать системные папки и выставить права
USER root

# Создаем папку логов и даем права appuser
RUN mkdir -p /app/logs && \
    touch /app/logs/django.log && \
    chown -R appuser:appgroup /app/logs && \
    chmod -R 775 /app/logs

# ХАК: Создаем пустой файл .map для статики
RUN mkdir -p /app/static/vendor/bootstrap/js/ && \
    touch /app/static/vendor/bootstrap/js/bootstrap.bundle.min.js.map

# ─── 4. СБОРКА СТАТИКИ ───────────────────────────────────────────────────────
ARG SECRET_KEY=build-dummy-secret-key
ARG DB_ENGINE=django.db.backends.sqlite3
ENV SECRET_KEY=${SECRET_KEY} \
    DB_ENGINE=${DB_ENGINE} \
    DJANGO_SETTINGS_MODULE=aura_project.settings

RUN python manage.py collectstatic --noinput

# ─── 5. ЗАПУСК ───────────────────────────────────────────────────────────────
USER appuser

EXPOSE 8000

CMD ["gunicorn", "aura_project.wsgi:application", "--config", "gunicorn.conf.py"]