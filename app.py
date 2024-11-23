from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def create_connection():
    con = sqlite3.connect("newreaders.db")
    return con

def create_table():
    con = create_connection()
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS newuser(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, username TEXT, password TEXT)""")
    con.commit()
    con.close()
    return redirect("/feedback")

@app.route("/admin")
def admin():
    con=create_connection()
    cur=con.cursor()
    cur.execute('SELECT* FROM newuser')
    data= cur.fetchall()
    return render_template('admin.html', users=data)
    print(data)

@app.route("/")
def home():
    return render_template("homepage.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name= request.form.get("name")
        email= request.form.get("email")
        con= create_connection()
        cur= con.cursor()
        cur.execute('''INSERT INTO newuser(name, email) VALUES(?, ?)''', (name, email))
        user = cur.fetchone()
        con.commit()
        cur.close()
        print(f"Received: Name={name}, Email={email}")
        return redirect('/feedback')
    return render_template("loginpage.html")

@app.route("/registration", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        name= request.form.get("name")
        email= request.form.get("email")
        con= create_connection()
        cur= con.cursor()
        cur.execute('''INSERT INTO newuser(name, email, username, password) VALUES(?, ?, ?, ?)''', (name, email, username, password))
        con.commit()
        cur.close()
        print(f"Received: Name: {name}, Email= {email}, Username={username}, Password={password}")
        return redirect('/feedback')
    return render_template("registrationpage.html")

@app.route("/feedback")
def feedback():
    return render_template("feedback.html")

if __name__ == "__main__":
    create_connection()
    create_table()
    app.run(debug=True)
