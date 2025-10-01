from flask import Flask , render_template , request , redirect , url_for
from config import DB_PATH
import sqlite3
app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
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
    conn = get_db_connection()
    posts = conn.execute("SELECT * FROM posts ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("index.html", posts = posts)
@app.route("/about")
def about():
    return "<h2>About Page</h2>"

@app.route("/new" , methods = ["GET" , "POST"])
def new_post():

    error = None
    if request.method == "POST":
        title = request.form["title"]
        content =  request.form["content"]

        if not title or not content:
            error = "Title and Content are required!"
        else: 
            try:
                conn = get_db_connection()
                conn.execute("INSERT INTO posts (title , content) VALUES (? , ? )" , (title , content))
                conn.commit()
                conn.close()
                return redirect(url_for("home"))
            except Exception as e:
                error = f"database error {e}"
                
    return render_template("new_post.html" , error = error)



if __name__ == "__main__":
    app.run(debug=True)




