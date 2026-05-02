"""
Gunicorn configuration — оптимизировано под 2 CPU ядра.
Формула воркеров: (2 × CPU) + 1 = 5
"""
import multiprocessing
import os

# ─── Сетевой интерфейс ────────────────────────────────────────────────────────
bind = "0.0.0.0:8000"

# ─── Воркеры ─────────────────────────────────────────────────────────────────
workers = int(os.getenv("GUNICORN_WORKERS", multiprocessing.cpu_count() * 2 + 1))
worker_class = "gthread"    # I/O-bound Django → gthread эффективнее gevent
threads = 4                 # потоков на воркер
worker_connections = 1000

# ─── Лимиты запросов (защита от утечек памяти) ───────────────────────────────
max_requests = 1000
max_requests_jitter = 100   # ±100 запросов — предотвращает одновременный рестарт

# ─── Тайм-ауты ───────────────────────────────────────────────────────────────
timeout = 60                # воркер убивается, если молчит дольше 60 с
graceful_timeout = 30       # время на завершение текущих запросов при рестарте
keepalive = 5               # keep-alive соединения (сек)

# ─── Логирование ─────────────────────────────────────────────────────────────
# Docker перехватывает stdout/stderr и пишет в свой драйвер логов.
# Файловые логи — дополнительно, с ротацией через logrotate на хосте.
accesslog = "/app/logs/gunicorn_access.log"
errorlog  = "/app/logs/gunicorn_error.log"
loglevel  = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# ─── Процесс ─────────────────────────────────────────────────────────────────
proc_name = "aura_gunicorn"
forwarded_allow_ips = "*"   # доверяем заголовкам от Nginx-прокси
