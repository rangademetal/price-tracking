from tracking import price
from tracking.secret import *
from tracking import database
from PyQt5.QtWidgets import *
import gui
from datetime import date
import time
import threading
import requests


headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15'}
receive_email = ['stro3andr3i@gmail.com', 'stroeandrei483@gmail.com']
tracker = []


tracking = price.price(headers)
db = database.database(HOST_DATABASE, USERNAME_DATABASE_TRACKING, PASSWORD_DATABASE_TRACKING, DATABASE_TRACKING)


tracking.send_mail(USERNAME_GMAIL, receive_email, tracking.message_email(tracker), PASSWORD_GMAIL)
tracking.convert_dict_to_arr(tracker, tracking.price_playstation('https://store.playstation.com/en-ro/product/EP3473-CUSA23320_00-9096831598950562'))
tracking.send_mail(USERNAME_GMAIL, receive_email, tracking.message_email(tracker), PASSWORD_GMAIL)
class MainApp(gui.Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(MainApp , self).__init__()
        self.setupUi(self)
        self.InitUI()


    def InitUI(self):
        self.get_platforms()
        self.tabWidget.tabBar().setVisible(False)
        self.textEdit.setReadOnly(True)
        self.price_btn.clicked.connect(self.open_price)
        self.settings_btn.clicked.connect(self.open_settings)
        self.view_btn.clicked.connect(self.open_view)   	
        self.create_btn.clicked.connect(self.open_create)
        self.addurl.clicked.connect(self.set_url)
        self.checker_btn.clicked.connect(self.set_platform)


    def open_price(self):
        self.tabWidget.setCurrentIndex(0) 
    def open_settings(self):
        self.tabWidget.setCurrentIndex(1)
    def open_view(self):
        self.tabWidget.setCurrentIndex(2)
    def open_create(self):
        self.tabWidget.setCurrentIndex(3)


    def get_platforms(self):
        con = db.connection()
        query = con.cursor()
        query.execute('SELECT name_platform FROM platform')
        myrs = query.fetchall()
        for i in myrs:
            self.comboBox.addItem(i[0])
        con.close()

    def set_url(self):
        url = self.text_url.text()
        con = db.connection()
        query = con.cursor()
        sql = 'INSERT INTO tracking(url, date_put, id_platform) values(%s, %s, %s)'
        query.execute("SELECT id FROM platform WHERE name_platform = '"+str(self.comboBox.currentText())+"'")
        id_platform = query.fetchone()
        values = (url, date.today().strftime('%Y-%m-%d'), id_platform[0])
        query.execute(sql, values)
        con.commit()
        con.close()
        self.textEdit.append('Added ' +url +' at '+ date.today().strftime('%Y-%m-%d'))
    def set_platform(self):
        url = self.url_checker_text.text()
        name = self.name_checker_text.text()
        con = db.connection()
        query = con.cursor()
        sql = 'INSERT INTO platform(name_platform, url_checker) values (%s, %s)'
        values = (name, url)
        query.execute(sql, values)
        self.comboBox.addItem(name)
        con.commit()
        con.close()
        self.url_checker_text.setText('')
        self.name_checker_text.setText('')





if __name__ == '__main__':
    app = QApplication([])
    window = MainApp()
    window.show()
    app.exec_()