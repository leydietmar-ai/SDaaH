from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt
from subroutines.icon_subroutine import emoji_to_icon


class MemoryModel(QStandardItemModel):
    def __init__(self, mem_dict):
        super().__init__()
        self.setHorizontalHeaderLabels(["Key", "Value"])

        # Icon für Memory
        self.icon = emoji_to_icon("💾")

        for key, value in mem_dict.items():
            self.appendRow([
                QStandardItem(str(key)),
                QStandardItem(self._format_value(value))
            ])

    def data(self, index, role):
        if role == Qt.DecorationRole and index.column() == 0:
            return self.icon
        return super().data(index, role)

    def _format_value(self, v):
        try:
            return f"{v / 1024 / 1024:.2f} MB"
        except Exception:
            return str(v)
