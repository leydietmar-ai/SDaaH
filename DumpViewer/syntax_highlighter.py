from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PySide6.QtCore import QRegularExpression

class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)

        self.rules = []

        def fmt(color, bold=False):
            f = QTextCharFormat()
            f.setForeground(QColor(color))
            if bold:
                f.setFontWeight(QFont.Bold)
            return f

        # Keywords
        keyword_format = fmt("#C678DD", True)
        keywords = [
            "False", "class", "finally", "is", "return",
            "None", "continue", "for", "lambda", "try",
            "True", "def", "from", "nonlocal", "while",
            "and", "del", "global", "not", "with",
            "as", "elif", "if", "or", "yield",
            "assert", "else", "import", "pass",
            "break", "except", "in", "raise",
        ]
        for kw in keywords:
            pattern = QRegularExpression(rf"\b{kw}\b")
            self.rules.append((pattern, keyword_format))

        # Strings
        string_format = fmt("#98C379")
        self.rules.append((QRegularExpression(r"'[^']*'"), string_format))
        self.rules.append((QRegularExpression(r'"[^"]*"'), string_format))

        # Kommentare
        comment_format = fmt("#5C6370")
        self.comment_format = comment_format

        # Zahlen
        number_format = fmt("#D19A66")
        self.rules.append((QRegularExpression(r"\b[0-9]+\b"), number_format))

    def highlightBlock(self, text):
        for pattern, form in self.rules:
            it = pattern.globalMatch(text)
            while it.hasNext():
                m = it.next()
                self.setFormat(m.capturedStart(), m.capturedLength(), form)

        # Kommentar ab "#"
        comment_index = text.find("#")
        if comment_index >= 0:
            self.setFormat(comment_index, len(text) - comment_index, self.comment_format)
