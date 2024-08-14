
import sys
from PyQt5.QtWidgets import QApplication
from view.video_edition_config_form import VideoEditionConfigForm
from core.notification.notification_system import NotificationSystem

def main():
    notification_system = NotificationSystem()
    notification_system.notification_message_signal.connect(print)
    app = QApplication(sys.argv)
    form = VideoEditionConfigForm()
    form.show()
    sys.exit(app.exec_()) 
if __name__ == "__main__":
    main()