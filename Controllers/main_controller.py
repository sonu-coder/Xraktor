import os

from PyQt6.QtCore import QFileInfo
from PyQt6.QtPrintSupport import QPrinter
from PyQt6.QtWidgets import QFileDialog

from Controllers.Extraktor import Extraktor as ext
from UI.AboutDialog import AboutDialog
from UI.CloseDialog import CloseDialog
from UI.CustomDialog import CustomDialog
from UI.MainWindow import MainApp
from UI.SaveDialog import SaveThread
from Utils.Const import languages
from Utils.Enum import RightLayout


class MainController:
    def __init__(self, mwindow: MainApp):
        super().__init__()
        self.mwindow = mwindow
        self.explorer = QFileDialog()
        self.dialog = CustomDialog()
        self.about_dialog = AboutDialog()

    def closeWindow(self):
        self.closeDialog()
        # self.mwindow.close()

    def closeAboutDialog(self):
        self.about_dialog.close()

    def minimizeWindow(self):
        self.mwindow.showMinimized()

    def centerWindow(self):
        qr = self.mwindow.frameGeometry()
        cp = self.mwindow.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.mwindow.move(qr.topLeft())

    def selectFileBox(self, i):
        if i == 0:
            self.mwindow.openfile = True
            self.mwindow.multiExport = False
            self.mwindow.export_options.hide()
        else:
            self.mwindow.openfile = False

            self.mwindow.export_options.show()

    def selectExportOptions(self, i):
        if i == 0:
            self.mwindow.multiExport = False
        else:
            self.mwindow.multiExport = True

    def selectLang(self, i):
        os.environ['XRAKT_LANGUAGE'] = languages[i]

    # Function to init. Threads
    def initThread(self):
        self.extraktThread = ext(self.mwindow)

        # Attaching thread instance to functions
        self.extraktThread.extraktProg.connect(self.extraktThread.extraktProgress)
        self.extraktThread.extraktDone.connect(self.extraktThread.done)

        self.saveThread = SaveThread(self)
        self.saveThread.exportProg.connect(self.saveThread.exportProgress)
        self.saveThread.exportDone.connect(self.saveThread.done)
        self.saveThread.exportDialog.connect(self.saveThread.showDialog)

    # Extrakt function
    def extrakt_thread(self):
        self.extraktThread.extrakt()

    # Function to control layout visibility
    def hideShow(self, status: RightLayout):
        match status:
            case status.EMPTY:
                self.mwindow.search_frame.show()
                self.mwindow.plain_text.hide()
                self.mwindow.extract_frame.hide()

            case status.RESULT:
                self.mwindow.search_frame.hide()
                self.mwindow.plain_text.show()
                self.mwindow.extract_frame.hide()
                # self.disableButton(enabled=False)

            case status.SEARCH:
                self.mwindow.search_frame.hide()
                self.mwindow.plain_text.hide()
                self.mwindow.extract_frame.show()

    # Function to open folder or file location and make selection
    def openExplorer(self):
        if not self.mwindow.openfile and not self.mwindow.isExtracting:
            folderName = self.explorer.getExistingDirectory(self.mwindow, 'Open Folder')
            self.mwindow.env_path.setText(folderName)
        elif self.mwindow.openfile and not self.mwindow.isExtracting:
            fileName = self.explorer.getOpenFileName(self.mwindow, 'Open File',
                                                     filter="Images (*.jpg *.jpeg *.png *.gif)")
            self.mwindow.env_path.setText(fileName[0])

    # Function to Save resultant extracted text to a Text file
    def saveText(self):
        try:
            if self.mwindow.isExtracting: return
            if not self.mwindow.plain_text.toPlainText(): raise Exception('EmptyFileError',
                                                                          'Nothing to save in a text file.')
            # Condition to check export options
            if self.mwindow.multiExport:
                self.filefolder = self.explorer.getExistingDirectory(self.mwindow, 'Open Folder')  # Folder path

                if not self.mwindow.extractResults: raise Exception('EmptyFileError',
                                                                    'Nothing to save in a text files.')

                if self.filefolder:
                    self.files_list = self.mwindow.extractResults
                    self.mwindow.isPdf = False
                    self.saveThread.startSaveThread()

            else:
                filename = self.explorer.getSaveFileName(self.mwindow, "Save File")[0]
                # print(filename)

                if filename.strip():
                    if QFileInfo(filename).suffix() == "": filename += ".txt"
                    f = open(filename, 'w')
                    with f:
                        text = self.mwindow.plain_text.toPlainText()
                        f.write(text)

                    self.dialog.dialog_title.setText("File Saved")
                    self.dialog.dialog_msg.setText('File Saved Successfully')
                    self.dialog.exec()
        except Exception as err:
            self.dialog.dialog_title.setText("Warning")
            self.dialog.dialog_msg.setText(err.args[1])
            self.dialog.exec()

    def exportPdf(self):
        try:
            if self.mwindow.isExtracting: return
            if not self.mwindow.plain_text.toPlainText(): raise Exception('EmptyFileError',
                                                                          'Cannot export empty PDF file. Please extract text first.')

            if self.mwindow.multiExport:
                self.filefolder = self.explorer.getExistingDirectory(self.mwindow, 'Open Folder')  # Folder path

                if not self.mwindow.extractResults: raise Exception('EmptyFileError',
                                                                    'Nothing to save in a text files.')
                if self.filefolder:
                    self.files_list = self.mwindow.extractResults
                    self.mwindow.isPdf = True
                    self.saveThread.startSaveThread()

            else:
                filename, _ = self.explorer.getSaveFileName(
                    self.mwindow, "Export PDF", None, "PDF files (.pdf);;All Files()"
                )

                if filename:
                    if QFileInfo(filename).suffix() == "": filename += ".pdf"
                    printer = QPrinter(QPrinter.PrinterMode.HighResolution)
                    printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
                    printer.setOutputFileName(filename)
                    self.mwindow.plain_text.document().print(printer)
                    self.dialog.dialog_title.setText("Exported")
                    self.dialog.dialog_msg.setText('Pdf Exported Successfully')
                    self.dialog.exec()

        except Exception as err:
            self.dialog.dialog_title.setText("Warning")
            self.dialog.dialog_msg.setText(err.args[1])
            self.dialog.exec()

    def disableButton(self, enabled=True):
        if enabled:
            self.mwindow.extrakt_button.setDisabled(True)
            self.mwindow.about_btn.setDisabled(True)
            self.mwindow.export_pdf.setDisabled(True)
            self.mwindow.export_options.setDisabled(True)
            self.mwindow.save_txt_button.setDisabled(True)
            self.mwindow.browse_button.setDisabled(True)
            self.mwindow.file_folder.setDisabled(True)
        else:
            self.mwindow.extrakt_button.setEnabled(True)
            self.mwindow.about_btn.setEnabled(True)
            self.mwindow.export_pdf.setEnabled(True)
            self.mwindow.export_options.setEnabled(True)
            self.mwindow.save_txt_button.setEnabled(True)
            self.mwindow.browse_button.setEnabled(True)
            self.mwindow.file_folder.setEnabled(True)

    def closeDialog(self):
        dialog = CloseDialog(self.mwindow)
        dialog.exec()

    def openAbout(self):
        self.about_dialog.exec()
