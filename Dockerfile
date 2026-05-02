# ... (твой код выше)

# ─── Исходный код
COPY --chown=appuser:appgroup . .

# ХАК: Создаем папку логов и даем на неё права ПЕРЕД сборкой статики
# Также фиксим права на весь /app на всякий случай
USER root
RUN mkdir -p /app/logs && chown -R appuser:appgroup /app/logs && chmod -R 755 /app/logs

# ХАК: Создаем пустой файл .map
RUN mkdir -p /app/static/vendor/bootstrap/js/ && \
    touch /app/static/vendor/bootstrap/js/bootstrap.bundle.min.js.map

RUN python manage.py collectstatic --noinput

# Переключаемся на непривилегированного пользователя
USER appuser

EXPOSE 8000

CMD ["gunicorn", "aura_project.wsgi:application", "--config", "gunicorn.conf.py"]