import os

from PyQt6.QtCore import QSize, Qt, QPoint, QThread, pyqtSignal, QFileInfo, pyqtSlot
from PyQt6.QtGui import QPixmap, QMovie, QTextDocument
from PyQt6.QtPrintSupport import QPrinter
from PyQt6.QtWidgets import QDialog, QSpacerItem, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QWidget, \
    QGraphicsDropShadowEffect, QSizePolicy

from Utils.Const import CloseDialogInfo
from Utils.StyleSheets.DialogStyle import DialogStyle


class SaveDialog(QDialog):

    def __init__(self, mcontrol):
        super().__init__()
        self.mcontrol = mcontrol
        self.setWindowTitle("Exporting")
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
        self.dialog_title = QLabel("Exporting")
        self.dialog_title.setObjectName('dialog_title')
        self.title_layout.addWidget(self.dialog_title)
        self.title_layout.addSpacing(10)
        self.layout.addWidget(self.title_widget)

        self.dialog_body_layout = QHBoxLayout()
        self.dialog_body_layout.setAlignment(Qt.AlignmentFlag.AlignLeading)

        self.dialog_body_layout.setContentsMargins(10, 10, 10, 10)

        self.dialog_body_icon = QLabel()
        self.dialog_body_icon.setObjectName('search_img')
        self.dialog_body_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.movie = QMovie("images/save.gif")
        self.dialog_body_icon.setScaledContents(True)
        self.dialog_body_icon.setFixedSize(120, 120)
        self.movie.start()
        self.dialog_body_icon.setMovie(self.movie)
        self.dialog_body_layout.addWidget(self.dialog_body_icon)
        self.layout.addLayout(self.dialog_body_layout, 3)

        self.dialog_body_layout.addSpacing(10)
        self.dialog_msg = QLabel(CloseDialogInfo)
        self.dialog_msg.setFixedSize(QSize(400, 120))
        self.dialog_msg.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.dialog_msg.setObjectName('dialog_msg')
        self.dialog_msg.setWordWrap(True)
        self.dialog_body_layout.addWidget(self.dialog_msg)
        self.dialog_body_layout.addSpacerItem(
            QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.button_layout = QHBoxLayout()
        self.button_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.button_layout.setContentsMargins(0, 0, 10, 10)

        self.buttonBox = QPushButton('Browse files')
        self.buttonBox.setObjectName('no_button')
        self.buttonBox.setFixedSize(100, 40)
        self.buttonBox.clicked.connect(self.browseFiles)
        self.buttonBox.hide()
        self.button_layout.addWidget(self.buttonBox)
        self.layout.addLayout(self.button_layout)

        self.buttonBox2 = QPushButton('Close')
        self.buttonBox2.setObjectName('yes_button')
        self.buttonBox2.setFixedSize(100, 40)
        self.buttonBox2.clicked.connect(self.closeDialog)
        self.buttonBox2.hide()
        self.button_layout.addWidget(self.buttonBox2)
        self.layout.addLayout(self.button_layout)

    def closeDialog(self):
        movie = QMovie('images/save.gif')
        movie.start()
        self.dialog_body_icon.setMovie(movie)
        self.dialog_widget.setFixedSize(QSize(500, 200))
        self.dialog_body_icon.setFixedSize(120, 120)
        self.dialog_msg.setFixedSize(QSize(400, 120))
        self.buttonBox.hide()
        self.buttonBox2.hide()
        self.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.__press_pos = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.__press_pos = QPoint()

    def mouseMoveEvent(self, event):
        if not self.__press_pos.isNull():
            self.move(self.pos() + (event.pos() - self.__press_pos))

    def browseFiles(self):
        print(r'explorer /select,"{}"'.format(self.mcontrol.filefolder))
        os.system('start {}'.format(self.mcontrol.filefolder))


# Thread Class to perform update operation of QDialog
class SaveThread(QThread):
    exportProg = pyqtSignal(str)
    exportDone = pyqtSignal()
    exportDialog = pyqtSignal()

    def __init__(self, mcontroller):
        super().__init__()
        QThread.__init__(self)
        self.mcontroller = mcontroller
        self.save_dialog = SaveDialog(mcontroller)

    def __del__(self):
        self.wait()

    def run(self):
        self.exportDialog.emit()
        for filename, fileData in self.mcontroller.files_list.items():
            if self.mcontroller.mwindow.isPdf:
                finalFileName = ''
                if filename:
                    if QFileInfo(filename).suffix() in ['jpg', 'jpeg', 'png', 'gif']:
                        finalFileName = filename.split(QFileInfo(filename).suffix())[0] + "pdf"
                    if finalFileName:
                        filePath = "{}\{}".format(self.mcontroller.filefolder, finalFileName)
                        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
                        printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
                        printer.setOutputFileName(filePath)
                        textDoc = QTextDocument()
                        textDoc.setPlainText(fileData)
                        textDoc.print(printer)
                        self.sleep(2)
                        self.exportProg.emit(finalFileName)

            else:
                finalFileName = ''
                if filename:
                    if QFileInfo(filename).suffix() in ['jpg', 'jpeg', 'png', 'gif']:
                        finalFileName = filename.split(QFileInfo(filename).suffix())[0] + "txt"
                    if finalFileName:
                        filePath = "{}\{}".format(self.mcontroller.filefolder, finalFileName)
                        f = open(filePath, 'w')
                        with f:
                            f.write(fileData)
                        self.sleep(2)
                        self.exportProg.emit(finalFileName)

        self.sleep(2)
        self.exportDone.emit()

    @pyqtSlot()
    def showDialog(self):
        self.save_dialog.dialog_title.setText("Exporting")
        self.save_dialog.dialog_msg.setText('Initializing export...')
        self.save_dialog.exec()

    def exportProgress(self, file):
        self.save_dialog.dialog_msg.setText("Exporting... {}".format(file))

    def done(self):
        self.save_dialog.dialog_title.setText("Exported")
        self.save_dialog.dialog_msg.setText('Exported {} files successfully.'.format(len(self.mcontroller.files_list)))
        movie = QMovie('images/done.gif')
        movie.start()
        self.save_dialog.dialog_body_icon.setMovie(movie)
        self.save_dialog.dialog_widget.setFixedSize(QSize(500, 220))
        self.save_dialog.dialog_body_icon.setFixedSize(150, 150)
        self.save_dialog.dialog_msg.setFixedSize(QSize(400, 150))
        self.save_dialog.buttonBox.show()
        self.save_dialog.buttonBox2.show()
        # self.save_dialog.closeDialog()

    def startSaveThread(self):
        self.start()
