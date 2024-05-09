from PyQt6.QtCore import QSize, Qt, QPoint
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QDialog, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QGraphicsDropShadowEffect, \
    QSpacerItem, QSizePolicy, QPlainTextEdit

from Utils.Const import AboutInfo
from Utils.StyleSheets.AboutDialogStyle import AboutDialogStyle
from Utils.StyleSheets.ScrollBarStyle import VScrollStyle


class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()
        # self.setFixedSize(QSize(500, 400))

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet(AboutDialogStyle)

        self.dialog_widget = QWidget(self)
        self.dialog_widget.setObjectName('dialog_widget')
        self.dialog_widget.setContentsMargins(0,0,0,0)
        self.dialog_widget.setFixedSize(QSize(500, 350))
        effect = QGraphicsDropShadowEffect(self.dialog_widget)
        effect.setBlurRadius(50)
        effect.setColor(Qt.GlobalColor.black)
        effect.setOffset(0,0)
        effect.setEnabled(True)
        self.dialog_widget.move(50,50)
        self.dialog_widget.setGraphicsEffect(effect)

        self.layout = QVBoxLayout(self.dialog_widget)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setContentsMargins(0,0,0,0)

        self.title_widget = QWidget(self)
        self.title_widget.setObjectName('title_widget')
        self.title_widget.setFixedSize(500,50)
        self.title_layout = QHBoxLayout(self.title_widget)
        self.title_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.title_icon = QLabel()
        self.title_pixmap = QPixmap('images/logo_24_blue.png')
        self.title_icon.setPixmap(self.title_pixmap)
        self.title_layout.addWidget(self.title_icon)

        self.title_layout.addSpacing(1)
        self.dialog_title = QLabel("About")
        self.dialog_title.setObjectName('dialog_title')
        self.title_layout.addWidget(self.dialog_title)
        self.title_layout.addSpacing(10)
        self.closeButton = QPushButton('r')
        self.closeButton.setObjectName('close_button')
        self.closeButton.clicked.connect(self.close)
        self.title_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.title_layout.addWidget(self.closeButton)
        self.layout.addWidget(self.title_widget)

        self.dialog_msg = QPlainTextEdit(AboutInfo)
        self.dialog_msg.setContentsMargins(10, 10, 10, 10)
        self.dialog_msg.setFixedSize(500, 300)

        self.dialog_msg.setObjectName('dialog_msg')
        self.dialog_msg.setVerticalScrollBar(self.dialog_msg.setStyleSheet(VScrollStyle))
        self.dialog_msg.setLineWrapMode(self.dialog_msg.LineWrapMode.WidgetWidth)
        self.dialog_msg.setReadOnly(True)
        self.layout.addWidget(self.dialog_msg)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.__press_pos = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.__press_pos = QPoint()

    def mouseMoveEvent(self, event):
        if not self.__press_pos.isNull():
            self.move(self.pos() + (event.pos() - self.__press_pos))
