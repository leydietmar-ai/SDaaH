from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt


class MetaLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__("", parent)
        self.setAlignment(Qt.AlignCenter)
        self.setObjectName("meta_label")
