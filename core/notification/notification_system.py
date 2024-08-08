from core.notification.notification_client import NotificationClient

class NotificationSystem:
    _instance = None

    def __init__(self):
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
        
    