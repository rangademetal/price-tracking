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
		if soup.find('div', {'class': 'discount_pct'}):
			title = soup.find('div', {'class': 'apphub_AppName'}).get_text()
			price = soup.find('div', {'class': 'discount_final_price'}).get_text()
		else:
			title = soup.find('div', {'class': 'apphub_AppName'}).get_text()
			price = soup.find('div', {'class': 'game_purchase_price price'}).get_text()
			price = price.split()
			price = ''.join(price)
		items = {'url': url, 'title': title, 'price':price}
		return items.values()
		
	def message_email(self, array):
		price = ''
		for i in array:
			price += str(i)
		return price

	def convert_dict_to_arr(self, array, dict_array):
		for i in dict_array:
			array.append(i+'\n')
		array.append('\n')

	def send_mail(self, sender_email, receive_email, data, password):
		msg = EmailMessage()
		msg['Subject'] = 'Price tracker'
		msg['From'] = sender_email
		msg['To'] = receive_email
		msg.set_content(data)
		with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
			smtp.login(sender_email, password)
			smtp.send_message(msg)