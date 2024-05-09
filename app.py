import sys

from PyQt6.QtWidgets import QApplication

from UI.SplashWindow import SplashWindow
from Utils.StyleSheets.MainWindowStyle import splashStyle

if __name__ == "__main__":
    app = QApplication([])
    app.setStyleSheet(splashStyle)
    window = SplashWindow()
    window.show()
    sys.exit(app.exec())
