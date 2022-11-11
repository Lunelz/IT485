from flask import Flask, render_template, request
import requests
import json
import meal_suggestor

# Flask Instance
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def calc_html():
    if request.method == 'GET':
      return render_template('calc.html')
    else:
      return calc_result()

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
