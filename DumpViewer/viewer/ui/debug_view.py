from PySide6.QtWidgets import QPlainTextEdit
from .debug_highlighter import DebugDumpHighlighter

class DebugLogView(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setObjectName("debuglog_view")

        # HIGHLIGHTER AKTIVIEREN
        self.highlighter = DebugDumpHighlighter(self.document())

    def set_log(self, lines: list[str]):
        self.setPlainText("".join(lines))

        

