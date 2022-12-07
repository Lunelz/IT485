from datetime import datetime, timedelta
from threading import Timer
from app import calorie_refill

x=datetime.today()
y = x.replace(day=x.day, hour=0, minute=0, second=0, microsecond=0) + timedelta(days=7)
delta_t=y-x

secs=delta_t.total_seconds()

t = Timer(secs, calorie_refill)
t.start()
print('started')