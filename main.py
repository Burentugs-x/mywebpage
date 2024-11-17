import sqlite3
import hashlib
from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Ensure you set this for session to work

@app.route('/')
def hello_world():
    return render_template('index.html', message='Hello, World!')

@app.route('/about')
def about():
    name = "Burentugs"
    age = 15
    print(name, age)
    return render_template('about.html',
                            my_title=name,
                            my_hobby=age
                            )

@app.route('/form', methods=['GET', 'POST'])
def render_form():
    message = ''
    if request.method == 'POST':
        text = request.form.get('text')
        if request.form['submit_button'] == 'Lowercase':
            message = text.lower()
        elif request.form['submit_button'] == 'Capital':
            message = text.upper()
        elif request.form['submit_button'] == 'Byamba':
            message = "Hi Byamba"
    return render_template('form.html', message=message)

@app.route('/me', methods=['GET', 'POST'])
def about_me():
    message = ""
    if request.method == 'POST':
        name_insert = request.form['name']
        age_insert = request.form['age']
        hobby_insert = request.form['hobby']
        project_insert = request.form['project']

        conn = sqlite3.connect('titanic.sqlite')
        cursor = conn.cursor()

        # Ensure the me table exists (you might want to modify or remove this part)
        cursor.execute('''CREATE TABLE IF NOT EXISTS contacts ( id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT NOT NULL, message TEXT NOT NULL, db_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

        # Insert the submitted form data into the me table
        cursor.execute("INSERT INTO me (name, age, hobby, project) VALUES (?, ?, ?, ?)", (name_insert, age_insert, hobby_insert, project_insert))
        conn.commit()
        conn.close()

        message = "Post submitted successfully!"
    return render_template('burentugs.html', message=message)

@app.route('/posts', methods=['GET', 'POST'])
def submit_post():
    message = ""
    if request.method == 'POST':
        title = request.form['title']
        post_content = request.form['post']
        post_type = request.form['type']

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS post (id INTEGER PRIMARY KEY, title TEXT, post TEXT, type TEXT)''')

        cursor.execute("INSERT INTO post (title, post, type) VALUES (?, ?, ?)", (title, post_content, post_type))
        conn.commit()
        conn.close()

        message = "Post submitted successfully!"
    return render_template('form.html', message=message)

@app.route('/admin')
def show_blogs():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch all posts from the database
    cursor.execute("SELECT title, post, type FROM contact")
    posts = cursor.fetchall()
    conn.close()

    # Format posts for rendering
    format_contacts = [{"name": row[0], "email": row[1], "messages": row[2]} for row in posts]

    return render_template('blog.html', posts=format_contacts)

@app.route('/blogs')
def show_blogs():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch all posts from the database
    cursor.execute("SELECT title, post, type FROM post")
    posts = cursor.fetchall()
    conn.close()

    # Format posts for rendering
    formatted_posts = [{"title": row[0], "content": row[1], "type": row[2]} for row in posts]

    return render_template('blog.html', posts=formatted_posts)

@app.route('/me', methods=['GET', 'POST'])
def about_me():
    message = ""
    if request.method == 'POST':
        name_insert = request.form['name']
        age_insert = request.form['age']
        hobby_insert = request.form['hobby']
        project_insert = request.form['project']

        conn = sqlite3.connect('titanic.sqlite')
        cursor = conn.cursor()

        # Ensure the me table exists (you might want to modify or remove this part)
        cursor.execute('''CREATE TABLE IF NOT EXISTS contacts ( id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT NOT NULL, message TEXT NOT NULL, db_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

        # Insert the submitted form data into the me table
        cursor.execute("INSERT INTO me (name, age, hobby, project) VALUES (?, ?, ?, ?)", (name_insert, age_insert, hobby_insert, project_insert))
        conn.commit()
        conn.close()

        message = "Post submitted successfully!"
    return render_template('grace.html', message=message)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            flash("Registration successful! Please log in.")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Username already exists. Please try another one.")
        finally:
            conn.close()
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['username'] = username
            flash("Login successful!")
            return redirect(url_for('show_blogs'))
        else:
            flash("Invalid username or password.")

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)