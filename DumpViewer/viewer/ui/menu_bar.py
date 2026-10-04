from PySide6.QtWidgets import QMenuBar, QToolBar, QLineEdit, QMessageBox, QFileDialog
from PySide6.QtCore import Qt


class DumpViewerMenuBar(QMenuBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self._create_menu()
        self._create_toolbar()

    # ---------------------------------------------------------
    # Menüleiste
    # ---------------------------------------------------------
    def _create_menu(self):
        # Datei
        file_menu = self.addMenu("Datei")

        open_action = file_menu.addAction("Öffnen…")
        open_action.triggered.connect(self.parent.open_file_dialog)

        file_menu.addSeparator()

        exit_action = file_menu.addAction("Beenden")
        exit_action.triggered.connect(self.parent.close)

        # Hilfe
        help_menu = self.addMenu("Hilfe")

        about_action = help_menu.addAction("Über…")
        about_action.triggered.connect(self.parent.show_about_dialog)

        desc_action = help_menu.addAction("Beschreibung")
        desc_action.triggered.connect(self.parent.show_desc_dialog)

    # ---------------------------------------------------------
    # Toolbar
    # ---------------------------------------------------------
    def _create_toolbar(self):
        toolbar = QToolBar("Suche")
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        self.parent.addToolBar(toolbar)

        # --- Suchfeld ---
        self.parent.search_field = QLineEdit()
        self.parent.search_field.setPlaceholderText("Suche…")
        self.parent.search_field.setFixedWidth(200)
        self.parent.search_field.textChanged.connect(self.parent.filter_stacktrace)
        toolbar.addWidget(self.parent.search_field)

        # --- Theme-Switcher ---
        self.parent.theme_action = toolbar.addAction("🌙 DarkMode Umschalter")
        self.parent.theme_action.triggered.connect(self.parent.toggle_theme)
        self.parent.theme_action.setToolTip("Theme wechseln")
