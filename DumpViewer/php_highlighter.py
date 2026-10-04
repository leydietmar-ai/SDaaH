from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PySide6.QtCore import QRegularExpression

class PHPHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)

        self.rules = []

        def fmt(color, bold=False):
            f = QTextCharFormat()
            f.setForeground(QColor(color))
            if bold:
                f.setFontWeight(QFont.Bold)
            return f

        # PHP Keywords
        keyword_format = fmt("#C678DD", True)
        keywords = [
            "function", "class", "public", "private", "protected",
            "static", "return", "try", "catch", "throw",
            "if", "else", "elseif", "for", "foreach", "while",
            "break", "continue", "new", "use", "namespace",
            "extends", "implements", "finally",
        ]
        for kw in keywords:
            pattern = QRegularExpression(rf"\b{kw}\b")
            self.rules.append((pattern, keyword_format))

        # Variablen: $name
        var_format = fmt("#61AFEF")
        self.rules.append((QRegularExpression(r"\$[A-Za-z_][A-Za-z0-9_]*"), var_format))

        # Namespaces: \Foo\Bar
        ns_format = fmt("#E5C07B")
        pattern_ns = QRegularExpression(r"\\[A-Za-z_][A-Za-z0-9_\\]*")
        self.rules.append((pattern_ns, ns_format))

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

        # ---------------------------------------------------------
        # Spezifische Erweiterungen für den GTF-Trace (JETZT KORREKT IN __init__)
        # ---------------------------------------------------------
        # Subsysteme (CONTROLLER, MODEL, SUBSYSTEM) -> Kräftiges Cyan
        subsystem_format = fmt("#56B6C2", bold=True)
        self.rules.append((QRegularExpression(r"\b(CONTROLLER|MODEL|SUBSYSTEM)\b"), subsystem_format))

        # Trace-Events (ACTION_START, USER_CHECK, BEFORE_SNAP, CALCULATION_START) -> Helles Rot/Rosa
        event_format = fmt("#E06C75", bold=True)
        self.rules.append((QRegularExpression(r"\b[A-Z]{3,}_[A-Z]{3,}\b"), event_format))

        # Zeitstempel am Zeilenanfang (hh:mm:ss) -> Dezentes Grau
        time_format = fmt("#ABB2BF")
        self.rules.append((QRegularExpression(r"^\d{2}:\d{2}:\d{2}"), time_format))

        # Die Baum-Strukturzeichen (└── [Stack #0]) -> Dunkles Blau/Grau für Struktur
        tree_format = fmt("#4B5263")
        self.rules.append((QRegularExpression(r"└── \[[A-Za-z0-9 #]+\]"), tree_format))

    def highlightBlock(self, text):
        # Wichtig: highlightBlock führt NUR das Zeichnen aus, KEIN Registrieren von Regeln!
        for pattern, form in self.rules:
            it = pattern.globalMatch(text)
            while it.hasNext():
                m = it.next()
                self.setFormat(m.capturedStart(), m.capturedLength(), form)

        # Kommentare: // ...
        comment_index = text.find("//")
        if comment_index >= 0:
            self.setFormat(comment_index, len(text) - comment_index, self.comment_format)
