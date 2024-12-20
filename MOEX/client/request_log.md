## Струтура данных MOEX и логика построения запросов

### Структура ИСС
![ISS concept](/MOEX/client/img/ISS.png)

### Интерфейсы блоков ИСС
![ISS concept](/MOEX/client/img/interfaces.png)

[Программный интерфейс к ИСС](https://www.moex.com/a2193)

Руководство разработчика ИСС Московской биржи

### Авторизация

Используется basic-аутентификация, то есть имя пользователя и пароль передаются
серверу в заголовке запроса в соответствии со спецификацией.
Возможны следующие способы аутентификации:

1. По специальной ссылке по протоколу HTTPS:
`https://passport.moex.com/authenticate`
2. По любой ссылке на ресурсы (см. справочник запросов) по протоколу HTTP.
3. При подключении без аутентификации итоги торгов и ход торгов в режиме online
недоступны.
При успешной аутентификации сервер возвращает cookie с именем MicexPassportCert,
хранящей сертификат аутентификации. Cookie должен быть сохранён до указанного в
нём времени жизни (expire) и отправляться при последующих запросах.

**Пример**

```python
# python example
import requests
from requests.auth import HTTPBasicAuth

url = 'https://passport.moex.com/authenticate'

# Basic authentication credentials
username = <login>
password = <password>

# Make a GET request with Basic Authentication
response = requests.get(url, auth=HTTPBasicAuth(username, password))

cert = response.cookies['MicexPassportCert']
```

### Формирование url-запроса для акций

* Префикс url системы: `http://iss.moex.com/`
* Пространстов имен для данных итогов торгов: `/iss/history`

Формат, в котором необходимо получить данные, указывается в конце основной части URL через точку.

Например:

`http://iss.moex.com/iss/history/engines/stock/markets/shares/boards/tqbr/securities.json?date=2013-12-20`

Поддерживаются следующие форматы: XML, CSV, JSON, HTML


### [Описание метаданных](https://iss.moex.com/iss/index)

* engines - 
* markets -
* boards - 
* securities - 
* boardgroups - 
* durations - 
* securitytypes - 
* securitygroups - 
* securitycollections - 

 HFT traders - high frequency traider - высокочастотны трейдер