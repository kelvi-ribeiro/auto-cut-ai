
import sys
import core.manager_api as manager
from PyQt5.QtWidgets import QApplication
from ui.recognition_config_form import RecognitionConfigForm

def main():
    app = QApplication(sys.argv)
    form = RecognitionConfigForm()
    form.show()
    sys.exit(app.exec_()) 
if __name__ == "__main__":
    main()