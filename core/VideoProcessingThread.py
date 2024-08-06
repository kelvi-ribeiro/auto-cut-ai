from PyQt5.QtCore import QThread, pyqtSignal

class VideoProcessingThread(QThread):
    finished = pyqtSignal()

    def __init__(self, config, manager, parent=None):
        super().__init__(parent)
        self.config = config
        self.manager = manager

    def run(self):
        self.manager.generate_final_video(self.config)
        self.finished.emit()
