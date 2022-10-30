from datetime import datetime

# get current datetime
dt = datetime.now()
print('Datetime is:', dt)

# get day of week as an integer
x = dt.weekday()
print('Day of a week is:', x)

weeklyMultiplier = abs(x - 6)
if weeklyMultiplier == 0 :
    weeklyMultiplier = 7
def newAccountTally():
    print('Weekly multiplier for this new account is', weeklyMultiplier)
    dailyIntake = int(input('How many calories do you eat per day? ')) #replace with database value
    print('If you signed up today you would still be able to eat', weeklyIntake, 'calories')

dailyIntake = int(input('How many calories do you eat per day? ')) #replace with database value
weeklyIntake = dailyIntake * 7

def weeklyReset():
        weeklyIntake = dailyIntake * 7
