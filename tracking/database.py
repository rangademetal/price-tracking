import mysql.connector

class database:
	def __init__(self, host, user, password, database):
		self.host = host
		self.user = user
		self.password = password
		self.database = database
	def connection(self):
		con = mysql.connector.connect(host = self.host, user = self.user, password = self.password, database = self.database)
		return con


# SELECT tracking.URL FROM tracking LEFT JOIN platform ON tracking.id_platform = platform.id'