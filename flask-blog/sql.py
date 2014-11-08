#sql.py --> Create a sqllite table and populate with data
import sqlite3
with sqlite3.connect("blog.db") as connection:
	c = connection.cursor()
	c.execute("DROP TABLE if exists posts")
	c.execute("""CREATE TABLE posts
			(title TEXT, post TEXT)""")
	#insert some dummy data for testing
	c.execute('INSERT INTO posts values ("Good" , "I\'m good.")')
	c.execute('INSERT INTO posts values ("Well" , "I\'m Well.")')
	c.execute('INSERT INTO posts values ("Excellent" , "I\'m Excellent.")')
	c.execute('INSERT INTO posts values ("Ok" , "I\'m Ok.")')
