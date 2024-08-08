
import sys
from PyQt5.QtWidgets import QApplication
from view.video_edition_config_form import VideoEditionConfigForm

def main():
    app = QApplication(sys.argv)
    form = VideoEditionConfigForm()
    form.show()
    sys.exit(app.exec_()) 
if __name__ == "__main__":
    main()