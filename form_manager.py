import sys
from PyQt5.QtWidgets import *

import main
from functools import partial
import input_manager

class form_manager(QMainWindow):
    def on_click(self,args=0):
        dialog = input_manager.input_manager(url = self.url,result=self.forms[int(args)], parent=self)
        dialog.show()

    def __init__(self,url,result, parent=None):
        super(form_manager,self).__init__(parent)
        self.url = url
        self.tblForm = QTableWidget()

        from scraper import getheader, findallform

        self.forms = findallform(result)
        self.tblForm.setRowCount(len(self.forms))

        self.tblForm.setColumnCount(3)

        header = ("Method", "Action", "Button")
        self.tblForm.setHorizontalHeaderLabels(header)

        self.rowcount = 0
        for f in self.forms:

            header = getheader(f)
            methoditem = QTableWidgetItem(header["method"])

            self.tblForm.setItem(self.rowcount, 0, methoditem)
            self.tblForm.setItem(self.rowcount, 1, QTableWidgetItem(header["action"]))
            button = QPushButton("input",self)
            curr = self.rowcount
            button.clicked.connect(partial(self.on_click,curr))
            self.tblForm.setCellWidget(self.rowcount, 2, button)
            self.rowcount+=1


        layout = QVBoxLayout()
        # layout.addWidget(QTextEdit(str(result)))
        layout.addWidget(self.tblForm)

        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)
        self.resize(400, 300)
        self.setWindowTitle("Form Manager")
        self.statusBar().showMessage("Active")

if __name__=="__main__":
    main.main()
