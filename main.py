from tracking import price
from tracking import secret
from tracking import database


headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15'}
receive_email = ['stro3andr3i@g mail.com', 'stroeandrei483@gmail.com']
tracker = []


tracking = price.price(headers)
db = database.database(os.environ['host'], os.environ['user'], os.environ['password_database'], os.environ['database'])


con = db.connection();
query = con.cursor()
query.execute('SELECT * FROM tracking')
myresult = query.fetchall()
for i in myresult:
	tracker.append(tracking.price_steam(i[1]))
tracking.send_mail(os.environ['username'], receive_email, tracking.send_price(tracker), os.environ['password_email']) 