from PySide6.QtCore import Qt, QAbstractItemModel, QModelIndex

class LocalNode:
    def __init__(self, key, value, parent=None):
        self.key = key
        self.value = value
        self.parent = parent
        self.children = []

        self._build_children()

    def _build_children(self):
        v = self.value

        # dict → Schlüssel als Unterknoten
        if isinstance(v, dict):
            for k, val in v.items():
                self.children.append(LocalNode(k, val, self))

        # list / tuple → Indexe als Unterknoten
        elif isinstance(v, (list, tuple)):
            for i, val in enumerate(v):
                self.children.append(LocalNode(f"[{i}]", val, self))

        # primitive Werte → keine Kinder
        else:
            pass

    def child_count(self):
        return len(self.children)

    def child(self, row):
        return self.children[row]

    def row(self):
        if self.parent:
            return self.parent.children.index(self)
        return 0


class LocalsModel(QAbstractItemModel):
    def __init__(self, locals_dict):
        super().__init__()
        self.root = LocalNode("locals", locals_dict)

    def index(self, row, col, parent):
        if not self.hasIndex(row, col, parent):
            return QModelIndex()

        parent_node = parent.internalPointer() if parent.isValid() else self.root
        child = parent_node.child(row)
        return self.createIndex(row, col, child)

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        node = index.internalPointer()
        parent = node.parent

        if parent is None or parent == self.root:
            return QModelIndex()

        return self.createIndex(parent.row(), 0, parent)

    def rowCount(self, parent):
        if not parent.isValid():
            node = self.root
        else:
            node = parent.internalPointer()

        return node.child_count()

    def columnCount(self, parent):
        return 2  # key + value

    def data(self, index, role):
        if not index.isValid():
            return None

        node = index.internalPointer()

        if role == Qt.DisplayRole:
            if index.column() == 0:
                return str(node.key)
            if index.column() == 1:
                return self._format_value(node.value)

        return None

    def _format_value(self, v):
        if isinstance(v, dict):
            return f"dict ({len(v)})"
        if isinstance(v, list):
            return f"list ({len(v)})"
        if isinstance(v, tuple):
            return f"tuple ({len(v)})"
        if v is None:
            return "None"
        return repr(v)
