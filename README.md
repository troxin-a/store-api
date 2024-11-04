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


## Структура проекта
```bash
FastAPI-project
├── src/
│   ├── api
│   │   ├── base.py
│   │   ├── cart.py
│   │   ├── product.py
│   │   └── user.py
│   ├── config
│   │   ├── db.py
│   │   └── settings.py
│   ├── migrations
│   │   ├── versions
│   │   │   ├── 9b24f25e85da_init.py
│   │   │   └── 4352eef4cc3a_ondelete_cascade_for_tables.py
│   │   ├── env.py
│   │   └── script.py.mako
│   ├── models
│   │   ├── cart_product.py
│   │   ├── cart.py
│   │   ├── product.py
│   │   └── users.py
│   ├── schemas
│   │   ├── cart.py
│   │   ├── product.py
│   │   └── users.py
│   ├── services
│   │   ├── cart.py
│   │   ├── create_admin.py
│   │   ├── product.py
│   │   └── users.py
│   └── main.py
├── tests
│   ├── conftest.py
│   ├── test_cnonymous.py
│   ├── test_auth.py
│   ├── test_cart.py
│   └── test_product.py
├── .dockerignore
├── .env
├── alembic.ini
├── docker-compose.yaml
├── Dockerfile
├── Makefile
├── poetry.lock
└── pyproject.toml
```


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

3. **Тестирование приложения:**
```bash
poetry shell
poetry install
pytest
```

4. **Запустите сервер**

```bash
make up
```

5. **Примените миграции:**

```bash
make migrate
```

6. **Создайте администратора**

```bash
make csu
```

## 📚️ Документация
Документация по использованию API будет доступна после запуска сервера по ссылке: http://127.0.0.1:8000/docs/

**Остановить и удалить контейнеры:**

```bash
make down
```


