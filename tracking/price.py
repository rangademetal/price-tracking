import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage

class price:
	def __init__(self, header):
		self.header = header

	def price_steam(self, url):
		page = requests.get(url, self.header)
		soup = BeautifulSoup(page.content, 'html.parser')

		title = soup.find('div', {'class': 'apphub_AppName'}).text
		price = soup.find('div', {'class': 'game_purchase_price price'}).text
		
		price = price.split()
		price = ''.join(price)
		price = price.replace('€', ' - Euro')
		
		return str(url)+'\n'+str(title)+'\n'+str(price)+'\n\n\n'

	def send_price(self, array):
		price = ''
		for i in array:
			price += str(i)
		return price

	def send_mail(self, sender_email, receive_email, data, password):
		msg = EmailMessage()
		msg['Subject'] = 'Price tracker'
		msg['From'] = sender_email
		msg['To'] = receive_email
		msg.set_content(data)

		with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
			smtp.login(sender_email, password)
			smtp.send_message(msg)