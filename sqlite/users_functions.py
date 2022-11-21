import sqlite3

def show_all():
	conn = sqlite3.connect('users.db')
	c = conn.cursor()
	c.execute("SELECT rowid, * FROM users")
	users = c.fetchall()
	for user in users:
		print(user)
	conn.commit()
	conn.close()

def add_one(username, password):
	conn = sqlite3.connect('users.db')
	c = conn.cursor()
	c.execute("INSERT INTO users VALUES (?,?)", (username, password))
	conn.commit()
	conn.close()

def delete_one(id):
	conn = sqlite3.connect('users.db')
	c = conn.cursor()
	c.execute("DELETE from users WHERE rowid = (?)", id)
	conn.commit()
	conn.close()