import mainwindow
import sys
from PyQt4.QtGui import QApplication, QSplashScreen, QPixmap
from PyQt4.Qt import Qt
import time
from datetime import datetime

class Application:
    
    def __init__(self):
        self.qApp = QApplication(sys.argv)
        self.window = mainwindow.MainWindow(self)
        
        self.window.update_ui({"OTP": 3500, "MOL": 13400, "RICHTER": 3700, "DAX": 9950, "RÁBA": 1100, "UPDATE1": 990, "ELMŰ": 13900}, 
                            lambda n: w.stock_values(n, [(datetime(2014, 11, 27, 9, 32), 12400, 2), (datetime(2014, 11, 27, 9, 35), 12350, 5)]))
    
    def load(self):
        splash = QSplashScreen(QPixmap("main_icon.png"))
        splash.show()
        splash.showMessage("Loading modules", Qt.AlignBottom)
        time.sleep(1)
        splash.showMessage("Loading data", Qt.AlignBottom)
        time.sleep(2)
        splash.finish(self.window)
        
    def exec(self):
        self.window.show()
        self.qApp.exec()

if __name__ == '__main__':
    application = Application()
    application.load()
    application.exec()
    