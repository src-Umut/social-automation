from flask import Flask , render_template , request , redirect , url_for
from config import DB_PATH
import sqlite3
app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.row
    return conn 

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return render_template("index.html")
@app.route("/about")
def about():
    return "<h2>About Page</h2>"

@app.route("/new" , methods = ["GET" , "POST"])
def new_post():
    if request.method == "POST":
        title = request.form["title"]
        content =  request.form["content"]
        conn = get_db_connection
        conn.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))
        conn.commit()
        conn.close()
        return redirect(url_for("home"))
    return render_template("new_post.html")



if __name__ == "__main__":
    app.run(debug=True)




