from tracking import Price
from tracking.secret import *
from tracking import Database
from PyQt5.QtWidgets import *
from datetime import date

import gui
import time
import threading
import requests


tracker = []
db = Database.database(HOST_DATABASE, USERNAME_DATABASE_TRACKING, PASSWORD_DATABASE_TRACKING, DATABASE_TRACKING)

class MainApp(gui.Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(MainApp , self).__init__()
        self.setupUi(self)
        self.InitUI()


    def InitUI(self):
        self.get_platforms()
        self.get_product.clicked.connect(self.get_link)
        self.tabWidget.tabBar().setVisible(False)
        self.textEdit.setReadOnly(True)
        self.header_btn.clicked.connect(self.set_header)
        self.price_btn.clicked.connect(self.open_price)
        self.settings_btn.clicked.connect(self.open_settings)
        self.view_btn.clicked.connect(self.open_view)   	
        self.create_btn.clicked.connect(self.open_create)
        self.addurl.clicked.connect(self.set_url)
        self.checker_btn.clicked.connect(self.set_platform)
        self.get_price.clicked.connect(self.get_all_price)
        self.get_status.clicked.connect(self.check_all_status)
        self.selected_price.clicked.connect(self.selected_prices)



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
            self.combo_platform.addItem(i[0])
        con.close()

    def set_header(self):
        header = self.header_text.text()
        header = {'User-Agent': str(header)}
        self.tracking = Price.Price(header)
        self.textEdit.append('User-Agent: '+str(header.get('User-Agent')))
        self.header_text.setReadOnly(True)
        self.email = self.set_email.text()
        self.email = self.email.split(',')
        self.textEdit.append('Email list:')
        for i in self.email:
            self.textEdit.append(i)

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

    # Adding the platforms in database
    def set_platform(self):
        url = self.url_checker_text.text()
        name = self.name_checker_text.text()
        con = db.connection()
        query = con.cursor()
        sql = 'INSERT INTO platform(name_platform, url_checker) values (%s, %s)'
        values = (name, url)
        query.execute(sql, values)
        self.comboBox.addItem(name)
        self.url_checker_text.setText('')
        self.name_checker_text.setText('')
        con.commit()
        con.close()

    # Get price
    def get_all_price(self):
        con = db.connection()
        query = con.cursor()
        sql = 'SELECT tracking.URL FROM tracking LEFT JOIN platform ON tracking.id_platform = platform.id'
        query.execute(sql)
        myrs = query.fetchall()
        for i in myrs:
            dictionar = self.tracking.get_price(i[0])
            self.tracking.convert_dict_to_arr(tracker, dictionar)
        self.textEdit.append(self.tracking.message_email(tracker))
        if(self.checkBox.isChecked()):
            self.tracking.send_mail(USERNAME_GMAIL, self.email, self.tracking.message_email(tracker), PASSWORD_GMAIL)
        con.close()
    
    def check_all_status(self):
        con = db.connection()
        query = con.cursor()
        sql = 'SELECT platform.name_platform, platform.url_checker from platform'
        query.execute(sql)
        myrs = query.fetchall()
        for i in myrs:
            status = self.tracking.get_status(i[1])
            self.textEdit.append(i[0]+': '+str(status))
        con.close()

    def get_link(self):
        self.combo_product.clear()
        con = db.connection()
        query = con.cursor()
        sql = "SELECT tracking.url FROM tracking LEFT JOIN platform ON tracking.id_platform = platform.id where platform.name_platform ='"+str(self.combo_platform.currentText())+"'"
        query.execute(sql)
        selected = query.fetchall()
        for i in selected:
            self.combo_product.addItem(str(i[0]))
        con.close()

    def selected_prices(self):
        tracker = []
        url = self.combo_product.currentText()
        print(url)
        x = self.tracking.get_price(str(url))
        self.tracking.convert_dict_to_arr(tracker, x)
        if(self.checkBox.isChecked()):
            self.tracking.send_mail(USERNAME_GMAIL, self.email, self.tracking.message_email(tracker), PASSWORD_GMAIL)
        self.textEdit.append(self.tracking.message_email(tracker))

if __name__ == '__main__':
    app = QApplication([])
    window = MainApp()
    window.show()
    app.exec_()