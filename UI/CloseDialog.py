from PyQt6.QtCore import QSize, Qt, QPoint
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QDialog, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QGraphicsDropShadowEffect

from Utils.Const import CloseDialogInfo
from Utils.StyleSheets.DialogStyle import DialogStyle


class CloseDialog(QDialog):

    def __init__(self, mcontroller):
        super().__init__()
        self.mcontroller = mcontroller
        self.setWindowTitle("Warning")
        # self.setFixedSize(QSize(500, 200))

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet(DialogStyle)

        self.dialog_widget = QWidget(self)
        self.dialog_widget.setObjectName('dialog_widget')
        self.dialog_widget.setContentsMargins(0, 0, 0, 0)
        self.dialog_widget.setFixedSize(QSize(500, 200))
        effect = QGraphicsDropShadowEffect(self.dialog_widget)
        effect.setBlurRadius(50)
        effect.setColor(Qt.GlobalColor.black)
        effect.setOffset(0, 0)
        effect.setEnabled(True)
        self.dialog_widget.move(50, 50)
        self.dialog_widget.setGraphicsEffect(effect)

        self.layout = QVBoxLayout(self.dialog_widget)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.title_widget = QWidget(self)
        self.title_widget.setObjectName('title_widget')
        self.title_widget.resize(500, 50)
        self.title_layout = QHBoxLayout(self.title_widget)
        self.title_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.title_icon = QLabel()
        self.title_pixmap = QPixmap('images/logo_24_blue.png')
        self.title_icon.setPixmap(self.title_pixmap)
        self.title_layout.addWidget(self.title_icon)

        self.title_layout.addSpacing(1)
        self.dialog_title = QLabel("Warning")
        self.dialog_title.setObjectName('dialog_title')
        self.title_layout.addWidget(self.dialog_title)
        self.title_layout.addSpacing(10)
        self.layout.addWidget(self.title_widget)

        self.dialog_body_layout = QHBoxLayout()
        self.dialog_body_layout.setAlignment(Qt.AlignmentFlag.AlignLeading)

        self.dialog_body_layout.setContentsMargins(10, 10, 10, 10)

        self.dialog_body_icon = QLabel()
        self.dialog_body_icon.setScaledContents(True)
        self.dialog_body_icon.setFixedSize(64, 64)
        self.dialog_body_pixmap = QPixmap()
        self.dialog_body_pixmap.load('images/warning.png')
        self.dialog_body_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dialog_body_icon.setPixmap(self.dialog_body_pixmap)
        self.dialog_body_layout.addWidget(self.dialog_body_icon)
        self.layout.addLayout(self.dialog_body_layout, 2)

        self.dialog_body_layout.addSpacing(10)
        self.dialog_msg = QLabel(CloseDialogInfo)
        self.dialog_msg.setFixedSize(QSize(400, 80))
        self.dialog_msg.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.dialog_msg.setObjectName('dialog_msg')
        self.dialog_msg.setWordWrap(True)
        self.dialog_body_layout.addWidget(self.dialog_msg)

        self.button_layout = QHBoxLayout()
        self.button_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.button_layout.setContentsMargins(0, 0, 10, 10)

        self.buttonBox = QPushButton('Yes, Exit')
        self.buttonBox.setObjectName('yes_button')
        self.buttonBox.setFixedSize(100, 40)
        self.buttonBox.clicked.connect(self.closeWindow)
        self.button_layout.addWidget(self.buttonBox)
        self.layout.addLayout(self.button_layout)

        self.buttonBox = QPushButton('No')
        self.buttonBox.setObjectName('no_button')
        self.buttonBox.setFixedSize(100, 40)
        self.buttonBox.clicked.connect(self.close)
        self.button_layout.addWidget(self.buttonBox)
        self.layout.addLayout(self.button_layout)

    def closeWindow(self):
        self.close()
        self.mcontroller.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.__press_pos = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.__press_pos = QPoint()

    def mouseMoveEvent(self, event):
        if not self.__press_pos.isNull():
            self.move(self.pos() + (event.pos() - self.__press_pos))
