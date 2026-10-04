from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt
from subroutines.icon_subroutine import emoji_to_icon


class EnvironmentModel(QStandardItemModel):
    def __init__(self, env_dict):
        super().__init__()
        self.setHorizontalHeaderLabels(["Key", "Value"])

        # Icon für Environment
        self.icon = emoji_to_icon("🧩")

        self._populate(env_dict)

    def data(self, index, role):
        if role == Qt.DecorationRole and index.column() == 0:
            return self.icon
        return super().data(index, role)

    # ---------------------------------------------------------
    # Rekursive Befüllung
    # ---------------------------------------------------------
    def _populate(self, data, parent_item=None):
        if parent_item is None:
            parent_item = self.invisibleRootItem()

        if isinstance(data, dict):
            for key, value in data.items():
                key_item = QStandardItem(str(key))
                val_item = QStandardItem(self._format_value(value))

                parent_item.appendRow([key_item, val_item])

                if isinstance(value, (dict, list)):
                    self._populate(value, key_item)

        elif isinstance(data, list):
            for i, value in enumerate(data):
                key_item = QStandardItem(f"[{i}]")
                val_item = QStandardItem(self._format_value(value))

                parent_item.appendRow([key_item, val_item])

                if isinstance(value, (dict, list)):
                    self._populate(value, key_item)

    def _format_value(self, v):
        if v is None:
            return "null"
        if isinstance(v, bool):
            return "true" if v else "false"
        if isinstance(v, (dict, list)):
            return ""
        return str(v)
