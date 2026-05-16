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

# ─── 3. ИСХОДНЫЙ КОД ─────────────────────────────────────────────────────────
COPY --chown=appuser:appgroup . .

# ─── 4. ПОДГОТОВКА ПАПОК ─────────────────────────────────────────────────────
USER root

RUN mkdir -p /app/logs /app/staticfiles /app/media \
    && chown -R appuser:appgroup /app \
    && chmod -R 775 /app/staticfiles /app/media /app/logs

# ─── 5. ENV ДЛЯ BUILD ────────────────────────────────────────────────────────
ARG SECRET_KEY=build-dummy-secret-key
ARG DB_ENGINE=django.db.backends.sqlite3

ENV SECRET_KEY=${SECRET_KEY} \
    DB_ENGINE=${DB_ENGINE} \
    DJANGO_SETTINGS_MODULE=aura_project.settings \
    PYTHONUNBUFFERED=1

# ─── 6. 🔥 ФИКС SOURCEMAP (ГЛАВНОЕ) ──────────────────────────────────────────
# Чистим ВСЕ JS (и в проекте, и в пакетах)
RUN find /app -name "*.js" -exec sed -i '/sourceMappingURL/d' {} \; \
 && find /usr/local/lib/python3.12/site-packages -name "*.js" -exec sed -i '/sourceMappingURL/d' {} \;

# ─── 7. COLLECTSTATIC ────────────────────────────────────────────────────────
RUN python manage.py collectstatic --noinput --clear

# ─── 8. ПЕРЕКЛЮЧАЕМСЯ НА БЕЗОПАСНОГО ЮЗЕРА ─────────────────────────────────
USER appuser

EXPOSE 8000

CMD ["gunicorn", "aura_project.wsgi:application", "--config", "gunicorn.conf.py"]
