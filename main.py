
import sys
from PyQt5.QtWidgets import QApplication
from core.notification.notification_client import NotificationClient
from view.video_edition_config_form import VideoEditionConfigForm
from core.notification.notification_system import NotificationSystem

def main():
    notification_system = NotificationSystem()
    printer_client = NotificationClient(print)
    notification_system.add_client(printer_client)
    app = QApplication(sys.argv)
    form = VideoEditionConfigForm()
    form.show()
    sys.exit(app.exec_()) 
if __name__ == "__main__":
    main()