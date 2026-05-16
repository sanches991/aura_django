import multiprocessing
import os

bind = "0.0.0.0:8000"
workers = int(os.getenv("GUNICORN_WORKERS", multiprocessing.cpu_count() * 2 + 1))
worker_class = "gthread"
threads = 4

timeout = 60
graceful_timeout = 30
keepalive = 5

# === Важно: логи только в консоль (Docker-friendly) ===
accesslog = "-"
errorlog = "-"
loglevel = "info"

proc_name = "aura_gunicorn"
forwarded_allow_ips = "*"
