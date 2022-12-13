from asyncio.windows_events import NULL
from flask import Flask, render_template, request, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo
from flask_bcrypt import Bcrypt
import requests
import json
import sqlite3
from random import shuffle
from datetime import datetime, timedelta
from threading import Timer

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
    history =db.Column(db.Text)


class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    password2 = PasswordField(validators=[
                             InputRequired(), EqualTo('password')], render_kw={"placeholder": "Repeat Password"})
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
def homepage_html():
  form = LoginForm()
  if request.method == 'GET':
    return render_template('index.html', form=form)
  else:
    if form.validate_on_submit():
      user = User.query.filter_by(username=form.username.data).first()
      if user:
          if bcrypt.check_password_hash(user.password, form.password.data):
              login_user(user)
              return redirect(url_for('tracker_html'))
  return render_template('index.html', form=form)


@app.route('/calc.html', methods=['GET', 'POST'])
def calc_html():
    if request.method == 'GET':
      return render_template('calc.html')
    else:
      return calc_result()

@app.route('/user.html', methods=['GET', 'POST'])
def user_html():
    user = User.query.filter_by(username=current_user.username).first()
    conn = sqlite3.connect('sqlite/food.db')
    c = conn.cursor()
    username = user.username
    remaining = user.remainingCalorieIntake
    weekly =  user.weeklyCalorieIntake
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

    history = user.history
    try: 
      historylist = list(history.split(","))
    except AttributeError:
       pass
    foodhistory = []
    # try:
    i=0
    x=0
    try:
      for i in historylist:
        i = int(i)

      # historylist contains indexes of foods so we select whatever food has each index once per loop.
        foodhistory.append(c.execute("SELECT meal FROM food WHERE Identifier = " + str(i)).fetchone())
        x+=1
    except UnboundLocalError:
      pass


    conn.close()

    try:
        food24 = str(foodhistory[-1]).strip("()',")
    except IndexError:
        food24 = ''
    try:
        food23 = str(foodhistory[-2]).strip("()',")
    except IndexError:
        food23 = ''
    try:
        food22 = str(foodhistory[-3]).strip("()',")
    except IndexError:
        food22 = ''
    try:
        food21 = str(foodhistory[-4]).strip("()',")
    except IndexError:
        food21 = ''
    try:
        food20 = str(foodhistory[-5]).strip("()',")
    except IndexError:
        food20 = ''
    try:
        food19 = str(foodhistory[-6]).strip("()',")
    except IndexError:
        food19 = ''
    try:
        food18 = str(foodhistory[-7]).strip("()',")
    except IndexError:
        food18 = ''
    try:
        food17 = str(foodhistory[-8]).strip("()',")
    except IndexError:
        food17 = ''
    try:
        food16 = str(foodhistory[-9]).strip("()',")
    except IndexError:
        food16 = ''
    try:
        food15 = str(foodhistory[-10]).strip("()',")
    except IndexError:
        food15 = ''    
    try:
        food14 = str(foodhistory[-11]).strip("()',")
    except IndexError:
        food14 = ''
    try:
        food13 = str(foodhistory[-12]).strip("()',")
    except IndexError:
        food13 = ''
    try:
        food12 = str(foodhistory[-13]).strip("()',")
    except IndexError:
        food12 = ''
    try:
        food11 = str(foodhistory[-14]).strip("()',")
    except IndexError:
        food11 = ''
    try:
        food10 = str(foodhistory[-15]).strip("()',")
    except IndexError:
        food10 = ''
    try:
        food9 = str(foodhistory[-16]).strip("()',")
    except IndexError:
        food9 = ''
    try:
        food8 = str(foodhistory[-17]).strip("()',")
    except IndexError:
        food8 = ''
    try:
        food7 = str(foodhistory[-18]).strip("()',")
    except IndexError:
        food7 = ''
    try:
        food6 = str(foodhistory[-19]).strip("()',")
    except IndexError:
        food6 = ''
    try:
        food5 = str(foodhistory[-20]).strip("()',")
    except IndexError:
        food5 = ''
    try:
        food4 = str(foodhistory[-21]).strip("()',")
    except IndexError:
        food4 = ''    
    try:
        food3 = str(foodhistory[-22]).strip("()',")
    except IndexError:
        food3 = ''
    try:
        food2 = str(foodhistory[-23]).strip("()',")
    except IndexError:
        food2 = ''
    try:
        food1 = str(foodhistory[-24]).strip("()',")
    except IndexError:
        food1 = ''
    try:
        food0 = str(foodhistory[-25]).strip("()',")
    except IndexError:
        food0 = ''



    if request.method == 'GET':
        return render_template('user.html', username=username, remaining=remaining, weekly=weekly, vegetarian=vegetarian, vegan=vegan, no_dairy=no_dairy, history=history, food24=food24, food23=food23, food22=food22, food21=food21, food20=food20, food19=food19, food18=food18, food17=food17, food16=food16, food15=food15, food14=food14, food13=food13,food12=food12, food11=food11, food10=food10, food9=food9, food8=food8, food7=food7, food6=food6,food5=food5,food4=food4,food3=food3, food2=food2, food1=food1, food0=food0)


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
    return render_template('index.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    session['logged_in'] = False
    return redirect(url_for('homepage_html'))


@ app.route('/register.html', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

currentfood = ""

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
        food_vegetarian = food[3]
        food_nodairy = food[4]
        food_vegan = food[5]
        if (user.vegetarian == 1 and food_vegetarian != 1) or (user.vegan == 1 and food_vegan != 1) or (user.no_dairy == 1 and food_nodairy != 1): continue
        if food_cals <= user.remainingCalorieIntake:
            return food
    return -1

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
            result = food[0],
            result2 = food[1],
            result3 = food[2],
            result4 = food[6],
          )
      else: #If they click select
          if currentfood != "": #Look if current food is not empty -- if they hit select before calculate this would be empty.
            user = User.query.filter_by(username=current_user.username).first() 
            user.remainingCalorieIntake -= currentfood[1]
            if user.history is None or user.history == "": #If user.history is empty, we do not want it to start with a comma.
              user.history = "" #This is in case that user.history is none, so this'll convert it to a string so that we can then add the string current food.
              user.history += str(currentfood[7])
            else:
              user.history += "," + str(currentfood[7])
            db.session.commit()
            selectedfood = currentfood #Saving currentfood before emptying the value so we can print out a message.
            currentfood = "" #Current food had to be cleared because otherwise people would be able to keep selected the current food. Due to it being a global variable and the contents stored outside of the function.
            return render_template(
              'tracker.html',
              result = selectedfood[0]+" has been selected!"
            )
          else:
            return render_template(
              'tracker.html',
              result = "No food has been selected."
            )

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
  if user.remainingCalorieIntake is None:
    user.remainingCalorieIntake = BMR * 7
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
    result=BMR *7
  )



def calorie_refill():
  user = User.query.filter_by(username=current_user.username).first()
  # user.remainingCalorieIntake = user.weeklyCalorieIntake
  user.remainingCalorieIntake = user.remainingCalorieIntake - 1
  db.session.commit()

def weekly_reset():
  x=datetime.today()
  y = x.replace(day=x.day, hour=0, minute=0, second=0, microsecond=0) + timedelta(seconds=1)
  delta_t=y-x

  secs=delta_t.total_seconds()

  t = Timer(secs, calorie_refill)
  t.start()

if __name__ == '__main__':
    with app.app_context():
      db.create_all()
      app.debug = True
      app.run() 