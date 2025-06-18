# API

## /register

### Запрос

```bash
POST /register
Body: { 
  "login": "john_doe", 
  "email": "john_doe@example.ex"
  "password": "qwerty123" 
  }
```


### Ответ

* success:

```JSON
{
  "status": "ok",
  "message": "Письмо с подтверждением отправлено"
}
```

* errors:

409 Conflict — если email или логин заняты.

400 Bad Request — если email невалиден (если добавите проверку).

## /login

### Запрос

```bash
POST /login
Body: { 
  "login": "john_doe", 
  "password": "qwerty123" 
  }
```


### Ответ

* success:

```json
{
  "status": "success",
  "user": {
    "id": 123,
    "login": "john_doe",
    "email": "john@example.com",
    "email_verified": true
  }
}
```

* errors:

```json
{
  "detail": "Неверный логин или пароль"
}
```