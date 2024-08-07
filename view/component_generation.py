from PyQt5.QtGui import QIcon, QPixmap
from utils.request_utils import get_content

def generate_icon(icon_url):
    icon_data = get_content(icon_url)
    pixmap = QPixmap()
    pixmap.loadFromData(icon_data)
    return QIcon(pixmap)