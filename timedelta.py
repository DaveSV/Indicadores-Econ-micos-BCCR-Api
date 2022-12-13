#Collecting last dates into array 
from datetime import date,timedelta 
today = date.today() 
dates = [(today - timedelta(days=i)).strftime("%d-%m-%Y") for i in range(10)] 
print(dates) 