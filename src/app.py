 from flask import Flask, request, render_template, redirect, make_response, session
import os
import sqlite3

 
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "hardcoded-dev-secret")  # слабкий секрет для демо

DB_PATH = os.environ.get("DB_PATH", "demo.sqlite3")


def get_db():
    """Повертає нове зʼєднання з базою даних."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    """Домашня сторінка."""
    return render_template("index.html")


@app.route("/echo")
def echo():
    """Уразлива до відображеної XSS сторінка."""
    msg = request.args.get("msg", "")
    # ненадійне відображення параметра без екранування
    return f"<h1>Echo</h1><p>{msg}</p>"


@app.route("/search")
def search():
    """Уразливий пошук із SQL‑інʼєкцією."""
    q = request.args.get("q", "")
    conn = get_db()
    cur = conn.cursor()
    
    sql = f"SELECT id, title, body FROM posts WHERE title LIKE '%{q}%' OR body LIKE '%{q}%'"
    rows = cur.execute(sql).fetchall()
    return render_template("search.html", q=q, rows=rows, sql=sql)


@app.route("/login", methods=["GET", "POST"])
def login():
 
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        conn = get_db()
        cur = conn.cursor()
        # паролі зберігаються у відкритому вигляді (навмисно)
        row = cur.execute("SELECT id, username, password FROM users WHERE username = ?", (username,)).fetchone()
        if row and row["password"] == password:
            session["user_id"] = row["id"]
            resp = make_response(redirect("/profile"))
            return resp
        return render_template("login.html", error="Невірні облікові дані")
    return render_template("login.html")


@app.route("/profile")
def profile():
    """Профіль користувача. Доступний лише після входу."""
    if "user_id" not in session:
        return redirect("/login")
    conn = get_db()
    cur = conn.cursor()
    user = cur.execute("SELECT id, username FROM users WHERE id = ?", (session["user_id"],)).fetchone()
    return render_template("profile.html", user=user)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)