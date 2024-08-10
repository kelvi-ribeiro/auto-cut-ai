from PyQt5.QtCore import pyqtSignal, QObject

class NotificationSystem(QObject):
    progress_signal = pyqtSignal(str, int)
    _instance = None

    def __init__(self):
        super().__init__()
        self.clients = []

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(NotificationSystem, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def add_client(self, notification_client):
        self.clients.append(notification_client)
    
    def notify(self, message):
        for client in self.clients:
            client.action(message)

    def notify_progress_bar(self, phase, percentage):
        self.progress_signal.emit(phase, percentage)  