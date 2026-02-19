from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"

DATABASE = "blog.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    conn = get_db()
    posts = conn.execute("""
        SELECT posts.*, users.username
        FROM posts
        JOIN users ON posts.user_id = users.id
    """).fetchall()
    conn.close()
    return render_template("index.html", posts=posts)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        try:
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            conn.commit()
            return redirect("/login")
        except:
            return "Username already exists"
        finally:
            conn.close()

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        ).fetchone()
        conn.close()

        if user:
            session["user_id"] = user["id"]
            return redirect("/")
        else:
            return "Invalid credentials"

    return render_template("login.html")


@app.route("/create", methods=["GET", "POST"])
def create():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        conn = get_db()
        conn.execute(
            "INSERT INTO posts (title, content, user_id) VALUES (?, ?, ?)",
            (title, content, session["user_id"])
        )
        conn.commit()
        conn.close()
        return redirect("/")

    return render_template("create.html")


# ---------- UPDATE (EDIT) ----------
@app.route("/edit/<int:post_id>", methods=["GET", "POST"])
def edit(post_id):
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()
    post = conn.execute(
        "SELECT * FROM posts WHERE id=?",
        (post_id,)
    ).fetchone()

    if not post:
        conn.close()
        return "Post not found"

    if post["user_id"] != session["user_id"]:
        conn.close()
        return "Unauthorized"

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        conn.execute(
            "UPDATE posts SET title=?, content=? WHERE id=?",
            (title, content, post_id)
        )
        conn.commit()
        conn.close()
        return redirect("/")

    conn.close()
    return render_template("edit.html", post=post)


# ---------- DELETE ----------
@app.route("/delete/<int:post_id>")
def delete(post_id):
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()
    post = conn.execute(
        "SELECT * FROM posts WHERE id=?",
        (post_id,)
    ).fetchone()

    if not post:
        conn.close()
        return "Post not found"

    if post["user_id"] != session["user_id"]:
        conn.close()
        return "Unauthorized"

    conn.execute("DELETE FROM posts WHERE id=?", (post_id,))
    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
