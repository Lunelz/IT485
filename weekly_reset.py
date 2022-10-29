from datetime import datetime, timedelta
from threading import Timer
import weekly_tally

x=datetime.today()
y = x.replace(day=x.day, hour=0, minute=0, second=0, microsecond=0) + timedelta(days=7)
delta_t=y-x

secs=delta_t.total_seconds()

t = Timer(secs, weekly_tally.weeklyReset)
t.start()