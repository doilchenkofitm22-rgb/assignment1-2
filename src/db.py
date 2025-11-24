
import sqlite3
import os
import pathlib

DB_PATH = os.environ.get("DB_PATH", "demo.sqlite3")

# видаляємо стару базу, якщо є
pathlib.Path(DB_PATH).unlink(missing_ok=True)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript(
    """
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL  -- зберігання у відкритому вигляді для демо
    );

    CREATE TABLE posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        body TEXT NOT NULL
    );

    INSERT INTO users(username, password) VALUES
        ("dima", "dima123"),
        ("max", "max12345");

    INSERT INTO posts(title, body) VALUES
        ("Ласкаво просимо", "Це демо‑стаття."),
        ("Поради щодо безпеки", "Ніколи не довіряйте введеним даним. Використовуйте параметризовані запити.");
    """
)

conn.commit()
conn.close()
print(f"Initialized SQLite DB at {DB_PATH}")