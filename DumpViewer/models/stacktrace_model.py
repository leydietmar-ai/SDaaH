from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt

from subroutines.frame_kind import detect_frame_kind
from subroutines.frame_icons import icon_for_frame_kind


class StacktraceModel(QStandardItemModel):
    def __init__(self, stacktrace):
        super().__init__()
        self.stacktrace = stacktrace

        self.setHorizontalHeaderLabels(["Frame", "Function"])

        for i, frame in enumerate(stacktrace):
            # Spalte 0: Frame-Index
            item_index = QStandardItem(str(i))
            item_index.setData(frame)  # Frame speichern

            # Spalte 1: Signature
            item_sig = QStandardItem(frame["signature"])
            item_sig.setData(frame)

            self.appendRow([item_index, item_sig])

    # ---------------------------------------------------------
    # Daten für TreeView liefern (Text, Icon, Frame)
    # ---------------------------------------------------------
    def data(self, index, role):

        if not index.isValid():
            return None

        item = self.itemFromIndex(index)
        frame = item.data()  # <-- MUSS als erstes kommen!

        # Icons deaktiviert (falls du das noch brauchst)
        if role == Qt.DecorationRole and frame is None:
            return None

        # Text
        if role == Qt.DisplayRole:
            return item.text()

        # Icon links vom Text
        if role == Qt.DecorationRole and frame:
            kind = detect_frame_kind(frame)
            return icon_for_frame_kind(kind)

        # Frame-Objekt zurückgeben
        if role == Qt.UserRole + 1:
            return frame

        return super().data(index, role)
