import sqlite3


#conn = sqlite3.connect('food.db')
#c = conn.cursor()
#c.execute("""CREATE TABLE food (
#			Meal text,
#			Calories int,
#			Fat int,
#			Carb int,
#			Category text,
#			Meat bool,
#			Dairy bool,
#			Recipe_Link varchar(2083)
#		)""")
#conn.commit()
#conn.close()


def show_all():
	conn = sqlite3.connect('food.db')
	c = conn.cursor()
	c.execute("SELECT rowid, * FROM food")
	foods = c.fetchall()
	for food in foods:
		print(food)
	conn.commit()
	conn.close()

def add_one(Meal, Calories, Fat, Carb, Category, Meat, Dairy, Recipe_Link):
	conn = sqlite3.connect('food.db')
	c = conn.cursor()
	c.execute("INSERT INTO food VALUES (?,?,?,?,?,?,?,?)", (Meal, Calories, Fat, Carb, Category, Meat, Dairy, Recipe_Link))
	conn.commit()
	conn.close()

def delete_one(id):
	conn = sqlite3.connect('food.db')
	c = conn.cursor()
	c.execute("DELETE from food WHERE rowid = (?)", id)
	conn.commit()
	conn.close()