import sys
from PyQt5.QtWidgets import *
import main
import PyQt5.QtCore
from functools import partial
from bs4 import BeautifulSoup
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

class input_manager(QMainWindow):
    def cellChanged(self,row, col):

        #Value changed
        if col==3:
            print("Value Change To : "+str(self.tblForm.item(row,col).text()))
            import scraper
            text = str(self.tblForm.item(row,col).text())
            self.listofinputed.append(
                {"tag": scraper.getheader(self.inputs[row])["tag"], "id": scraper.getheader(self.inputs[row])["id"], "class": scraper.getheader(self.inputs[row])["class"],
                 "name": scraper.getheader(self.inputs[row])["name"], "value": text})


    def on_click(self,args=0):
        # TODO VALIDASI JIKA BUTTON
        import scraper
        self.listofinputed.append(
            {"tag": scraper.getheader(self.inputs[args])["tag"],"id": scraper.getheader(self.inputs[args])["id"], "class": scraper.getheader(self.inputs[args])["class"],
             "name": scraper.getheader(self.inputs[args])["name"], "value": "{button.click}"})
        # print(self.listofinputed)
        # if(str(self.tblForm.item(args,0).text()).lower()=="submit"):
        #     import scraper
        #     scraper.browser = scraper.dive(self.url, self.listofinputed)

        # else:
        #     pass

    def executeAllClick(self):
        print("executed")
        import scraper
        scraper.browser = scraper.dive_plus(self.url, self.listofinputed)
        wait = WebDriverWait(scraper.browser, 5)
        try:
            page_loaded = wait.until_not(
                lambda browser: browser.current_url == self.url
            )
            print("Page is ready!")
            cookies = scraper.browser.get_cookies()

            for cookie in cookies:
                print(cookie['name'], " : ", cookie['value'])
                scraper.session.cookies.set(cookie['name'], cookie['value'])
            url2 = "https://industry.socs.binus.ac.id/learning-plan/"
            loginResult = scraper.scrape(url2)
            self.browser_shower.setText(str(loginResult))
            soup = BeautifulSoup(loginResult, features='html.parser')

        except TimeoutException:
            print("Timeout")



    def __init__(self,url,result, parent=None):
        super(input_manager, self).__init__(parent)
        self.url = url
        self.listofinputed= []
        self.inputs = result
        self.tblForm = QTableWidget()

        from scraper import getheader, findallinput,findallbutton,findalltextarea

        self.inputs = findallinput(result)+findallbutton(result)+findalltextarea(result)
        # self.buttons = findallbutton(result)


        self.tblForm.setRowCount(len(self.inputs))

        self.tblForm.setColumnCount(6)

        header = ("Type", "Id", "Name", "Value", "Button","Inner")
        self.tblForm.setHorizontalHeaderLabels(header)

        self.rowcount = 0
        for inp in self.inputs:
            header = getheader(inp)
            if header["innerHTML"]!= None and header["innerHTML"].lower()=="submit":
                itemtype = QTableWidgetItem(header["innerHTML"])
            else:
                itemtype = QTableWidgetItem(header["type"])
            itemid = QTableWidgetItem(header["id"])
            itemname = QTableWidgetItem(header["name"])
            iteminner = QTableWidgetItem(header["innerHTML"])

            itemtype.setFlags(itemtype.flags() & ~PyQt5.QtCore.Qt.ItemIsEditable & ~PyQt5.QtCore.Qt.TextEditable)
            itemid.setFlags(itemtype.flags() & ~PyQt5.QtCore.Qt.ItemIsEditable & ~PyQt5.QtCore.Qt.TextEditable)
            itemname.setFlags(itemtype.flags() & ~PyQt5.QtCore.Qt.ItemIsEditable & ~PyQt5.QtCore.Qt.TextEditable)

            self.tblForm.setItem(self.rowcount, 0, itemtype)
            self.tblForm.setItem(self.rowcount, 1, itemid)
            self.tblForm.setItem(self.rowcount, 2, itemname)
            self.tblForm.setItem(self.rowcount, 3, QTableWidgetItem(header["value"]))
            self.tblForm.setItem(self.rowcount, 4, iteminner)
            input_button = QPushButton("input")
            input_button.clicked.connect(partial(self.on_click, self.rowcount))
            self.tblForm.setCellWidget(self.rowcount, 4, input_button)

            self.rowcount += 1

        self.tblForm.cellChanged.connect(self.cellChanged)
        layout = QVBoxLayout()
        self.browser_shower = QTextEdit(str(result))
        self.execute_button = QPushButton("Execute")

        self.execute_button.clicked.connect(self.executeAllClick)
        layout.addWidget(self.browser_shower)
        layout.addWidget(self.tblForm)
        layout.addWidget(self.execute_button)

        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)
        self.resize(600, 400)
        self.setWindowTitle("Input Manager")
        self.statusBar().showMessage("Active")


if __name__=="__main__":
    main.main()