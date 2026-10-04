import sys

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

import json
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QVBoxLayout,
    QFileDialog,
    QMessageBox,
    QScrollArea,
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QModelIndex

# Viewer Modules
from viewer.loader.abend_loader import AbendLoader
from viewer.loader.snap_loader import SnapLoader
from viewer.ui.header_widget import HeaderLabel
from viewer.ui.meta_widget import MetaLabel
from viewer.ui.context_widget import ContextView
from viewer.ui.errorinfo_widget import ErrorInfoLabel
from viewer.ui.stacktrace_view import StackTraceView
from viewer.ui.locals_view import LocalsView
from viewer.ui.globals_view import GlobalsView
from viewer.ui.code_view import CodeView
from viewer.ui.environment_view import EnvironmentView
from viewer.ui.memory_view import MemoryView
from viewer.ui.menu_bar import DumpViewerMenuBar
from viewer.ui.debug_view import DebugLogView


# Grid-System
from subroutines.grid_layout_generator import Grid
from subroutines.statusbar_subroutine import status_bar
from subroutines.color_subroutine import Color

# Models
from models.stacktrace_model import StacktraceModel
from models.locals_model import LocalsModel
from models.globals_model import GlobalsModel
from models.environment_model import EnvironmentModel
from models.memory_model import MemoryModel


class AbendDumpViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.current_filename = None
        
        self.current_theme = "darkmode"
        self.load_stylesheet("styles/darkmode.qss")
        
        # Menüleiste + Toolbar korrekt initialisieren
        self.setMenuBar(DumpViewerMenuBar(self))

        self.setWindowTitle("DumpViewer – ABEND + SNAP + DEBUG + TRACE")
        self.setWindowIcon(QIcon("assets/img/SDaaH-logo.png"))
        self.setGeometry(200, 200, 1200, 900)

        # ---------------------------------------------------------
        # Zentrales Widget
        # ---------------------------------------------------------
        central = QWidget()
        main_layout = QVBoxLayout(central)
        
        # ---------------------------------------------------------
        # Grid-Template (mit CONTEXT-Bereich)
        # ---------------------------------------------------------
        grid_template_area = [
            ["header",      "header",      "header",      "header"],
            ["meta",        "meta",        "meta",        "meta"],
            ["context",     "context",     "context",     "context"],  
            ["errorinfo",   "errorinfo",   "errorinfo",   "errorinfo"],
            ["stack",       "stack",       "code",        "code"],
            ["locals",      "locals",      "code",        "code"],
            ["globals",     "globals",     "globals",     "globals"],
            ["environment", "environment", "environment", "environment"],
            ["memory",      "memory",      "memory",      "memory"],
            ["debuglog",    "debuglog",    "debuglog",    "debuglog"],
            ["footer",      "footer",      "footer",      "footer"],
        ]

        grid_layout = Grid(
            grid_template_rows=11,
            grid_template_cols=4,
            grid_gap=8,
            grid_template_area=grid_template_area,
            grid_tst=False,
        )

        # ---------------------------------------------------------
        # HEADER
        # ---------------------------------------------------------
        self.header_label = HeaderLabel()
        grid_layout.add_to_area("header", self.header_label)

        # ---------------------------------------------------------
        # META
        # ---------------------------------------------------------
        self.meta_label = MetaLabel()
        grid_layout.add_to_area("meta", self.meta_label)

        # ---------------------------------------------------------
        # CONTEXT (NEU)
        # ---------------------------------------------------------
        self.context_view = ContextView()
        grid_layout.add_to_area("context", self.context_view)

        # ---------------------------------------------------------
        # ERRORINFO
        # ---------------------------------------------------------
        self.error_info_label = ErrorInfoLabel()
        grid_layout.add_to_area("errorinfo", self.error_info_label)

        # ---------------------------------------------------------
        # STACKTRACE
        # ---------------------------------------------------------
        self.stack_view = StackTraceView()
        grid_layout.add_to_area("stack", self.stack_view)

        # ---------------------------------------------------------
        # CODE VIEW
        # ---------------------------------------------------------
        self.code_view = CodeView()
        grid_layout.add_to_area("code", self.code_view)

        # ---------------------------------------------------------
        # LOCALS
        # ---------------------------------------------------------
        self.locals_view = LocalsView()
        grid_layout.add_to_area("locals", self.locals_view)

        # ---------------------------------------------------------
        # GLOBALS
        # ---------------------------------------------------------
        self.globals_view = GlobalsView()
        grid_layout.add_to_area("globals", self.globals_view)

        # ---------------------------------------------------------
        # ENVIRONMENT
        # ---------------------------------------------------------
        self.environment_view = EnvironmentView()
        grid_layout.add_to_area("environment", self.environment_view)

        # ---------------------------------------------------------
        # MEMORY
        # ---------------------------------------------------------
        self.memory_view = MemoryView()
        grid_layout.add_to_area("memory", self.memory_view)
        
        # ---------------------------------------------------------
        # DEBUGLOG  ← GENAU HIER MUSS ES HIN
        # ---------------------------------------------------------
        self.debug_widget = DebugLogView()
        grid_layout.add_to_area("debuglog", self.debug_widget)

        # ---------------------------------------------------------
        # FOOTER
        # ---------------------------------------------------------
        self.footer_label = QLabel("Ende der Anzeige")
        self.footer_label.setAlignment(Qt.AlignCenter)
        self.footer_label.setObjectName("footer_label")
        grid_layout.add_to_area("footer", self.footer_label)

        main_layout.addLayout(grid_layout)

        # ---------------------------------------------------------
        # ScrollArea
        # ---------------------------------------------------------
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(central)
        self.setCentralWidget(scroll)

        # ---------------------------------------------------------
        # Statusbar
        # ---------------------------------------------------------
        status_bar(self)

    # ---------------------------------------------------------
    # Stylesheets laden
    # ---------------------------------------------------------    
    def load_stylesheet(self, path: str):
        try:
            with open(path, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print(f"Stylesheet konnte nicht geladen werden: {e}")

    # ---------------------------------------------------------
    # Dump laden (ABEND, SNAP, DEBUG oder GTF-TRACE)
    # ---------------------------------------------------------
    def load_stacktrace(self, json_data):
        # Falls ein Pfad/Dateiname übergeben wurde, der auf .jsonl endet:
        if isinstance(json_data, str) and json_data.endswith('.jsonl'):
            self.load_gtftrace(json_data)
            return

        try:
            data = json.loads(json_data)
            if data.get("type") == "SNAP":
                SnapLoader(self).load(data)
            else:
                AbendLoader(self).load(data)
        except json.JSONDecodeError:
            # Falls Plaintext oder anderes Format, wie gehabt behandeln
            pass

    # ---------------------------------------------------------
    # SNAP-Dump laden
    # ---------------------------------------------------------
    def load_snap(self, data):

        # Header
        if self.current_filename:
            name = Path(self.current_filename).name
            self.header_label.setText(f"SnapDump – Viewer\n{name}")
        else:
            self.header_label.setText("SnapDump – Viewer")

        # Meta
        meta = data.get("meta", {})
        self.meta_label.setText(
            f"Zeit: {meta.get('timestamp','')}\n"
            f"Version: {meta.get('version','')}\n"
            f"Request-ID: {meta.get('request_id','')}"
        )

        # Errorinfo ausblenden
        self.error_info_label.hide()
        
        # Context
        context = data.get("context", {})
        self.context_view.setModel(GlobalsModel(context))

        # Stacktrace
        stacktrace = data.get("stacktrace", [])
        model = StacktraceModel(stacktrace)
        self.stack_view.setModel(model)
        self.stack_view.clicked.connect(self.on_stack_item_clicked)

        # Locals (werden beim Klick geladen)
        self.locals_view.setModel(LocalsModel({}))

        # Globals optional
        if "globals" in data:
            self.globals_view.setModel(GlobalsModel(data["globals"]))
            self.globals_view.show()
        else:
            self.globals_view.hide()

        # Environment optional
        if "environment" in data:
            self.environment_view.setModel(EnvironmentModel(data["environment"]))
            self.environment_view.show()
        else:
            self.environment_view.hide()

        # Memory
        self.memory_view.setModel(MemoryModel(data.get("memory", {})))

    # ---------------------------------------------------------
    # ABEND-Dump laden
    # ---------------------------------------------------------
    def load_abend(self, data):

        # Header
        if self.current_filename:
            name = Path(self.current_filename).name
            self.header_label.setText(f"AbendDump – Viewer\n{name}")
        else:
            self.header_label.setText("AbendDump – Viewer")

        # Meta
        meta = data.get("meta", {})
        timestamp   = meta.get("timestamp", "")
        version     = meta.get("version", "")
        request_id  = meta.get("request_id", "")
        session_id  = meta.get("session_id", None)

        meta_text = (
            f"Zeit: {timestamp}\n"
            f"Version: {version}\n"
            f"Request-ID: {request_id}"
        )

        if session_id:
            meta_text += f"\nSession-ID: {session_id}"

        self.meta_label.setText(meta_text)
        
        # Errorinfo
        error_line = f"{data.get('type', '')}: {data.get('message', '')}"
        file_line = f"{data.get('file', '')}:{data.get('line', '')}"
        self.error_info_label.setText(f"{error_line}\n{file_line}")
        self.error_info_label.show()

        # Context ausblenden
        self.context_view.setModel(GlobalsModel({}))

        # Stacktrace
        stacktrace = data.get("stacktrace", [])
        model = StacktraceModel(stacktrace)
        self.stack_view.setModel(model)
        self.stack_view.clicked.connect(self.on_stack_item_clicked)

        # Globals
        self.globals_view.setModel(
            GlobalsModel(data.get("globals", {}))
        )
        self.globals_view.show()

        # Environment
        self.environment_view.setModel(
            EnvironmentModel(data.get("environment", {}))
        )
        self.environment_view.show()

        # Memory
        self.memory_view.setModel(
            MemoryModel(data.get("memory", {}))
        )
        
    # ---------------------------------------------------------
    # DEBUG-Dump laden
    # ---------------------------------------------------------
    def load_debugdump(self, filename):
        from viewer.loader.debug_loader import DebugLoader

        # Datei einlesen
        lines = DebugLoader.load(filename)

        # Header
        name = Path(filename).name
        self.header_label.setText(f"DebugDump – Viewer\n{name}")

        # Meta leeren
        self.meta_label.setText("")

        # Alle anderen Bereiche ausblenden
        self.error_info_label.hide()
        self.stack_view.hide()
        self.locals_view.hide()
        self.globals_view.hide()
        self.environment_view.hide()
        self.memory_view.hide()
        self.code_view.hide()
        self.context_view.hide()

        # DebugWidget anzeigen
        self.debug_widget.show()
        self.debug_widget.set_log(lines)
        
    # ---------------------------------------------------------
    # GTF-Trace laden
    # ---------------------------------------------------------
    def load_gtftrace(self, filename):
        from viewer.loader.gtf_loader import GtfLoader

        # Datei zeilenweise einlesen und für die Textansicht formatieren
        trace_data = GtfLoader.load(filename)
        
        # Falls der GtfLoader ein Dictionary mit ["logs"] liefert:
        lines = trace_data.get("logs", [])

        # Header im Mainframe-Stil setzen
        name = Path(filename).name
        self.header_label.setText(f"GTF-SystemTrace – Viewer\n{name}")

        # Meta leeren
        self.meta_label.setText("")

        # Alle strukturierten MVC-Bereiche sauber ausblenden
        self.error_info_label.hide()
        self.stack_view.hide()
        self.locals_view.hide()
        self.globals_view.hide()
        self.environment_view.hide()
        self.memory_view.hide()
        self.code_view.hide()
        self.context_view.hide()

        # Bestehendes debug_widget einblenden und mit dem Trace-Stream befüllen
        self.debug_widget.show()
        
        if hasattr(self.debug_widget, "set_log"):
            self.debug_widget.set_log(lines)
        elif hasattr(self.debug_widget, "set_logs"):
            self.debug_widget.set_logs(lines)

    # ---------------------------------------------------------
    # Klick auf Stacktrace → Code + Locals anzeigen
    # ---------------------------------------------------------
    def on_stack_item_clicked(self, index):
        frame = index.data(Qt.UserRole + 1)
        if not frame:
            return

        # Code anzeigen
        snippet_lines = []
        for line in frame["snippet"]:
            prefix = "→ " if line["current"] else "   "
            ln = line["line"]
            ln_str = f"{ln:>4}" if isinstance(ln, int) else "    "
            snippet_lines.append(f"{prefix}{ln_str}  {line['code']}")

        self.code_view.setPlainText("\n".join(snippet_lines))

        # Locals anzeigen
        self.locals_view.setModel(LocalsModel(frame["locals"]))

    # ---------------------------------------------------------
    # Menüleiste
    # ---------------------------------------------------------
    # ALT:
    # self._create_menu()
    # NEU:
    # Menüleiste wird jetzt im Konstruktor gesetzt:
    # self.setMenuBar(DumpViewerMenuBar(self))


    def filter_stacktrace(self, text):
        """
        Wird live aufgerufen, wenn Text in das Suchfeld eingegeben wird.
        Filtert entweder den GTF-Trace im debug_widget oder den klassischen Stacktrace.
        """
        text = text.strip().lower()

        # ---------------------------------------------------------
        # FALL 1: Ein GTF-Trace (.jsonl) ist geladen
        # ---------------------------------------------------------
        if self.current_filename and self.current_filename.endswith(".jsonl"):
            from viewer.loader.gtf_loader import GtfLoader
            
            # Alle Zeilen frisch aus dem Loader holen
            trace_data = GtfLoader.load(self.current_filename)
            all_lines = trace_data.get("logs", [])
            
            if not text:
                # Suchfeld leer? Gesamten Trace wieder anzeigen
                if hasattr(self.debug_widget, "set_log"):
                    self.debug_widget.set_log(all_lines)
                elif hasattr(self.debug_widget, "set_logs"):
                    self.debug_widget.set_logs(all_lines)
                return

            filtered_lines = []
            
            # Jede Zeile prüfen, ob der Suchtext enthalten ist
            for line in all_lines:
                if text in line.lower():
                    filtered_lines.append(line)
            
            # Gefilterte Zeilen im debug_widget anzeigen
            if hasattr(self.debug_widget, "set_log"):
                self.debug_widget.set_log(filtered_lines)
            elif hasattr(self.debug_widget, "set_logs"):
                self.debug_widget.set_logs(filtered_lines)
            return

        # ---------------------------------------------------------
        # FALL 2: Klassischer Stacktrace (ABEND/SNAP) ist geladen
        # ---------------------------------------------------------
        model = self.stack_view.model()
        if not model:
            return

        for row in range(model.rowCount()):
            index = model.index(row, 0)
            frame = index.data(Qt.UserRole + 1)

            if not frame:
                self.stack_view.setRowHidden(row, QModelIndex(), False)
                continue

            snippet = frame.get("snippet", [])
            code_lines = " ".join([l["code"] for l in snippet]).lower()

            haystack = (
                frame.get("function", "").lower() + " " +
                frame.get("file", "").lower() + " " +
                code_lines
            )

            match = text in haystack if text else True
            self.stack_view.setRowHidden(row, QModelIndex(), not match)

    # ---------------------------------------------------------
    # Theme Toggle
    # ---------------------------------------------------------
    def toggle_theme(self):
        if self.current_theme == "darkmode":
            self.current_theme = "lightmode"
            self.load_stylesheet("styles/lightmode.qss")
            self.theme_action.setText("☀️ DarkMode Umschalter")
        else:
            self.current_theme = "darkmode"
            self.load_stylesheet("styles/darkmode.qss")
            self.theme_action.setText("🌙 DarkMode Umschalter")

    # ---------------------------------------------------------
    # Datei öffnen
    # ---------------------------------------------------------
    def open_file_dialog(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Dump/Trace öffnen",
            "",
            "Dump- & Trace-Dateien (*.json *.jsonl *.log);;GTF-Traces (*.jsonl);;Alle Dateien (*)"
        )

        if not filename:
            return

        self.current_filename = filename

        # 1. NEU: GTF-Trace (.jsonl) direkt an die neue Routine übergeben
        if filename.endswith(".jsonl"):
            self.load_gtftrace(filename)
            return

        # 2. DebugDump (.log)
        if filename.endswith(".log"):
            self.load_debugdump(filename)
            return

        # 3. AbendDump / SnapDump (.json)
        with open(filename, "r", encoding="utf-8") as f:
            data = f.read()

        self.load_stacktrace(data)

    # ---------------------------------------------------------
    # Über-Dialog
    # ---------------------------------------------------------
    def show_about_dialog(self):
        QMessageBox.information(
            self,
            "Über DumpViewer",
            "DumpViewer – ABEND + SNAP + DEBUG + TRACE\n\n"
            "Version 1.2.0\n"
            "Erstellt mit PySide6\n"
            "© 2026 von Dietmar Ley"
        )
        
    # ---------------------------------------------------------
    # Beschreibung-Dialog
    # ---------------------------------------------------------
    def show_desc_dialog(self):
        QMessageBox.information(
            self,
            "DumpViewer - Beschreibung",
            "DumpViewer verarbeitet JSON-Dumps aus:\n"
            "• AbendDump (Fehlerfall)\n"
            "• SnapDump (Debug-Snapshot)\n\n"
            "Angezeigt werden:\n"
            "Meta\nContext (SNAP)\nErrorinfo (ABEND)\nStacktrace\nLocals\nGlobals\nEnvironment\nMemory\n\n"
            ".......... verarbeitet JSON-List aus:\n"
            "• TraceDump (Zeit, Subsystem, Event, Speicher)\n\n"
            "...........verarbeitet Log-Daten aus:\n"
            "• var_dump (Label, Variablen-Ausgabe)"
        )    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = AbendDumpViewer()
    viewer.show()
    sys.exit(app.exec())
