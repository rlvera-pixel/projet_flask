from flask import Flask, request, render_template, make_response, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__, 
            static_folder='static',
            template_folder='app/templates')

# Clé secrète pour les sessions et flash messages
app.secret_key = 'comprendeshi_secret_key_2024'

# Dossier pour les uploads
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello/<name>')
def hello_name(name):
    return f'Hello {name}!'

# --- COOKIES ---
@app.route('/setcookie', methods=['POST', 'GET'])
def setcookie():
    if request.method == 'POST':
        user = request.form['nm']
        resp = make_response(render_template('cookie.html'))
        resp.set_cookie('userID', user)
        return resp

@app.route('/getcookie')
def getcookie():
    name = request.cookies.get('userID')
    return f'<h1>Welcome {name}!</h1>'

# --- FILE UPLOAD ---
@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/uploader', methods=['POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
        f.save(filepath)
        flash(f'File {f.filename} uploaded successfully!', 'success')
        return redirect(url_for('upload'))

# --- STUDENT FORM ---
@app.route('/student')
def student():
    return render_template('student.html')

@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        result = request.form
        return render_template('result.html', result=result)

# --- SESSIONS & LOGIN ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid username or password. Please try again!'
        else:
            session['logged_in'] = True
            session['username'] = request.form['username']
            flash('You were successfully logged in!', 'success')
            return redirect(url_for('dashboard'))
    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        flash('Please login first!', 'error')
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session.get('username'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('You were logged out!', 'info')
    return redirect(url_for('index'))

# --- URL BUILDING & REDIRECT ---
@app.route('/admin')
def hello_admin():
    return 'Hello Admin!'

@app.route('/guest/<guest>')
def hello_guest(guest):
    return f'Hello {guest} as Guest!'

@app.route('/user/<name>')
def hello_user(name):
    if name == 'admin':
        return redirect(url_for('hello_admin'))
    else:
        return redirect(url_for('hello_guest', guest=name))

if __name__ == '__main__':
    app.run(debug=True)