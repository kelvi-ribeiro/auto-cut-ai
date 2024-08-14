from PyQt5.QtCore import pyqtSignal, QObject

class NotificationSystem(QObject):
    progress_signal = pyqtSignal(str, int)
    notification_message_signal = pyqtSignal(str)
    _instance = None

    def __init__(self):
        super().__init__()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(NotificationSystem, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def notify(self, message):
        self.notification_message_signal.emit(message)  

    def notify_progress_bar(self, phase, percentage):
        self.progress_signal.emit(phase, percentage)  