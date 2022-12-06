from flask import Flask, render_template, request, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import requests
import json
import sqlite3
from random import shuffle

#Flask Instance
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.config['SECRET_KEY'] = 'thisisasecretkey'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    remainingCalorieIntake = db.Column(db.Integer)
    weeklyCalorieIntake = db.Column(db.Integer)
    vegetarian = db.Column(db.Integer)
    vegan = db.Column(db.Integer)
    no_dairy = db.Column(db.Integer)


with app.app_context():
    db.create_all()

class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')
          
class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
      return render_template('index.html')
    else:
      return home()

@app.route('/calc.html', methods=['GET', 'POST'])
def calc_html():
    if request.method == 'GET':
      return render_template('calc.html')
    else:
      return calc_result()

@app.route('/about.html', methods=['GET', 'POST'])
def about_html():
    if request.method == 'GET':
      return render_template('about.html')
    else:
      return about_html()

@app.route('/user.html', methods=['GET', 'POST'])
def user_html():
    user = User.query.filter_by(username=current_user.username).first()
    username = user.username
    remaining = user.remainingCalorieIntake
    weekly =  user.weeklyCalorieIntake
    # vegetarian = user.vegetarian
    if user.vegetarian == 0:
      vegetarian = "No"
    else:
      vegetarian = "Yes"
    if user.vegan == 0:
      vegan = "No"
    else:
      vegan = "Yes"
    if user.no_dairy == 0:
      no_dairy = "No"
    else:
      no_dairy = "Yes"
    # vegan = user.vegan
    # no_dairy = user.no_dairy
    if request.method == 'GET':
      return render_template('user.html', username=username, remaining=remaining, weekly=weekly, vegetarian=vegetarian, vegan=vegan, no_dairy=no_dairy)
    else:
      return user_html()

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                session['logged_in'] = True
                return redirect(url_for('calc_html'))
    return render_template('brian_login.html', form=form)


#@app.route('/dashboard', methods=['GET', 'POST'])
#@login_required
#def dashboard():
#    return render_template('dashboard.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    session['logged_in'] = False
    return redirect(url_for('home'))


@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('brian_register.html', form=form)

currentfood = ""
@app.route('/tracker.html', methods=['GET', 'POST'])
def tracker_html():
    if request.method == 'GET':
      return render_template('tracker.html')
    else:
      global currentfood
      if request.form["booton"] == "Calculate":
        with app.app_context():
          food = select_food()
        if food == -1:
          currentfood = ""
          return render_template(
            'tracker.html',
            result="No food found, starve!"
          )
        else:
          currentfood = food
          return render_template(
            'tracker.html',
            result = food
          )
      else:
          if currentfood != "":
            user = User.query.filter_by(username=current_user.username).first()
            user.remainingCalorieIntake -= currentfood[1]
            db.session.commit()
            selectedfood = currentfood
            currentfood = ""
            return render_template(
              'tracker.html',
              result = selectedfood[0]+" has been selected!"
            )
          else:
            return render_template(
              'tracker.html',
              result = "No food has been selected."
            )

"""@ app.route('/dailyintake', methods=['GET', 'POST'])
def dailyintake():
    form = CalcForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('brian_register.html', form=form)
"""

"""if __name__ == '__main__':
    app.debug = True
    app.run()

if __name__ == '__main__':
    with app.app_context():
      app.debug = True
      app.run()
"""

# Calculator operations
def calc_result(): 
  print(request.form)
  weight_input=request.form['Weight']
  heightft_input=request.form['HeightFeet']
  heightin_input=request.form['HeightInch']
  age_input=request.form['Age']
  gender=request.form['Gender']
  vegetarian_input = "Vegetarian" in request.form
  vegan_input = "Vegan" in request.form
  nodairy_input = "NoDairy" in request.form

  if weight_input == "" or heightft_input == "" or heightin_input == "" or age_input == "" or gender == "":
    return render_template(
      'calc.html',
      Weight=weight_input,
      HeightFeet=heightft_input,
      HeightInch=heightin_input,
      Age=age_input,
      Gender=gender,
      result="Don't leave blank input fields!"
    )
#
  weight_input=int(weight_input)
  heightft_input=int(heightft_input)
  heightin_input=int(heightin_input)
  age_input=int(age_input)
  vegetarian_input=int(vegetarian_input)
  vegan_input=int(vegan_input)
  nodairy_input=int(nodairy_input)

  totalinches = (heightft_input * 12) + heightin_input

  if gender == "Woman":
    BMR = round(655.1 + (4.35 * weight_input) + (4.7 * totalinches) - (4.7 * age_input))

  elif gender == "Man":
    BMR = round(66.47 + (6.24 * weight_input) + (12.7 * totalinches) - (6.75 * age_input))

  user = User.query.filter_by(username=current_user.username).first()
  user.weeklyCalorieIntake = BMR * 7
  user.vegetarian = vegetarian_input
  user.vegan = vegan_input
  user.no_dairy = nodairy_input
  db.session.commit()



  return render_template(
    'calc.html',
    Weight=weight_input,
    HeightFeet=heightft_input,
    HeightInch=heightin_input,
    Age=age_input,
    Gender=gender,
    Vegetarian=vegetarian_input,
    Vegan=vegan_input,
    NoDairy=nodairy_input,
    result=BMR
  )

if __name__ == "__main__":
  with app.app_context():
    db.create_all()
  app.run(debug=True)

def select_food():
    user = User.query.filter_by(username=current_user.username).first()
    conn = sqlite3.connect('sqlite/food.db')
    c = conn.cursor()
    c.execute("SELECT * FROM food")
    foods = c.fetchall()
    conn.commit()
    conn.close()
    shuffle(foods)
    for food in foods:
        food_cals = food[1]
        food_vegetarian = food[5]
        food_nodairy = food[6]
        food_vegan = food[7]
        if (user.vegetarian == 1 and food_vegetarian != 1) or (user.vegan == 1 and food_vegan != 1) or (user.no_dairy == 1 and food_nodairy != 1): continue
        if food_cals <= user.remainingCalorieIntake:
            return food
    return -1
