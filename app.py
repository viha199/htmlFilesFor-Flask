from flask import Flask, render_template,request,redirect,url_for
from werkzeug.security import generate_password_hash,check_password_hash
import sqlite3 

from flask_login import(
    LoginManager,login_user,logout_user,login_required,UserMixin,current_user
)

app = Flask(__name__)
app.secret_key="super-secret-key"

def get_db():
    conn=sqlite3.connect("database.db")
    conn.row_factory=sqlite3
    return conn

db=get_db()
db.execute("""
    CREATE TABLE IF NOT EXISTS USERS(email TEXT PRIMARY KEY, password TEXT NOT NULL)
""")

db.execute("""CREATE TABLE IF NOT EXISTS PARTICIPANTS(
           name TEXT,
           email TEXT,
           city TEXT,
           country TEXT,
           phone TEXT)""")
db.commit()
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view="login"

class User(UserMixin):
    def __init__(self,email):
        self.id=email

@login_manager.user_loader
def load_user(user_id):
    db=get_db()
    user=db.execute(
        "SELECT email FROM USERS WHERE email=?",
        (user_id)
    ).fetchone()
    return User(user["email"]) if user else None
@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html")

connect=sqlite3.connect('database.db')
connect.execute(
    'CREATE TABLE IF NOT EXISTS PARTICIPANTS(name TEXT,email TEXT,city TEXT,country TEXT,phone TEXT)'
)

@app.route("/join",methods=['GET','POST'])

def join():
    if request.method=='POST':
        name=request.form["name"]
        email=request.form["email"]
        city=request.form["city"]
        country=request.form["country"]
        phone=request.form["phone"]
        with sqlite3.connect("database.db") as users:
            cursor=users.cursor()
            cursor.execute("INSERT INTO PARTICIPANTS" \
            "(name,email,city,country,phone) VALUES" \
            "(?,?,?,?,?)",(name,email,city,country,phone))
            users.commit()
        return render_template("index.html")
    return render_template("join.html")

@app.route("/participants")
def participants():
    connect=sqlite3.connect('database.db')
    curser=connect.cursor()
    curser.execute('SELECT*FROM PARTICIPANTS')
    data=curser.fetchall()

    return render_template("participants.html",data=data)

if __name__ == '__main__':
    app.run(debug=False)
