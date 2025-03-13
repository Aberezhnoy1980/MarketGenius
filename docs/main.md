## Backend workflow

### Сервисы (endpoints)

1. Регистрация/Аутентификация (jwt-token - смотрим примеры)
2. Клиент для биржи - какая то готовность (PostgreSQL/Radis) 
3. Endpoints:

```python
def register(name: str, surname: str, email: str) -> bool:
```

```python
def get_prediction(ticker: str, date: Date, userdata: Auth) -> float:
```

<!-- ```python
def _get_history(ticker: str) -> list[Tuple[str, int]]:
```

```python
def _build_chart(List[Tuple[str, int]]):
```

```python
def _get_indicators(ticker: str) -> List[Dict[str, float]]:
``` -->

### Модели данных (entities)

1. Users
2. Subscription
3. Assets
4. History
5. Predictions
6. Indicators
7. News (MongoDB ?)
8. Features (ML/DL: S3 or SQL ? как удобнее использовать ?)
9. ???
