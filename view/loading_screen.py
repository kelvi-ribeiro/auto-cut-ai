import sys
import time
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QProgressBar, QLabel, QMessageBox
from core.notification.notification_system import NotificationSystem
from view.component_generation import generate_icon
from PyQt5.QtCore import Qt

notification_system = NotificationSystem()

class LoadingScreen(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Processando vídeo...")
        self.setWindowIcon(generate_icon('https://img.icons8.com/?size=100&id=5dPeBRbvJRr1&format=png&color=000000'))
        self.setFixedSize(400, 300)  
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
       

        self.message_area = QTextEdit()
        self.message_area.setReadOnly(True)

        self.details_button = QPushButton("Ocultar detalhes")
        self.details_button.clicked.connect(self.toggle_details)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        
        self.bold_label = QLabel(self)
        self.bold_label.setAlignment(Qt.AlignCenter) 

        layout = QVBoxLayout()
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.bold_label)
        layout.addWidget(self.message_area)
        layout.addWidget(self.details_button)

        self.setLayout(layout)
        notification_system.progress_signal.connect(self.update_progress_bar)
        notification_system.notification_message_signal.connect(self.add_message)

    def toggle_details(self):
        if self.message_area.isVisible():
            self.message_area.setVisible(False)
            self.details_button.setText("Mostrar Detalhes")
        else:
            self.message_area.setVisible(True)
            self.details_button.setText("Ocultar Detalhes")

    def add_message(self, message):
        self.message_area.append(message)

    def update_progress_bar(self, phase, percentage):
        self.progress_bar.setValue(percentage)
        self.bold_label.setText('<b>' + phase + '</b>')

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Confirmar', 'Isso vai encerrer o processamento do vídeo. Tem certeza de que deseja fechar?',
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()  
            sys.exit(0)
        else:
            event.ignore()  