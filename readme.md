1. Установить PostgreSQL
2. Создать базу данных:

CREATE DATABASE incidents_db;

3. Обновить настройки подключения в `.env` файле

## Запуск приложения

uvicorn main:app --reload
