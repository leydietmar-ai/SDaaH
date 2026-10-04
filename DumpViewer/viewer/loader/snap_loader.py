import warnings
from pathlib import Path
from models.stacktrace_model import StacktraceModel
from models.locals_model import LocalsModel
from models.globals_model import GlobalsModel
from models.environment_model import EnvironmentModel
from models.memory_model import MemoryModel


class SnapLoader:
    def __init__(self, viewer):
        self.v = viewer

    def load(self, data):

        # Header
        if self.v.current_filename:
            name = Path(self.v.current_filename).name
            self.v.header_label.setText(f"SnapDump – Viewer\n{name}")
        else:
            self.v.header_label.setText("SnapDump – Viewer")

        # Meta
        meta = data.get("meta", {})
        self.v.meta_label.setText(
            f"Zeit: {meta.get('timestamp','')}\n"
            f"Version: {meta.get('version','')}\n"
            f"Request-ID: {meta.get('request_id','')}"
        )

        # Errorinfo ausblenden
        self.v.error_info_label.hide()

        # Context
        context = data.get("context", {})
        self.v.context_view.setModel(GlobalsModel(context))

        # Stacktrace
        stacktrace = data.get("stacktrace", [])
        model = StacktraceModel(stacktrace)
        self.v.stack_view.setModel(model)
        
        # Unterdrückt die C++ RuntimeWarning beim ersten Laden geräuschlos
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            self.v.stack_view.clicked.disconnect()
            
        self.v.stack_view.clicked.connect(self.v.on_stack_item_clicked)

        # Locals leer
        self.v.locals_view.setModel(LocalsModel({}))

        # Globals optional
        if "globals" in data:
            self.v.globals_view.setModel(GlobalsModel(data["globals"]))
            self.v.globals_view.show()
        else:
            self.v.globals_view.hide()

        # Environment optional
        if "environment" in data:
            self.v.environment_view.setModel(EnvironmentModel(data["environment"]))
            self.v.environment_view.show()
        else:
            self.v.environment_view.hide()

        # Memory
        self.v.memory_view.setModel(MemoryModel(data.get("memory", {})))
