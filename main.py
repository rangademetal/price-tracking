from tracking import price
from tracking.secret import *
from tracking import database
import os


headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15'}
receive_email = ['stro3andr3i@g mail.com', 'stroeandrei483@gmail.com']
tracker = []


tracking = price.price(headers)
db = database.database(HOST_DATABASE, USERNAME_DATABASE_TRACKING, PASSWORD_DATABASE_TRACKING, DATABASE_TRACKING)


con = db.connection();
query = con.cursor()
query.execute('SELECT * FROM tracking')
myresult = query.fetchall()
for i in myresult:
	tracker.append(tracking.price_steam(i[1]))
tracking.send_mail(USERNAME_GMAIL, receive_email, tracking.send_price(tracker), PASSWORD_GMAIL) 