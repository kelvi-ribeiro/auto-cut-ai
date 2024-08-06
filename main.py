
import sys
import core.manager_api as manager
from PyQt5.QtWidgets import QApplication
from ui.recognition_config_form import RecognitionConfigForm


def main():
    app = QApplication(sys.argv)
    form = RecognitionConfigForm()
    form.show()
    app.exec_()
    form_data = form.get_form_data()
    print(form_data)
    #manager.generate_final_video()
if __name__ == "__main__":
    main()