import requests
from bs4 import BeautifulSoup


def user-agent(self):
	response = requests.get('https://www.whatismybrowser.com/detect/what-is-my-user-agent')
	soup = BeautifulSoup(response.content, 'html.parser')
