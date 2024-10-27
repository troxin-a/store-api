# Store API (Сервис покупки товаров для авторизованных пользователей)

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-lightgreen)
![SQLalchemy](https://img.shields.io/badge/SQLalchemy-2.0-red)
![alembic](https://img.shields.io/badge/Alembic-1.13-red)
![pyjwt](https://img.shields.io/badge/Pyjwt-2.9-yellow)

## 🛒 О проекте:
Backend-часть удобного и безопасного сервиса, который позволяет пользователям регистрироваться, авторизовываться и просматривать список доступных товаров.<br>
Авторизованные пользователи могут добавлять товары в корзину и управлять ею.<br>
Администратор сайта может управлять товарами: создавать новые, редактировать и удалять.


## 🛠️ Установка

1. **Клонируйте репозиторий:**

```bash
git clone https://github.com/troxin-a/store-api.git
cd store-api
```

2. **Создайте файл .env в корневом каталоге проекта и добавьте необходимые переменные окружения:**

```bash
cp .env.sample .env
nano .env
```

3. **Запустите сервер**

```bash
make up
```

4. **Примените миграции:**

```bash
make migrate
```

4. **Создайте администратора**

```bash
make csu
```

## 📚️ Документация
Документация по использованию API будет доступна после запуска сервера по ссылке: http://127.0.0.1:8000/docs/

**Если необходимо потушить сервер:**

```bash
make down
```


