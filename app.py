from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import requests
import json
import meal_suggestor

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
    dailyCalorieIntake = db.Column(db.Integer) 
    weeklyCalorieIntake = db.Column(db.Integer) 
    
    def __init__(self, dailyCalorieIntake, weeklyCalorieIntake):
      self.dailyCalorieIntake = dailyCalorieIntake
      self.weeklyCalorieIntake = weeklyCalorieIntake

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
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

@app.route('/tracker.html', methods=['GET', 'POST'])
def tracker_html():
    if request.method == 'GET':
      return render_template('tracker.html')
    else:
      food = meal_suggestor.select_food(300)
      if food == -1:
        return render_template(
          'tracker.html',
          result="No food found, starve!"
        )
      else:
        return render_template(
          'tracker.html',
          result = food
        )

if __name__ == '__main__':
    app.debug = True
    app.run()

# Calculator operations
def calc_result(): 
  weight_input=request.form['Weight']
  heightft_input=request.form['HeightFeet']
  heightin_input=request.form['HeightInch']
  age_input=request.form['Age']
  gender=request.form['Gender']

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

  totalinches = (heightft_input * 12) + heightin_input

  if gender == "Woman":
    BMR = round(655.1 + (4.35 * weight_input) + (4.7 * totalinches) - (4.7 * age_input))

  elif gender == "Man":
    BMR = round(66.47 + (6.24 * weight_input) + (12.7 * totalinches) - (6.75 * age_input))

  return render_template(
    'calc.html',
    Weight=weight_input,
    HeightFeet=heightft_input,
    HeightInch=heightin_input,
    Age=age_input,
    Gender=gender,
    result=BMR
  )

if __name__ == "__main__":
  with app.app_context():
    db.create_all()
  app.run(debug=True)

