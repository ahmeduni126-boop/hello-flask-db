import os
import psycopg2
from flask import Flask, render_template_string, request

app = Flask(__name__)
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS ziyaretciler (id SERIAL PRIMARY KEY, isim TEXT NOT NULL);")
    conn.commit()
    cur.close()
    conn.close()

HTML_SABLON = """
<!doctype html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <title>Buluttan Selam!</title>
  <style>
    body { font-family: sans-serif; text-align: center; padding: 50px; background: #f4f7f6; }
    .container { background: white; padding: 30px; border-radius: 12px; display: inline-block; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
    input { padding: 10px; border-radius: 5px; border: 1px solid #ddd; }
    button { padding: 10px 20px; background: #3498db; color: white; border: none; border-radius: 6px; cursor: pointer; }
    li { background: #ecf0f1; margin: 5px auto; width: 200px; padding: 10px; border-radius: 6px; list-style: none; }
  </style>
</head>
<body>
  <div class="container">
    <h1>Buluttan Selam! ☁️</h1>
    <form method="POST">
      <input type="text" name="isim" placeholder="Adınız" required>
      <button type="submit">Gönder</button>
    </form>
    <h3>Ziyaretçiler</h3>
    <ul>{% for ad in isimler %}<li>{{ ad }}</li>{% endfor %}</ul>
  </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == "POST":
        gelen_isim = request.form.get("isim")
        if gelen_isim:
            cur.execute("INSERT INTO ziyaretciler (isim) VALUES (%s)", (gelen_isim,))
            conn.commit()
    cur.execute("SELECT isim FROM ziyaretciler ORDER BY id DESC LIMIT 5")
    isimler = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return render_template_string(HTML_SABLON, isimler=isimler)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
