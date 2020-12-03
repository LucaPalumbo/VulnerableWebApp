from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3

app = Flask(__name__)

app.secret_key = b'this_is_a_really_secure_password_isnt_it?'

@app.route('/home', methods=['POST', 'GET'])
def home():
    if 'username' in session:
        
        conn = sqlite3.connect('db/data.db')
        c = conn.cursor()
        query = "SELECT id,titolo, testo FROM Note WHERE id_utente=?"
        c.execute(query, ( str(session['id']) ))
        rows = c.fetchall()

        return render_template('home.html', username = session['username'], email = session['email'], NoteList = rows)
    else:
        return redirect(url_for("index"))

@app.route('/addNote', methods=['POST', 'GET'])
def addNote():
    if request.method == 'POST':
        title = request.form['title']
        notetext = request.form['notetext']
        conn = sqlite3.connect('db/data.db')
        c = conn.cursor()
        query = "INSERT INTO Note (id_utente, titolo, testo) VALUES (?,?,?);"
        c.execute(query, (session['id'], title, notetext ))
        conn.commit()
        return redirect(url_for("home"))
    elif request.method == 'GET':
        return render_template('addNote.html')


@app.route('/shareNote/<id>')
def shareNote(id = None):
    conn = sqlite3.connect('db/data.db')
    c = conn.cursor()
    query = "SELECT * FROM Note WHERE id=?"
    c.execute(query, ( id  ))
    row = c.fetchone()
    return str(row)


    
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/', methods=['POST', 'GET'])
def index():
    if 'username' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('db/data.db')
        c = conn.cursor()
        query = "SELECT email FROM Utenti WHERE email='%s';"
        c.execute(query % email)
        rows = c.fetchone()
        if( rows is not None ):
            return "email already used. Use a different one."

        query = "INSERT INTO Utenti (username, email, password) VALUES ('%s', '%s', '%s');"
        c.execute(query % (username, email, password))
        conn.commit()
        return redirect(url_for("login"))

    elif request.method == 'GET':
        return render_template('register.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('db/data.db')
        c = conn.cursor()
        query = "SELECT id,username FROM Utenti WHERE email='%s' and (password='%s') ;"
        c.execute(query % (email, password))
        rows = c.fetchone()
        if( rows is not None):
            session['username'] = rows[1]
            session['email'] = email
            session['id'] = rows[0]

            return redirect(url_for('index'))
        else:
                return "Access denied"

    elif request.method == 'GET':
        return render_template('login.html')

