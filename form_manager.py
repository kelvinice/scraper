import sys
from PyQt5.QtWidgets import *
import main

class form_manager(QMainWindow):
    def __init__(self,result, parent=None):
        super(form_manager,self).__init__(parent)

        layout = QVBoxLayout()
        layout.addWidget(QTextEdit(str(result)))

        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)
        self.resize(800, 600)
        self.setWindowTitle("Form Manager")
        self.statusBar().showMessage("Active")

if __name__=="__main__":
    main.main()
