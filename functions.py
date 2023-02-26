from dateutil.parser import parse
import datetime
raw = '25 Feb 2023 19:54:09 +0300'
dt = parse(raw)
print(dt)
today_date = datetime.date.today()
print(today_date)
d_truncated = datetime.date(dt.year, dt.month, dt.day)
print(d_truncated)
if d_truncated == today_date:
    print('y')
else: print('n')
str_date = today_date.strftime("%d %b %Y")
print(str_date)

