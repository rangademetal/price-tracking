from tracking import price
import os
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15'}

tracker = []
tracking = price.price(headers)
price = tracking.price_steam('https://store.steampowered.com/app/244450/Men_of_War_Assault_Squad_2/')
tracker.append(price)
price = tracking.price_steam('https://store.steampowered.com/app/920840/Men_of_War_Assault_Squad_2__Ostfront_Veteranen/')
tracker.append(price)
price = tracking.price_steam('https://store.steampowered.com/app/1329600/Karting/')
tracker.append(price)

sender_email = 'pricetrackingbot123@gmail.com'
receive_email = ['stro3andr3i@gmail.com', 'stroeandrei483@gmail.com']
password = 'pricebot123.'
os.environ['email_sender'] = 'pricetrackingbot123@gmail.com'
os.environ['email_password'] = 'pricebot123.'

price = tracking.send_price(tracker)
tracking.send_mail(sender_email, receive_email, price, password)
