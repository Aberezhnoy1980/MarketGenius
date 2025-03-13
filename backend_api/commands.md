## Установка окружения

<hr>

Виртуальная среда

```SHELL
python3 -m venv .backend_api_env
```

Активация

```SHELL
source ./.backend_api_env/bin/activate
```

Проверка

```SHELL
which python; which pip; python -V; pip -V
```

## Фреймоврк

<hr>

Установка fastspi

```SHELL
pip install "fastapi[standart]"
```

Установка uvicorn

```SHELL
pip install uvicorn
```

Создание файла с зависимостями

```SHELL
pip freeze > requirements.txt
```

## База данных

<hr>

Установка pydantic-settings для переменных окружения и работы с ними

```SHELL
pip install pydantic-settings
```

Установка ORM

```SHELL
pip install sqlalchemy
```

Установка системы версионирования

```SHELL
pip install alembic
```

Не забываем (так как с базой данных работаем асинхронно) установить asyncpg

```SHELL
pip install asyncpg
```

Установка форматера и его настройка

```SHELL
pip install black
```

Файл alembic.ini

```ini
script_location = src/migrations
file_template = %%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(rev)s_%%(slug)s
prepend_sys_path = . src
version_path_separator = os
sqlalchemy.url = driver://user:pass@localhost/dbname
hooks = black
black.type = console_scripts
black.entrypoint = black
black.options = -l 88 REVISION_SCRIPT_FILENAME
```

compose.yaml

```yaml
services:
  postgres:
    container_name: mg_backend_users
    image: postgres:14
    command:
      - "postgres"
      - "-c"
#      - "config_file=/etc/postgresql.conf"
      - "max_connections=50"
      - "-c"
      - "shared_buffers=1GB"
      - "-c"
      - "effective_cache_size=4GB"
      - "-c"
      - "work_mem=16MB"
      - "-c"
      - "maintenance_work_mem=512MB"
      - "-c"
      - "random_page_cost=1.1"
      - "-c"
      - "temp_file_limit=10GB"
      - "-c"
      - "log_min_duration_statement=200ms"
      - "-c"
      - "idle_in_transaction_session_timeout=10s"
      - "-c"
      - "lock_timeout=1s"
      - "-c"
      - "statement_timeout=60s"
      - "-c"
      - "shared_preload_libraries=pg_stat_statements"
      - "-c"
      - "pg_stat_statements.max=10000"
      - "-c"
      - "pg_stat_statements.track=all"
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASS}
      PGDATA: "/var/lib/postgresql/data/pgdata"
    volumes:
#      - ./init_sql/:/docker-entrypoint-initdb.d
      - ./booking-data:/var/lib/postgresql/data
#      - ./postgresql.conf:/etc/postgresql.conf:ro
    ports:
      - "${DB_PORT}:5432"
    healthcheck:
      test: [ "CMD-SHELL", "pg_isready -U ${DB_USER} -d ${DB_NAME}" ]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 10s
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: "1"
          memory: 4G
    networks:
      - postgres

  postgres_exporter:
    container_name: exporter_container_for_booking
    image: prometheuscommunity/postgres-exporter:v0.10.1
    environment:
      DATA_SOURCE_URI: "postgres:5432/${DB_NAME}?sslmode=disable"
      DATA_SOURCE_USER: ${DB_USER}
      DATA_SOURCE_PASS: ${DB_PASS}
      PG_EXPORTER_EXTEND_QUERY_PATH: "/etc/postgres_exporter/queries.yaml"
    volumes:
      - ./queries.yaml:/etc/postgres_exporter/queries.yaml:ro
    ports:
      - "9189:9187"
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: "0.2"
          memory: 500M
    networks:
      - postgres

volumes:
  booking-data:

networks:
  postgres:
    driver: bridge
```

Запуск

```docker
docker compose --env-file .env up
```

Миграции
Инициализация

```SHELL
alembic init src/migrations 
```

Файл env.py (миграции не асинхронные)

```python
from backend_api.src.config import settings
from backend_api.src.database import Base
from backend_api.src.models.users import UsersOrm

config.set_main_option("sqlalchemy.url", f"{settings.DB_URL}?async_fallback=True")

target_metadata = Base.metadata
```

Создание скрипта

```SHEL
alembic revision --autogenerate -m "init migration"
```

Миграция

```SHELL
alembic upgrade head
```

## Авторизация/Аутентификация

Установка библиотек

```SHELL
pip install pyjwt "passlib[bcrypt]"
```

Валидация электронной почты

```SHELL
pip install email_validator
```
Создание случайного секретного ключа

```SHELL
openssl rand -hex 32
```