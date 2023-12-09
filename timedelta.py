# Collecting last dates into array 
from datetime import date,timedelta, datetime

today = date.today()
yesterday = datetime.today()+timedelta(days=-1)
dates = [(today - timedelta(days=i)).strftime("%d-%m-%Y") for i in range(10)] 
print(yesterday) 

now = datetime.now()+timedelta(days=-1)
format = now.strftime('%d/%m/%Y')
print(format)