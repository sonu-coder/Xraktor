from PyQt6.QtCore import pyqtSignal, QThread


class WorkerThread(QThread):
    # Create a counter thread
    change_value = pyqtSignal(int)

    def run(self):
        pass
