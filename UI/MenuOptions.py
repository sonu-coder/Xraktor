from PyQt6.QtWidgets import QPushButton
from UI.MainWindow import MainApp
from PyQt6.QtWidgets import QPushButton

from UI.MainWindow import MainApp


def MenuOptions(mainWindow: MainApp):
    mainWindow.export_pdf = QPushButton('Export PDF')
    mainWindow.export_pdf.setFixedSize(140, 40)
    mainWindow.export_pdf.setObjectName('export_pdf_button')
    mainWindow.left_layout.addWidget(mainWindow.export_pdf)
