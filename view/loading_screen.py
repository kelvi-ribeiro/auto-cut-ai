from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout
from PyQt5.QtGui import QMovie
from view.component_generation import generate_icon
from PyQt5.QtCore import Qt

class LoadingScreen(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Processando o vídeo...")
        self.setWindowIcon(generate_icon('https://img.icons8.com/?size=100&id=5dPeBRbvJRr1&format=png&color=000000'))
        self.setFixedSize(200, 100)
        layout = QVBoxLayout()
        self.label = QLabel(self)
        layout.addWidget(self.label)

        # # Set up the loading animation
        # self.movie = QMovie("loading.gif")  # Path to your animated GIF
        # self.label.setMovie(self.movie)
        # self.movie.start()
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setLayout(layout)