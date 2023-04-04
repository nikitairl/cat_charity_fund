
# QRCat - приложение для сбора средств на нужды котиков.
![Cat](cat.jpg)

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FASTAPI](https://img.shields.io/badge/Fastapi-37762B?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3771AB?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/index.html)
## О проекте
Этот асинхронный проект - сервис для сбора средств на различные целевые проекты, связанные с поддержкой котиков. Администратор добавляет новые проекты пожертвований, а зарегистрированные пользователи могут просто вносить свои средства, которые будут автоматически распределены в наиболее ранние проекты.

Информация о пожертвованиях и проектах сохраняется в базу данных SQLite, реализована система авторизации пользователей.

## Запуск
### В корневой директории проекта:
1. создать .env файл с необходимыми переменными:
- SECRET = 'Ваше секретное слово'
- DATABASE_URL = 'sqlite+aiosqlite:///./fastapi.db' по умолчанию.
```
python3 -m venv venv
```
Windows:
```
. source venv/Scripts/activate
```
Mac:
```
. source venv/bin/activate
```
```
pip install -r requirements.txt
```
Для запуска приложения:
```
uvicorn app.home:app
```
