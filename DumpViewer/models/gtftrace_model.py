from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt

class GtfTraceModel(QStandardItemModel):
    def __init__(self, trace_records):
        super().__init__()
        self.trace_records = trace_records

        # Klassische Tabellenköpfe für einen GTF-System-Trace
        self.setHorizontalHeaderLabels(["Zeit", "Subsystem", "Event", "Speicher"])

        for record in trace_records:
            # 1. Spalte: Zeit (Nur hh:mm:ss extrahieren)
            time_str = record.get("timestamp", "").split("T")[-1][:8]
            item_time = QStandardItem(time_str)
            item_time.setData(record) # Den gesamten Record für Klick-Events speichern

            # 2. Spalte: Komponente / Subsystem
            item_comp = QStandardItem(record.get("component", "UNKNOWN"))
            item_comp.setData(record)

            # 3. Spalte: Event / SVC
            item_event = QStandardItem(record.get("event", "UNKNOWN"))
            item_event.setData(record)

            # 4. Spalte: Speicherverbrauch formatiert
            mem_data = record.get("memory", {})
            mem_usage = mem_data.get("usage", 0) / 1024 / 1024
            item_mem = QStandardItem(f"{mem_usage:.2f} MB")
            item_mem.setData(record)

            # Reihe an das Model anhängen
            self.appendRow([item_time, item_comp, item_event, item_mem])

    def data(self, index, role):
        if not index.isValid():
            return None

        item = self.itemFromIndex(index)
        record = item.data()

        # Textanzeige für das Grid
        if role == Qt.DisplayRole:
            return item.text()

        # Falls der Viewer beim Anklicken einer Trace-Zeile den gesamten 
        # Record (z.B. den Calling-Stack oder den Context) auslesen möchte:
        if role == Qt.UserRole + 1:
            return record

        return super().data(index, role)
