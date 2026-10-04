from PySide6.QtWidgets import QTreeView


class StackTraceView(QTreeView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHeaderHidden(False)
        self.setObjectName("stack_view")
