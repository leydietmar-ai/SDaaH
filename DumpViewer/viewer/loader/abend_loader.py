import warnings
from pathlib import Path
from models.stacktrace_model import StacktraceModel
from models.locals_model import LocalsModel
from models.globals_model import GlobalsModel
from models.environment_model import EnvironmentModel
from models.memory_model import MemoryModel


class AbendLoader:
    def __init__(self, viewer):
        self.v = viewer

    def load(self, data):

        # Header
        if self.v.current_filename:
            name = Path(self.v.current_filename).name
            self.v.header_label.setText(f"AbendDump – Viewer\n{name}")
        else:
            self.v.header_label.setText("AbendDump – Viewer")

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

        self.v.meta_label.setText(meta_text)

        # Errorinfo
        error_line = f"{data.get('type', '')}: {data.get('message', '')}"
        file_line = f"{data.get('file', '')}:{data.get('line', '')}"
        self.v.error_info_label.setText(f"{error_line}\n{file_line}")
        self.v.error_info_label.show()

        # Context ausblenden
        self.v.context_view.setModel(GlobalsModel({}))

        # Stacktrace
        stacktrace = data.get("stacktrace", [])
        model = StacktraceModel(stacktrace)
        self.v.stack_view.setModel(model)
        
        # Unterdrückt die C++ RuntimeWarning beim ersten Laden geräuschlos
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            self.v.stack_view.clicked.disconnect()
            
        self.v.stack_view.clicked.connect(self.v.on_stack_item_clicked)

        # Globals
        self.v.globals_view.setModel(
            GlobalsModel(data.get("globals", {}))
        )
        self.v.globals_view.show()

        # Environment
        self.v.environment_view.setModel(
            EnvironmentModel(data.get("environment", {}))
        )
        self.v.environment_view.show()

        # Memory
        self.v.memory_view.setModel(
            MemoryModel(data.get("memory", {}))
        )
