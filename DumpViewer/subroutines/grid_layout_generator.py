from typing import List, Tuple, Optional, Dict
from PySide6.QtWidgets import QGridLayout, QLabel, QWidget
from PySide6.QtCore import Qt


# ---------------------------------------------------------
#  CSS‑ähnliche grid-template-areas → Bereiche erkennen
# ---------------------------------------------------------
def build_grid_area_from_template(template):
    rows = len(template)
    cols = len(template[0])

    areas = {}
    for r in range(rows):
        for c in range(cols):
            name = template[r][c]
            if name == ".":
                continue
            areas.setdefault(name, []).append((r, c))

    grid_area = []
    area_map = {}

    for name, cells in areas.items():
        rs = [r for r, _ in cells]
        cs = [c for _, c in cells]

        r0, r1 = min(rs), max(rs)
        c0, c1 = min(cs), max(cs)

        # prüfen, ob Rechteck vollständig gefüllt ist
        for r in range(r0, r1 + 1):
            for c in range(c0, c1 + 1):
                if template[r][c] != name:
                    raise ValueError(f"Bereich '{name}' ist kein Rechteck")

        row_span = r1 - r0 + 1
        col_span = c1 - c0 + 1

        tup = (r0, c0, row_span, col_span)
        grid_area.append(tup)
        area_map[name] = tup

    return grid_area, area_map


# ---------------------------------------------------------
#  Erweiterter GridLayout mit add_to_area()
# ---------------------------------------------------------
class GridLayout(QGridLayout):
    def __init__(self, area_map: Dict[str, Tuple[int, int, int, int]]):
        super().__init__()
        self.area_map = area_map

    def add_to_area(self, name: str, widget: QWidget):
        if name not in self.area_map:
            raise ValueError(f"Unbekannter Bereich: {name}")

        row, col, rs, cs = self.area_map[name]
        self.addWidget(widget, row, col, rs, cs)


# ---------------------------------------------------------
#  Hauptfunktion: Grid erzeugen (QSS‑freundlich)
# ---------------------------------------------------------
def Grid(
    grid_template_rows: int,
    grid_template_cols: int,
    grid_gap: int = 0,
    grid_template_area: Optional[List[List[str]]] = None,
    grid_area: Optional[List[Tuple[int, int, int, int]]] = None,
    grid_tst: bool = False,
) -> GridLayout:

    # beide Varianten dürfen nicht gleichzeitig gesetzt sein
    if grid_template_area is not None and grid_area is not None:
        raise ValueError("grid_template_area und grid_area schließen sich gegenseitig aus.")

    area_map = {}

    # Variante 1: CSS-like grid-template-area
    if grid_template_area is not None:
        grid_area, area_map = build_grid_area_from_template(grid_template_area)

    # Variante 2: manuelle grid_area
    if grid_area is not None and not area_map:
        area_map = {f"a{i}": tup for i, tup in enumerate(grid_area)}

    # Variante 3: Fallback → jede Zelle einzeln
    if grid_area is None:
        grid_area = [
            (r, c, 1, 1)
            for r in range(grid_template_rows)
            for c in range(grid_template_cols)
        ]
        area_map = {f"cell_{i}": tup for i, tup in enumerate(grid_area)}

    # erweitertes Layout
    grid_layout = GridLayout(area_map)
    grid_layout.setSpacing(grid_gap)

    # ---------------------------------------------------------
    # Normaler Modus → transparente Container + optional Debug-Text
    # ---------------------------------------------------------
    for i, (row, col, row_span, col_span) in enumerate(grid_area):

        # transparenter Container (QSS übernimmt Farben)
        cell_widget = QWidget()
        cell_widget.setStyleSheet("background: transparent;")
        grid_layout.addWidget(cell_widget, row, col, row_span, col_span)

    if grid_tst:
        print("Generated grid_area:", grid_area)

    return grid_layout
