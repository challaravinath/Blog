#blog.py -->Controller
#imports
from flask import Flask,render_template,request,session,flash,redirect,url_for,g
import sqlite3
import os
from functools import wraps

#configuration
DATABASE = 'blog.db'
USERNAME = 'admin'
PASSWORD = 'admin'
SECRET_KEY = os.urandom(24)
app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def login_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return test(*args, **kwargs)
		else:
			flash('You need to log in first!')
			return (url_for('login'))
	return wrap

@app.route('/' , methods = ['GET' , 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid credentials, Plz try again' 	
		else:
			session['logged_in'] = True
			#url_for end point for the method
			return redirect(url_for('main'))
	return render_template('login.html' , error = error)
@app.route('/logout')
def logout():
	session.pop('logged_in' , None)
	flash('You are logged out')
	return redirect(url_for('login'))

@app.route('/add', methods = ['POST'])
@login_required
def add():
	title = request.form['title']
	post = request.form['post']
	if not title or not post:
		flash('All feilds are required .Plz try again')
		return redirect(url_for('main'))
	else:
		g.db = connect_db()
		g.db.execute('insert into posts (title, post) values(?,?)' , [request.form['title'], request.form['post']])
		g.db.commit()
		g.db.close()
		flash('New entry was successfully posted!')
		return redirect(url_for('main'))

@app.route('/main')
@login_required
def main():
	g.db = connect_db()
	cur = g.db.execute('select * from posts')
	posts = [dict(title=row[0], post=row[1]) for row in cur.fetchall()]
	g.db.close()
	return render_template('main.html')
if __name__ =='__main__':
	app.run(debug=True)



