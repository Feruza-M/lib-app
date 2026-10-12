# Library API

Простое REST API для проекта «Библиотека».

Приложение написано на Python с FastAPI и SQLAlchemy, данные хранятся в MariaDB.  
Оно позволяет управлять авторами, книгами, читателями и выдачами книг.

## Возможности

- Создание и получение списка авторов
- Создание и получение списка книг
- Создание и получение списка читателей
- Выдача книги читателю
- Возврат книги
- Автоматическое уменьшение и увеличение количества доступных экземпляров
- Проверка доступности книги и активности читателя
- Health check endpoint: `GET /health`

## Настройка MariaDB

```bash
sudo mariadb
```

```sql
CREATE DATABASE IF NOT EXISTS library_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'library_app'@'localhost'
  IDENTIFIED BY 'CHANGE_ME_STRONG_PASSWORD';

GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, INDEX, REFERENCES
  ON library_db.*
  TO 'library_app'@'localhost';

FLUSH PRIVILEGES;
```

## Примеры запросов

### Создать автора

```bash
curl -X POST http://127.0.0.1:8000/authors \
  -H "Content-Type: application/json" \
  -d '{"name": "Andy Weir"}'
```

### Создать книгу

```bash
curl -X POST http://127.0.0.1:8000/books \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Project Hail Mary",
    "isbn": "9780593135204",
    "total_copies": 3,
    "author_id": 1
  }'
```

### Создать читателя

```bash
curl -X POST http://127.0.0.1:8000/readers \
  -H "Content-Type: application/json" \
  -d '{"full_name": "Ivan Ivanov", "email": "ivan@example.com"}'
```

### Выдать книгу

```bash
curl -X POST http://127.0.0.1:8000/loans \
  -H "Content-Type: application/json" \
  -d '{"book_id": 1, "reader_id": 1, "days": 14}'
```

### Вернуть книгу

```bash
curl -X POST http://127.0.0.1:8000/loans/1/return
```
