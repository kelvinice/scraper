import sys
from PyQt5.QtWidgets import *
import main

class input_manager(QMainWindow):
    def __init__(self,result, parent=None):
        super(input_manager, self).__init__(parent)
        self.tblForm = QTableWidget()

        from scraper import getheader, findallinput

        inputs = findallinput(result)
        self.tblForm.setRowCount(len(inputs))

        self.tblForm.setColumnCount(3)

        header = ("Type", "Id", "Name", "Value", "Button")
        self.tblForm.setHorizontalHeaderLabels(header)

        self.rowcount = 0
        for inp in inputs:
            header = getheader(inp)
            self.tblForm.setItem(self.rowcount, 0, QTableWidgetItem(header["type"]))
            self.tblForm.setItem(self.rowcount, 1, QTableWidgetItem(header["id"]))
            self.tblForm.setItem(self.rowcount, 2, QTableWidgetItem(header["name"]))
            self.tblForm.setItem(self.rowcount, 3, QTableWidgetItem(header["value"]))
            self.tblForm.setCellWidget(self.rowcount, 4, QPushButton("input"))
            self.rowcount += 1

        layout = QVBoxLayout()
        # layout.addWidget(QTextEdit(str(result)))
        layout.addWidget(self.tblForm)

        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)
        self.resize(400, 300)
        self.setWindowTitle("Input Manager")
        self.statusBar().showMessage("Active")


if __name__=="__main__":
    main.main()