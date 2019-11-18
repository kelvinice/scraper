import sys
from PyQt5.QtWidgets import *
import form_manager
from selenium import webdriver


class InputURLWindow(QMainWindow):
    def on_click(self):
        import scraper
        text = self.txtUrl.text()
        result = scraper.scrape(text)

        dialog = form_manager.form_manager(url=text, result=result, parent=self)
        dialog.show()

    def __init__(self, parent=None):
        super(InputURLWindow, self).__init__(parent)
        browsers = webdriver.Firefox()
        browsers.get("https://www.facebook.com/")

        layout = QVBoxLayout()
        self.txtUrl = QLineEdit()
        self.btnSubmit = QPushButton('Submit')

        layout.addWidget(QLabel("Url: "))
        self.txtUrl.setText("https://industry.socs.binus.ac.id/learning-plan/auth/login")
        layout.addWidget(self.txtUrl)
        layout.addWidget(QLabel("\n"))
        layout.addWidget(self.btnSubmit)

        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)

        self.btnSubmit.clicked.connect(self.on_click)

        self.resize(400, 150)
        self.setWindowTitle("Scaper")
        self.statusBar().showMessage("Scraper Application v0.1")


def main():
    app = QApplication(sys.argv)

    window = InputURLWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
