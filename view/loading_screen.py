from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QProgressBar, QWidget
from core.notification.notification_client import NotificationClient
from core.notification.notification_system import NotificationSystem
from view.component_generation import generate_icon

notification_system = NotificationSystem()

class LoadingScreen(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Processando o vídeo...")
        self.setWindowIcon(generate_icon('https://img.icons8.com/?size=100&id=5dPeBRbvJRr1&format=png&color=000000'))
        self.setFixedSize(400, 300)  

        self.message_area = QTextEdit()
        self.message_area.setReadOnly(True)

        self.details_button = QPushButton("Ocultar detalhes")
        self.details_button.clicked.connect(self.toggle_details)

        layout = QVBoxLayout()
        layout.addWidget(self.message_area)
        layout.addWidget(self.details_button)

        self.setLayout(layout)
        notification_system.add_client(NotificationClient(self.add_message))


    def toggle_details(self):
        if self.message_area.isVisible():
            self.message_area.setVisible(False)
            self.details_button.setText("Mostrar Detalhes")
        else:
            self.message_area.setVisible(True)
            self.details_button.setText("Ocultar Detalhes")

    def add_message(self, message):
        self.message_area.append(message)