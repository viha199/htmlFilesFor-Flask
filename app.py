from flask import Flask, render_template,request
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")
connect = sqlite3.connect('database.db')
connect.execute( 'CREATE TABLE IF NOT EXISTS participants ( name TEXT, email TEXT, city TEXT, country TEXT, phone TEXT )' )


@app.route('/join', methods=['GET', 'POST'] )
def join():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        city = request.form['city']
        country = request.form['country']
        phone = request.form['phone']
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO participants (name, email, city, country, phone) VALUES (?, ?, ?, ?, ?)", (name, email, city, country, phone))
        conn.commit()
        conn.close()
        
        return render_template("index.html")
    return render_template("join.html")

@app.route('/participants')
def participants():
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM participants")
    data = cursor.fetchall()
    return render_template("participants.html",data=data)

if __name__ == "__main__":
    app.run(port=5000)
