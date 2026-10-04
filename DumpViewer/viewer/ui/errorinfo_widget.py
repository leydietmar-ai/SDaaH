from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt


class ErrorInfoLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__("", parent)
        self.setAlignment(Qt.AlignCenter)
        self.setObjectName("error_info_label")
