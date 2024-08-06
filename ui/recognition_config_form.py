from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QComboBox, 
                             QPushButton, QCheckBox, QVBoxLayout, QFormLayout, 
                             QFileDialog, QDoubleSpinBox, QSpinBox, QMessageBox)

class RecognitionConfigForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PyQt5 Form Example')
        self.setGeometry(100, 100, 400, 500)

        # Layouts
        layout = QVBoxLayout()
        self.form_layout = QFormLayout()

        # Recognition Type
        self.recognition_type = QComboBox()
        recognition_items = [('Voice Recognition', 'voice_recognition'), 
                             ('Gesture Recognition', 'gesture_recognition'), 
                             ('Screen Color', 'screen_color')]
        for text, value in recognition_items:
            self.recognition_type.addItem(text, value)
        self.recognition_type.currentIndexChanged.connect(self.update_fields)

        # Videos Path Directory
        self.videos_path_dir = QLineEdit()
        self.browse_button = QPushButton('Browse')
        self.browse_button.clicked.connect(self.browse_directory)

        # Seconds to Cut
        self.seconds_to_cut = QSpinBox()
        self.seconds_to_cut.setRange(0, 10000)

        # Keyword
        self.keyword = QLineEdit()
        self.keyword_label = QLabel("Keyword:")

        # Minimum Confidence
        self.minimum_confidence = QDoubleSpinBox()
        self.minimum_confidence.setRange(0.0, 1.0)
        self.minimum_confidence.setSingleStep(0.01)
        self.minimum_confidence_label = QLabel("Minimum Confidence:")

        # Whisper Language
        self.whisper_language = QComboBox()
        whisper_language_items = [('Portuguese', 'pt'), ('English', 'en')]
        for text, value in whisper_language_items:
            self.whisper_language.addItem(text, value)
        self.whisper_language_label = QLabel("Whisper Language:")

        # Whisper Model
        self.whisper_model = QComboBox()
        whisper_model_items = [('Tiny', 'tiny'), ('Base', 'base'), ('Small', 'small'), 
                               ('Medium', 'medium'), ('Large', 'large'), 
                               ('Large-v2', 'large-v2'), ('Large-v3', 'large-v3')]
        for text, value in whisper_model_items:
            self.whisper_model.addItem(text, value)
        self.whisper_model_label = QLabel("Whisper Model:")

        # Flip
        self.flip = QCheckBox()

        # Use Saved Result File
        self.use_saved_result_file = QCheckBox()

        # Final Video Name
        self.final_video_name = QLineEdit()

        # Submit Button
        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.on_submit)

        # Add widgets to form layout
        self.form_layout.addRow('Recognition Type:', self.recognition_type)
        self.form_layout.addRow('Videos Path Directory:', self.videos_path_dir)
        self.form_layout.addRow('', self.browse_button)
        self.form_layout.addRow('Seconds to Cut:', self.seconds_to_cut)
        self.form_layout.addRow(self.keyword_label, self.keyword)
        self.form_layout.addRow(self.minimum_confidence_label, self.minimum_confidence)
        self.form_layout.addRow(self.whisper_language_label, self.whisper_language)
        self.form_layout.addRow(self.whisper_model_label, self.whisper_model)
        self.form_layout.addRow('Flip:', self.flip)
        self.form_layout.addRow('Use Saved Result File:', self.use_saved_result_file)
        self.form_layout.addRow('Final Video Name:', self.final_video_name)
        self.form_layout.addRow('', self.submit_button)

        # Add form layout to main layout
        layout.addLayout(self.form_layout)
        self.setLayout(layout)

        # Initial update of fields
        self.update_fields()

    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
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

        # Validate Videos Path Directory
        if not self.videos_path_dir.text():
            errors.append('Videos Path Directory is required.')

        # Validate Keyword
        if self.keyword.isVisible() and not self.keyword.text():
            errors.append('Keyword is required for voice recognition.')

        # Validate Final Video Name
        if not self.final_video_name.text():
            errors.append('Final Video Name is required.')

        if errors:
            QMessageBox.critical(self, 'Form Errors', '\n'.join(errors))
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
            print(config)
            QMessageBox.information(self, 'Form Submitted', 'Form data has been submitted successfully!')
    def get_form_data(self):
        return {
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