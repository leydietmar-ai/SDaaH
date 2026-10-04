from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor
import re

class DebugDumpHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)

        # Zeitstempel
        self.fmt_timestamp = QTextCharFormat()
        self.fmt_timestamp.setForeground(QColor("#888"))

        # Header
        self.fmt_header = QTextCharFormat()
        self.fmt_header.setForeground(QColor("#b8860b"))
        self.fmt_header.setFontWeight(700)

        # PHP-Typen
        self.fmt_keyword = QTextCharFormat()
        self.fmt_keyword.setForeground(QColor("#005cc5"))
        self.fmt_keyword.setFontWeight(600)

        # Strings
        self.fmt_string = QTextCharFormat()
        self.fmt_string.setForeground(QColor("#d14"))

    def highlightBlock(self, text):
        # Zeitstempel
        for m in re.finditer(r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]", text):
            self.setFormat(m.start(), m.end() - m.start(), self.fmt_timestamp)

        # Header
        for m in re.finditer(r"===.*===", text):
            self.setFormat(m.start(), m.end() - m.start(), self.fmt_header)

        # PHP-Typen
        for m in re.finditer(r"\b(string|array|int|float|bool)\b", text):
            self.setFormat(m.start(), m.end() - m.start(), self.fmt_keyword)

        # Strings
        for m in re.finditer(r"\".*?\"", text):
            self.setFormat(m.start(), m.end() - m.start(), self.fmt_string)
