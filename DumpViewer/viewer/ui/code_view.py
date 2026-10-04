from PySide6.QtWidgets import QPlainTextEdit
from PySide6.QtGui import QFont

# Deinen Highlighter importieren
from php_highlighter import PHPHighlighter


class CodeView(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setObjectName("code_view")

        # Optional: Font setzen
        font = QFont("Consolas", 10)
        self.setFont(font)

        # Syntax-Highlighting aktivieren
        self.highlighter = PHPHighlighter(self.document())

