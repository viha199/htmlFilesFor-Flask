from flask import Flask, render_template, request, redirect, url_for
import sqlite3 
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_login import LoginManager, login_user, logout_user, current_user, login_required, UserMixin

app = Flask(__name__)
app.secret_key = 'secretKey'

db = sqlite3.connect('database.db', check_same_thread=False)
db.row_factory = sqlite3.Row
cursor = db.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS USERS (email TEXT PRIMARY KEY, password TEXT NOT NULL)')
cursor.execute('CREATE TABLE IF NOT EXISTS PARTICIPANTS (name TEXT, email TEXT, city TEXT, country TEXT, phone TEXT)')
db.commit()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, email):
        self.id = email

@login_manager.user_loader
def load_user(user_id):
    user = cursor.execute('SELECT * FROM USERS WHERE email = ?', (user_id,)).fetchone()
    if user:
        return User(user['email'])
    else:
        None 

@app.route('/')
def root():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    else:
        return render_template("login.html")

@app.route('/signup', methods = ['GET','POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']
        
        if password != confirmPassword:
            return render_template('signup.html', errorMessage = 'Passwords do not match.')

        hashed_password = generate_password_hash(password)
        existing_user = cursor.execute('SELECT 1 FROM USERS WHERE email = ?', (email,)).fetchone()
        
        if existing_user:
            return render_template('signup.html', errorMessage = 'User already exists.')
        else:
            cursor.execute('INSERT INTO USERS (email, password) VALUES (?,?)', (email, hashed_password))
            db.commit()
            return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = cursor.execute('SELECT * FROM USERS WHERE email = ?', (email,)).fetchone()
        if user and check_password_hash(user['password'], password):
            login_user(User(user['email']))
            return redirect(url_for('index'))
        else:
            return render_template('login.html', errorMessage = 'Invalid credentials.')
    return render_template('login.html')

@app.route('/index')
@login_required
def index():
    return render_template('index.html')

@app.route('/join', methods = ['GET', 'POST'])
@login_required
def join():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        city = request.form['city']
        country = request.form['country']
        phone = request.form['phone']

        cursor.execute('INSERT INTO PARTICIPANTS (name, email, city, country, phone) VALUES (?, ?, ?, ?, ?)', (name, email, city, country, phone))
        db.commit()
        return redirect(url_for('participants'))
    
    return render_template('join.html')

@app.route('/participants')
@login_required 
def participants():
    data = cursor.execute('SELECT * FROM PARTICIPANTS').fetchall()
    return render_template('participants.html', data=data)

@app.route('/logout')
@login_required 
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
