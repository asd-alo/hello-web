from flask import Flask，request
import pymysql
import os
import time

app = Flask(__name__)

DB_HOST = os.environ.get("DB_HOST", "db")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "123456")
DB_NAME = os.environ.get("DB_NAME", "hello")

def get_conn():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4",
    )

def init_db():
    for i in range(30):
        try:
            conn = get_conn()
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS messages (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        content VARCHAR(500) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
            conn.commit()
            conn.close()
            return
        except Exception as e:
            print("等待数据库启动...", i, e)
            time.sleep(2)
    raise RuntimeError("数据库连不上")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        content = request.form.get("content", "").strip()
        if content:
            conn = get_conn()
            with conn.cursor() as cur:
                cur.execute("INSERT INTO messages (content) VALUES (%s)", (content,))
            conn.commit()
            conn.close()

    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute("SELECT id, content, created_at FROM messages ORDER BY id DESC")
        messages = cur.fetchall()
    conn.close()

    html = "<h1>我的留言板</h1>"
    html += '<form method="post"><input name="content" placeholder="说点什么..." required>'
    html += '<button type="submit">留言</button></form><hr>'
    for m in messages:
        html += "<p>[" + str(m[2]) + "] " + m[1] + "</p>"
    return html

init_db()

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)