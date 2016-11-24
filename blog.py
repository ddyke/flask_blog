# blog.py: Controller

#imports

from flask import Flask, render_template, request, session, flash, redirect, url_for, g
import sqlite3
from functools import wraps


# configure
DATABASE = "blog.db"
app = Flask(__name__)
USERNAME = 'admin'
PASSWORD = 'admin'
SECRET_KEY = 'himitsu'

# pulls in app configuration by looking for UPPERCASE variables
app.config.from_object(__name__)

# for connecting to the database
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args,**kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login'))
    return wrap

# return login template to the server
@app.route('/', methods = ['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or \
                        request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            return redirect(url_for('main'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))


# return main template to the server
@app.route('/main')
@login_required
def main():
    g.db = connect_db()         # connect to the database
    cur = g.db.execute('select * from posts')       # retrieve all data from the db
    posts = [dict(title=row[0], post=row[1]) for row in cur.fetchall()]     # fetch & convert data into a dictionary
    g.db.close()
    return render_template('main.html', posts=posts)

# add blog content
@app.route('/add', methods=['POST'])
@login_required
def add():
    title = request.form['title']
    post = request.form['post']
    if not title or not post:
        flash("All fields are required. Please try again.")
    else:
        g.db = connect_db()
        cur = g.db.execute('insert into posts (title, post) values (?, ?)',
                           [request.form['title'], request.form['post']])
        g.db.commit()
        g.db.close()
        flash('New entry was successfully posted!')
        return redirect(url_for('main'))

if __name__ == '__main__':
    app.run(debug=True)
