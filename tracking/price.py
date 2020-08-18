from bs4 import BeautifulSoup
from email.message import EmailMessage

import smtplib
import requests


class Price:
	def __init__(self, header):
		self.header = header

	def price_steam(self, url):
		page = requests.get(url, self.header)
		soup = BeautifulSoup(page.content, 'html.parser')
		title = soup.find('div', {'class': 'apphub_AppName'}).get_text()
		if soup.find('div', {'class': 'discount_pct'}):
			price_total = soup.find('div', {'class':'discount_original_price'}).get_text()
			price_final = soup.find('div', {'class': 'discount_final_price'}).get_text()
			discount = soup.find('div', {'class': 'discount_pct'}).get_text()
			items = {'url': url, 'title': 'Title: '+title, 'discount':'Discount: '+discount ,'price_total':'Total price: '+price_total, 'price_final':'Final price: '+price_final}
		else:		
			price = soup.find('div', {'class': 'game_purchase_price price'}).get_text()
			price = price.split()
			price = ''.join(price)
			items = {'url': url, 'title': 'Title: '+title, 'price':'Price: '+price}
		return items.values()
	
	def price_playstation(self, url):
		page = requests.get(url, self.header)
		soup = BeautifulSoup(page.content, 'html.parser')
		title = soup.find('h2', {'class': 'pdp__title'}).get_text()
		if soup.find('span', {'class': 'price-display__strikethrough'}):
			price_total = soup.find('div', {'class': 'price'}).get_text()
			price_final = soup.find('h3', {'class': 'price-display__price'}).get_text()
			discount = soup.find('span', {'class': 'discount-badge__message'}).get_text()
			items = {'url': url, 'title': 'Title: '+title, 'discount':'Discount: '+discount ,'price_total':'Total price: '+price_total, 'price_final':'Final price: '+price_final}
		else:
			price_final = soup.find('h3', {'class': 'price-display__price'}).get_text()
			items = {'url': url, 'title': 'Title: '+title, 'price':'Price: '+price_final}
		return items.values()
	
	def get_price(self, url):
		page = requests.get(url, self.header)
		soup = BeautifulSoup(page.content, 'html.parser')
		if soup.find('div', {'class': 'apphub_AppName'}):
			self.x = self.price_steam(url)
		elif soup.find('h2', {'class': 'pdp__title'}):
			self.x = self.price_playstation(url)
		return self.x
		 
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
	
	def get_status(self, url):
		response = requests.get(url, self.header)
		return response.status_code
