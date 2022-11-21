from flask import Flask
import sqlite3
from flask import g
from random import shuffle

# Name of database
Database = 'sqlite/food.db'

def get_db():
    db =getattr(g, '_database', None)
    if db is None:
        db = g.database = sqlite3.connect(Database)
    return db

# @app.teardown_appcontent
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def select_food(calories):
    conn = sqlite3.connect(Database)
    c = conn.cursor()
    c.execute("SELECT * FROM food")
    foods = c.fetchall()
    conn.commit()
    conn.close()
    shuffle(foods)
    for food in foods:
        food_cals = food[1]
        if food_cals <= calories:
            return food
    return -1


select_food(150)