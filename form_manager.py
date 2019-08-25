import sys
from PyQt5.QtWidgets import *

import main
from functools import partial
import input_manager
import automator

class form_manager(QMainWindow):
    def on_click(self,args=0):

        if(self.comboAuto.currentText() == "Manual"):
            dialog = input_manager.input_manager(url=self.url, result=self.forms[int(args)], parent=self)
            dialog.show()
        elif(self.comboAuto.currentText() == "Automated"):
            automator.Automator(url=self.url, result=self.forms[int(args)])


    def __init__(self,url,result, parent=None):
        super(form_manager,self).__init__(parent)
        self.url = url
        self.tblForm = QTableWidget()

        from scraper import getheader, findallform

        self.forms = findallform(result)
        self.tblForm.setRowCount(len(self.forms))

        self.tblForm.setColumnCount(3)

        header = ("Method", "Action", "Event")
        self.tblForm.setHorizontalHeaderLabels(header)

        self.rowcount = 0
        for f in self.forms:
            header = getheader(f)
            methoditem = QTableWidgetItem(header["method"])

            self.tblForm.setItem(self.rowcount, 0, methoditem)
            self.tblForm.setItem(self.rowcount, 1, QTableWidgetItem(header["action"]))
            button = QPushButton("Input",self)

            curr = self.rowcount
            button.clicked.connect(partial(self.on_click,curr))
            self.tblForm.setCellWidget(self.rowcount, 2, button)
            # self.tblForm.setCellWidget(self.rowcount, 3, comboAuto)
            self.rowcount+=1

        layout = QVBoxLayout()
        layout.addWidget(self.tblForm)

        # TODO refactor
        self.comboAuto = QComboBox()
        self.comboAuto.addItem("Manual")
        self.comboAuto.addItem("Automated")

        gridAction = QGridLayout()
        gridAction.setColumnStretch(1, 2)
        gridAction.addWidget(QLabel("Type of Action"))
        gridAction.addWidget(self.comboAuto)

        leftright = QWidget()
        leftright.setLayout(gridAction)
        layout.addWidget(leftright)

        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)
        self.resize(450, 300)
        self.setWindowTitle("Form Manager")
        self.statusBar().showMessage("Active")

if __name__=="__main__":
    main.main()
