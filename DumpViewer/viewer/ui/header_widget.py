from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt


class HeaderLabel(QLabel):
    def __init__(self, text: str = "DumpViewer – ABEND + SNAP + DEBUG + TRACE", parent=None):
        super().__init__(text, parent)
        self.setAlignment(Qt.AlignCenter)
        self.setObjectName("header_label")
