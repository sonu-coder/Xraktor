from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import QPixmap, QIcon
from Utils.Const import *


class SplashWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 250)
        self.setWindowIcon(QIcon('images/logo_32_blue.png'))
        self.setWindowTitle(AppName)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        from Controllers.SplashController import SplashController
        self.splashc = SplashController(splashwindow=self)

        self.initUI()

    def initUI(self):
        # layout to display splash screen frame
        layout = QHBoxLayout()
        self.setLayout(layout)

        # splash screen frame
        self.frame = QFrame()
        self.frame.setObjectName('splash_frame')
        layout.addWidget(self.frame)

        # splash screen title
        self.splash_logo_layout = QVBoxLayout(self.frame)
        self.splash_logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.splash_logo_text = QLabel(AppName)
        self.splash_logo_text.setObjectName('splash_logo_text')
        self.splash_logo_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.splash_logo_icon = QLabel(self.frame)
        self.splash_logo_icon.setObjectName('splash_logo_icon')
        self.splash_logo_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.splash_logo_pix = QPixmap('images/logo_64_blue.png')
        self.splash_logo_icon.setPixmap(self.splash_logo_pix)

        # splash screen title description
        self.description_label = QLabel(self.frame)

        self.description_label.resize(300, 20)
        self.description_label.setObjectName('desc_label')
        self.description_label.setText(SplashDesc)
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Splash Version text
        self.version_label = QLabel(self.frame)
        self.version_label.resize(300, 20)
        self.version_label.setObjectName('version_label')
        self.version_label.setText(AppVersion)
        self.version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.splash_logo_layout.addWidget(self.splash_logo_icon)
        self.splash_logo_layout.addWidget(self.splash_logo_text)
        self.splash_logo_layout.addWidget(self.description_label)
        self.splash_logo_layout.addWidget(self.version_label)

        # splash screen pogressbar
        self.progressBar = QProgressBar(self.frame)
        self.progressBar.resize(self.width() - 10, 4)
        self.progressBar.move(0, 220)
        self.progressBar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.progressBar.setTextVisible(False)
        self.progressBar.setRange(0, self.splashc.n)
        self.progressBar.setValue(20)
