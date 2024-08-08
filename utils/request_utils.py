import requests

from core.notification.notification_system import NotificationSystem

notification_system = NotificationSystem()

def get_content(url):    
    try:
        response = requests.get(url)
        response.raise_for_status() 
        return response.content
    except Exception as e:
        notification_system.notify(f"An issue occurred while trying to access the URL '{url}'", e)
        return ""