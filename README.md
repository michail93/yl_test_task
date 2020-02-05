###Описание 

####Запуск приложения
* Приложение запускается так:
```
docker-compose build
docker-compose up
```
* Приложение работает на localhost на порту 8000:
```
127.0.0.1:8000
```

####Аутентификация
  Приложение использует [Basic Authentication](https://en.wikipedia.org/wiki/Basic_access_authentication). Пользователи 
  аутентифицируются при помощи HTTP заголовка Authorization.

```
Authorization: Basic <credentials>
```


* Значение для credentials : 
 ```python
import base64

email = "example@mail.com"
password=1234

credentials = base64.b64encode(f"{email}:{password}".encode()).decode('ascii')

print(credentials) # ZXhhbXBsZUBtYWlsLmNvbToxMjM0

```
или
```bash
echo -n "example@mail.com:1234" | base64 && echo

ZXhhbXBsZUBtYWlsLmNvbToxMjM0
```
* Итоговый заголовок:
```
Authorization: Basic ZXhhbXBsZUBtYWlsLmNvbToxMjM0
```

#### Cоздание пользователя
Cоздание пользователя доступно для неаутентифицированных пользователей и происходит методом POST по этому URL:
```
/money-transfer/create-user/
```
с таким JSON:
```javascript
{
    "email": "example@mail.com",
    "balance": 126,
    "currency": "RUB",
    "password": "1234"
}

поле currency должно быть одно из "EUR", "USD", "GBP", "RUB", "BTC".
поле "balance" - первоначальный баланс пользователя.
```

#### Перевод средств
Перевод стредств доступен только для аутентифицированных пользователей(с использованием заголовка Authorization) и 
происходит методом POST по этому URL:
```
/money-transfer/transfer-money/
```
с таким JSON 
```javascript
{
    "transaction_email": "to_user@mail.com",
    "amount": 10.14
}

поле "transaction_email" - email пользователя которому переводятся деньги.
поле "amount" - сумма для перевода.
```

#### Просмотр списка всех операций на своем счету.
Просмотр списка всех операций на своем счету доступен только для аутентифицированных пользователей
(с использованием заголовка Authorization) и происходит методом GET по этому URL:
```
/money-transfer/get-info/
```
#### Базовая валюта 
В качестве базовой валюты был выбран российский рубль(RUB) - переменная BASE_CURRENCY в settings.py.