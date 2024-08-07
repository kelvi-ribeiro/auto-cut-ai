from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QComboBox, 
                             QPushButton, QCheckBox, QVBoxLayout, QFormLayout, 
                             QFileDialog, QDoubleSpinBox, QSpinBox, QMessageBox)
from core.VideoProcessingThread import VideoProcessingThread
import core.manager_api as manager

class VideoEditionConfigForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Configuração da edição')
        self.setGeometry(100, 100, 400, 500)

        # Layouts
        layout = QVBoxLayout()
        self.form_layout = QFormLayout()

        self.recognition_type = QComboBox()
        recognition_items = [('Reconhecimento por voz', 'voice_recognition'), 
                             ('Reconhecimento por gesto', 'gesture_recognition'), 
                             ('Reconhmecimento por cor da tela', 'screen_color')]
        for text, value in recognition_items:
            self.recognition_type.addItem(text, value)
        self.recognition_type.currentIndexChanged.connect(self.update_fields)

        self.videos_path_dir = QLineEdit()
        self.browse_button = QPushButton('Procurar...')
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

        self.submit_button = QPushButton('Processar')
        self.submit_button.clicked.connect(self.on_submit)

        self.form_layout.addRow('Tipo de reconhecimento:', self.recognition_type)
        self.form_layout.addRow('Selecione o directórios dos vídeos:', self.videos_path_dir)
        self.form_layout.addRow('', self.browse_button)
        self.form_layout.addRow('Segundos de corte:', self.seconds_to_cut)
        self.form_layout.addRow(self.keyword_label, self.keyword)
        self.form_layout.addRow(self.minimum_confidence_label, self.minimum_confidence)
        self.form_layout.addRow(self.whisper_language_label, self.whisper_language)
        self.form_layout.addRow(self.whisper_model_label, self.whisper_model)
        self.form_layout.addRow('Inverter vídeo:', self.flip)
        self.form_layout.addRow('Utilizar processamento prévio:', self.use_saved_result_file)
        self.form_layout.addRow('Nome do vídeo exportado:', self.final_video_name)
        self.form_layout.addRow('', self.submit_button)

        layout.addLayout(self.form_layout)
        self.setLayout(layout)

        self.update_fields()

    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Selecione a pasta")
        if directory:
            self.videos_path_dir.setText(directory)

    def update_fields(self):
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

    def on_submit(self):
        errors = []

        if not self.videos_path_dir.text():
            errors.append('A pasta é obrigatória.')

        if self.keyword.isVisible() and not self.keyword.text():
            errors.append('A palavra chave é obrigatória para o reconhecimento por voz.')

        if not self.final_video_name.text():
            errors.append('Nome do vídeo exportado é obrigatório.')

        if errors:
            QMessageBox.critical(self, 'Erros:', '\n'.join(errors))
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
                "final_video_name": self.final_video_name.text()
            }

            QMessageBox.information(self, 'Edição configurada!', 'O seu vídeo já está sendo processado...')

        self.processing_thread = VideoProcessingThread(config, manager)
        self.processing_thread.finished.connect(self.on_processing_finished)
        self.processing_thread.start()

    def on_processing_finished(self):
        QMessageBox.information(self, 'Processamento Concluído', 'O vídeo foi processado com sucesso!')
        self.close()

            