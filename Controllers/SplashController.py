from PyQt6.QtCore import QTimer

import time

from UI.SplashWindow import SplashWindow
from UI.MainWindow import MainApp

class SplashController:

    def __init__(self,splashwindow:SplashWindow):
        self.counter = 0
        self.n = 100
        self.timer = QTimer()
        self.splashwindow =splashwindow
        self.timer.timeout.connect(self.loading)
        self.timer.start(30)

    def loading(self):
        # set progressbar value
        self.splashwindow.progressBar.setValue(self.counter)
        # stop progress if counter
        # is greater than n and
        # display main window app
        if self.counter >= self.n:
            self.timer.stop()
            self.splashwindow.close()
            time.sleep(1)
            window = MainApp()
            window.show()
        self.counter += 1