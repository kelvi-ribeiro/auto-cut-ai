from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QComboBox, 
                             QPushButton, QCheckBox, QVBoxLayout, QFormLayout, 
                             QFileDialog, QDoubleSpinBox, QSpinBox, QMessageBox)
from core.VideoProcessingThread import VideoProcessingThread
import core.manager_api as manager
from view.loading_screen import LoadingScreen
from view.component_generation import generate_icon

class VideoEditionConfigForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Configuração da Edição')
        self.setGeometry(100, 100, 400, 600)

        self.setWindowIcon(generate_icon('https://img.icons8.com/?size=100&id=UWtgn2Fl5iGg&format=png&color=000000'))

        layout = QVBoxLayout()
        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(15)

        self.configure_widgets()

        self.form_layout.addRow('Tipo de Reconhecimento:', self.recognition_type)
        self.form_layout.addRow('Selecione o Diretório dos Vídeos:', self.videos_path_dir)
        self.form_layout.addRow('', self.browse_button)
        self.form_layout.addRow('Segundos de Corte:', self.seconds_to_cut)
        self.form_layout.addRow('Utilizar Processamento Prévio:', self.use_saved_result_file)
        self.form_layout.addRow('Inverter Vídeo:', self.flip)
        self.form_layout.addRow('Nome do Vídeo Exportado:', self.final_video_name)
        self.form_layout.addRow('Notificação por E-mail:', self.use_email_notification)
        self.form_layout.addRow(self.from_email_label, self.from_email)
        self.form_layout.addRow(self.from_email_password_label, self.from_email_password)
        self.form_layout.addRow(self.recipient_email_label, self.recipient_email)
        self.form_layout.addRow(self.keyword_label, self.keyword)
        self.form_layout.addRow(self.minimum_confidence_label, self.minimum_confidence)
        self.form_layout.addRow(self.whisper_language_label, self.whisper_language)
        self.form_layout.addRow(self.whisper_model_label, self.whisper_model)
        self.form_layout.addRow('', self.submit_button)

        layout.addLayout(self.form_layout)
        layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(layout)

        self.update_fields()
    
    def configure_widgets(self):
        self.recognition_type = QComboBox()
        recognition_items = [('Reconhecimento por cor da tela', 'screen_colorn'), 
                             ('Reconhecimento por gesto', 'gesture_recognition'), 
                             ('Reconhecimento por voz', 'voice_recognition')]
        for text, value in recognition_items:
            self.recognition_type.addItem(text, value)
        self.recognition_type.currentIndexChanged.connect(self.update_fields)

        self.videos_path_dir = QLineEdit()
        self.browse_button = QPushButton('Procurar...')
        self.browse_button.setIcon(generate_icon('https://img.icons8.com/?size=1000&id=Cw4a9E3dA73N&format=png&color=000000'))
        self.browse_button.clicked.connect(self.browse_directory)

        self.seconds_to_cut = QSpinBox()
        self.seconds_to_cut.setRange(0, 10000)

        self.keyword = QLineEdit()
        self.keyword_label = QLabel("Palavra chave:")

        self.minimum_confidence = QDoubleSpinBox()
        self.minimum_confidence.setRange(0.0, 1.0)
        self.minimum_confidence.setSingleStep(0.01)
        self.minimum_confidence_label = QLabel("Confiança mínima:")

        self.whisper_language = QComboBox()
        whisper_language_items = [('Português', 'pt'), ('Inglês', 'en')]
        for text, value in whisper_language_items:
            self.whisper_language.addItem(text, value)
        self.whisper_language_label = QLabel("Idioma:")

        self.whisper_model = QComboBox()
        whisper_model_items = [('Tiny', 'tiny'), ('Base', 'base'), ('Small', 'small'), 
                               ('Medium', 'medium'), ('Large', 'large'), 
                               ('Large-v2', 'large-v2'), ('Large-v3', 'large-v3')]
        for text, value in whisper_model_items:
            self.whisper_model.addItem(text, value)
        self.whisper_model_label = QLabel("Modelo Whisper:")

        self.flip = QCheckBox()

        self.use_saved_result_file = QCheckBox()

        self.final_video_name = QLineEdit()

        self.use_email_notification = QCheckBox()
        self.use_email_notification.stateChanged.connect(self.update_fields)

        self.from_email = QLineEdit()
        self.from_email_label = QLabel("Email do Remetente:")

        self.from_email_password = QLineEdit()
        self.from_email_password_label = QLabel("Senha email do Remetente:")

        self.recipient_email = QLineEdit()
        self.recipient_email_label = QLabel("Email destinatário:")

        self.submit_button = QPushButton('Processar')
        self.submit_button.clicked.connect(self.on_submit)

        self.setStyleSheet("""
            QWidget {
                font-family: Arial, sans-serif;
            }
            QLabel {
                font-size: 12px;
                padding: 5px;
            }
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {
                padding: 5px;
                font-size: 12px;
            }
            QPushButton {
                background-color: #28a745;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QCheckBox {
                font-size: 12px;
            }
        """)

    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Selecione a pasta")
        if directory:
            self.videos_path_dir.setText(directory)

    def update_fields(self):
        self.handle_recognition_type_change()
        self.use_email_notification_change()

    def handle_recognition_type_change(self):
        recognition_type_value = self.recognition_type.currentData()
        is_voice_recognition = recognition_type_value == 'voice_recognition'
        self.keyword_label.setVisible(is_voice_recognition)
        self.keyword.setVisible(is_voice_recognition)
        self.minimum_confidence_label.setVisible(is_voice_recognition)
        self.minimum_confidence.setVisible(is_voice_recognition)
        self.whisper_language_label.setVisible(is_voice_recognition)
        self.whisper_language.setVisible(is_voice_recognition)
        self.whisper_model_label.setVisible(is_voice_recognition)
        self.whisper_model.setVisible(is_voice_recognition)

    def use_email_notification_change(self):
        is_use_email = self.use_email_notification.isChecked()
        self.from_email.setVisible(is_use_email)
        self.from_email_label.setVisible(is_use_email)
        self.from_email_password.setVisible(is_use_email)
        self.from_email_password_label.setVisible(is_use_email)
        self.recipient_email.setVisible(is_use_email)
        self.recipient_email_label.setVisible(is_use_email)

    def on_submit(self):
        errors = []

        if not self.videos_path_dir.text():
            errors.append('A pasta é obrigatória.')

        if self.keyword.isVisible() and not self.keyword.text():
            errors.append('A palavra chave é obrigatória para o reconhecimento por voz.')

        if not self.final_video_name.text():
            errors.append('Nome do vídeo exportado é obrigatório.')

        if self.use_email_notification.isChecked():
            if not self.from_email.text():
                errors.append('Email remetente é obrigatório para a notificação por email.')
            if not self.from_email_password.text():
                errors.append('Senha do email remetente é obrigatória para a notificação por email.')
            if not self.recipient_email.text():
                errors.append('Email destinatário é obrigatório para a notificação por email.')

        if errors:
            QMessageBox.critical(self, 'Erros:', '\n'.join(errors), QMessageBox.Ok, QMessageBox.Ok)
        else:
            config = {
                "recognition_type": self.recognition_type.currentData(),
                "videos_path_dir": self.videos_path_dir.text(),
                "seconds_to_cut": self.seconds_to_cut.value(),
                "keyword": self.keyword.text() if self.keyword.isVisible() else '',
                "minimum_confidence": self.minimum_confidence.value() if self.minimum_confidence.isVisible() else 0.0,
                "whisper_language": self.whisper_language.currentData() if self.whisper_language.isVisible() else '',
                "whisper_model": self.whisper_model.currentData() if self.whisper_model.isVisible() else '',
                "flip": self.flip.isChecked(),
                "use_saved_result_file": self.use_saved_result_file.isChecked(),
                "final_video_name": self.final_video_name.text(),
                "use_email_notification": self.use_email_notification.isChecked(), 
                "from_email": self.from_email.text(), 
                "from_email_password": self.from_email_password.text(), 
                "recipient_email": self.recipient_email.text(), 
            }

            # TODO remover QMessageBox.information(self, 'Edição Configurada!', 'O seu vídeo já está sendo processado...', QMessageBox.Ok, QMessageBox.Ok)
            self.close()
            self.processing_thread = VideoProcessingThread(config, manager)
            self.loading_screen = LoadingScreen()
            self.loading_screen.show()
            self.repaint()  # Ensure the loading screen is visible immediately
            self.processing_thread.finished.connect(self.on_processing_finished)
            self.processing_thread.start()

    def on_processing_finished(self):
        self.loading_screen.close()
        QMessageBox.information(self, 'Processamento Concluído', 'O vídeo foi processado com sucesso!', QMessageBox.Ok, QMessageBox.Ok)
        self.close()
