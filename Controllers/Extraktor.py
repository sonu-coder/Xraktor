import os

import pytesseract
from PyQt6.QtCore import QFileInfo, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap
from tesseract_pack import data_here

from UI.CustomDialog import CustomDialog
from Utils.Const import separator
from Utils.Enum import RightLayout


class Extraktor(QThread):
    # Initializing signals
    sig = pyqtSignal()
    extraktProg = pyqtSignal(int)
    extraktDone = pyqtSignal()

    def __init__(self, mainapp):

        QThread.__init__(self)  # Initializing QThread class

        self.mainApp = mainapp  # Initializing MainApp instance
        self.dialog = CustomDialog()
        self.text = ""
        self.extracting = False

    def __del__(self):
        self.wait()

    # Extracting text from multiple files
    def run(self):
        try:
            for i, file in enumerate(self.mainApp.files_list):
                self.mainApp.extract_text_1.setText('Extracting from:\n' + file)
                ext_text = pytesseract.image_to_string(r'{}/{}'.format(self.root, file))

                if ext_text.strip():
                    self.mainApp.extractResults[file] = ext_text
                    self.text += separator
                    self.text += '{}. '.format(i + 1) + file + '\n\n'
                    self.text += ext_text
                    self.mainApp.progressValue = i + 1
                    self.mainApp.fileProgress.setValue(self.mainApp.progressValue)

                    self.extraktProg.emit(i)  # Calling extraktProgress function to update the progress
                elif len(self.mainApp.files_list) == 1 and not ext_text.strip():
                    self.text = "No text found or recognized to extract from {}".format(file)
            self.extraktDone.emit()  # Calling done() function to complete extraction

        except (Exception, pytesseract.pytesseract.TesseractError) as error:
            # print(str(error[1]))
            self.showError(error)
        # self.showError("oops!!! something went wrong.Cannot extract from file")

    # Resetting All tooltips and enabling all buttons
    def resetAll(self):
        self.mainApp.isExtracting = False
        self.mainApp.mcontrol.disableButton(False)
        self.mainApp.browse_button.setToolTip('Select one or more files')
        self.mainApp.save_txt_button.setToolTip('Save result in a single or multiple text files.')
        self.mainApp.export_pdf.setToolTip('Export result in single or multiple pdf files.')
        self.mainApp.extrakt_button.setToolTip('Click to start extraction.')

    # function to update the extraction progress
    def extraktProgress(self, i):
        self.mainApp.progressValue = i + 1
        self.mainApp.fileProgress.setValue(self.mainApp.progressValue)
        self.mainApp.extract_text_2.setText(
            '{} extracted out of {}'.format(self.mainApp.progressValue, self.totalFiles))
        self.mainApp.progressText.setText(
            '{}% completed'.format(int((self.mainApp.progressValue / self.totalFiles) * 100)))

    # function to set result after extraction
    def done(self):
        self.mainApp.plain_text.setPlainText(self.text)
        self.mainApp.mcontrol.hideShow(RightLayout.RESULT)
        self.mainApp.status_label1.setText('Status : Extraction Successful')
        self.resetAll()
        self.text = ''

    # Main Extrakt function called through class instance
    def extrakt(self):

        # condition to check if extraction is in progress
        if self.extracting:
            self.dialog.dialog_title.setText("Warning")
            self.dialog.dialog_msg.setText(
                "Extraction is in progress. Please try again after it is completed.")
            self.dialog.exec()
            return

        # Checking if file/folder path is selected
        if not self.mainApp.env_path.text():
            self.dialog.dialog_title.setText("Warning")
            self.dialog.dialog_msg.setText(
                "Please select one or multiple image files to extract text from it.")
            self.dialog.exec()
            return

        # Setting up Tooltips
        self.mainApp.browse_button.setToolTip('Cannot open as extraction in progress...')
        self.mainApp.save_txt_button.setToolTip('Cannot save text file as extraction in progress...')
        self.mainApp.export_pdf.setToolTip('Cannot export pdf file as extraction in progress...')
        self.mainApp.extrakt_button.setToolTip('Cannot extract as current extraction in progress...')

        self.mainApp.files_list = []
        self.mainApp.extractResults = {}
        try:
            self.mainApp.isExtracting = True

            # Path of tesseract offline lib
            pytesseract.pytesseract.tesseract_cmd = r'{}\tesseract'.format(data_here)
            if not os.environ.get('TESSDATA_PREFIX'):
                os.environ.setdefault('TESSDATA_PREFIX', r'{}\tessdata'.format(data_here))

            # Updating the layout to progress and disabling buttons
            self.mainApp.status_label1.setText('Status : Extracting...')
            self.mainApp.mcontrol.hideShow(RightLayout.SEARCH)
            self.mainApp.mcontrol.disableButton(True)

            # Condition to check if the single file to extract
            if self.mainApp.openfile:
                filePath = self.mainApp.env_path.text()
                self.root = os.path.dirname(filePath)
                fileName = os.path.basename(filePath)
                self.mainApp.files_list.append(fileName)
                self.totalFiles = 1
                self.mainApp.fileProgress.setMaximum(1)
                if filePath:
                    self.start()
                # self.text = pytesseract.image_to_string(r'{}'.format(self.mainApp.env_path.text()))
                #self.done()
            else:
                self.root = self.mainApp.env_path.text()
                files_dir = os.listdir(self.root)
                self.mainApp.files_list = [file for file in files_dir if
                                           QFileInfo(file).suffix() in ['jpg', 'jpeg', 'png', 'gif']]
                self.totalFiles = len(self.mainApp.files_list)
                self.mainApp.fileProgress.setMaximum(self.totalFiles)
                if self.mainApp.files_list:

                    # Calling the thread function to perform extraction in background
                    self.start()
                else:

                    # Show errors if folder has no images
                    self.dialog.dialog_title.setText("Error")
                    self.dialog.dialog_msg.setText('No images found in selected folder. Please select folder with '
                                                   'images.')
                    self.dialog.dialog_body_icon.setPixmap(QPixmap('images/error.png'))
                    self.dialog.exec()

        except (Exception, PermissionError, FileNotFoundError) as error:
            self.showError(error)

    def showError(self, error):
        self.mainApp.status_label1.setText('Status : Failed')
        self.mainApp.mcontrol.hideShow(RightLayout.EMPTY)
        self.resetAll()
        self.dialog.dialog_title.setText("An error occurred")
        self.dialog.dialog_msg.setText(
            str(error))
        self.dialog.exec()
