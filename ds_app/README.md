# Запуск БД

## Запускаем тестовую бд из контейнера:

Версия Docker на момент написания: 

[//]: # (![docker desktop]&#40;../../docs/img/docker_bundle_version.png&#41;)
<img src="../docs/img/docker_bundle_version.png" width="300">

файл compose.yaml:

```yaml
services:
  postgres:
    container_name: postgres_container
    image: postgres:14
    command:
      - "postgres"
      - "-c"
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
      POSTGRES_DB: "moexdb"
      POSTGRES_USER: "moexuser"
      POSTGRES_PASSWORD: "pg4moex"
      PGDATA: "/var/lib/postgresql/data/pgdata"
    volumes:
      - ./init_sql/:/docker-entrypoint-initdb.d
      - moexdb-data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U moexuser -d moexdb"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 10s
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 4G
    networks:
      - postgres

  postgres_exporter:
    container_name: exporter_container
    image: prometheuscommunity/postgres-exporter:v0.10.1
    environment:
      DATA_SOURCE_URI: "postgres:5432/moexdb?sslmode=disable"
      DATA_SOURCE_USER: "moexuser"
      DATA_SOURCE_PASS: "pg4moex"
      PG_EXPORTER_EXTEND_QUERY_PATH: "/etc/postgres_exporter/queries.yaml"
    volumes:
      - ./queries.yaml:/etc/postgres_exporter/queries.yaml:ro
    ports:
      - "9187:9187"
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: '0.2'
          memory: 500M
    networks:
      - postgres

volumes:
  moexdb-data:

networks:
  postgres:
    driver: bridge
```

## Публикуем модуль [simplest_async_s3client](https://pypi.org/project/simplest-async-s3client/) для работы с S3 на PyPI

Регистрируемся на pypi.org и test.pypi.org
Особенность второго ресурса не только в его предназначении тестирования модулей, но и в том что при установке модуля 
(pip install) не выйдет подтянуть зависимости

https://packaging.python.org/en/latest/tutorials/packaging-projects/

Добавляем зависимости:

https://packaging.python.org/en/latest/guides/writing-pyproject-toml/

Собираем дистрибутив:

```shell
python3 -m build
```

Публикуем для тестирования:

```shell
python3 -m twine upload --repository testpypi dist/* --verbose
```

В реальный регистр:

```shell
python3 -m twine upload dist/* --verbose 
```

Устанавливаем:

```shell
pip install simplest_async_s3client
```