# Technische Dokumentation: Grid Layout Generator (grid_layout_generator.py)

Dieses Modul bietet eine dynamische, CSS-inspirierte Abstraktionsschicht für das `QGridLayout` von PySide6. Es ermöglicht die Definition komplexer Benutzeroberflächen über visuelle Text-Matrizen oder Koordinaten-Listen und erzeugt automatisch transparente Container, die nahtlos über Qt Style Sheets (QSS) gestylt werden können.

## 1. Kernvorteile
* **Visuelle Layout-Struktur**: Das Layout wird lesbar als Text-Array im Code abgebildet (`grid_template_area`).
* **Automatische Validierung**: Das System prüft zur Laufzeit, ob alle definierten Layout-Bereiche mathematisch korrekte Rechtecke bilden.
* **QSS-ready**: Erzeugt standardmäßig transparente Hintergrund-Container (`QWidget`), wodurch das Layout flexibel über Qt Style Sheets (QSS) gestylt werden kann.
* **Wartungsfreundlich**: Zeilen- oder Spaltenänderungen erfordern kein manuelles Neuberechnen der nachfolgenden Widget-Positionen.

---

## 2. Komponenten & API-Referenz

### 2.1 build_grid_area_from_template(template)
Analysiert ein zweidimensionales Text-Array und berechnet die geometrischen Ausmaße der benannten Bereiche.

* **Eingabe**: `List[List[str]]` (Die Text-Matrix des Layouts)
* **Ausgabe**: `Tuple[List[Tuple], Dict]` (Gibt die berechneten Koordinaten-Tupel und die Namens-Map zurück)
* **Verhalten**: Scannt alle Zellen, gruppiert identische Strings und ignoriert Point-Platzhalter (`"."`). Errechnet `row`, `col`, `row_span`, `col_span`.
* **Validierung**: Bildet ein Name kein exaktes Rechteck (z. B. L-Formen), wird ein `ValueError` ausgelöst.

### 2.2 Klasse: GridLayout(QGridLayout)
Erweitert die native PySide6-Klasse `QGridLayout` um ein internes Namensregister (`area_map`).

#### Methode: add_to_area(name: str, widget: QWidget)
Platziert ein Widget direkt über seinen logischen Namen in den zuvor berechneten Bereich.

* **Fehlerbehandlung**: Wirft einen `ValueError`, falls der übergebene Bereichsname (`name`) nicht im Register existiert.

### 2.3 Factory-Funktion: Grid(...)
Die zentrale Einstiegsfunktion, die das fertige `GridLayout` initialisiert und drei flexible Definitions-Modi (Fallbacks) unterstützt.

#### Parameter

| Parameter | Typ | Standardwert | Beschreibung |
| :--- | :--- | :--- | :--- |
| `grid_template_rows` | `int` | *Erforderlich* | Anzahl der Gesamtzeilen im Grid. |
| `grid_template_cols` | `int` | *Erforderlich* | Anzahl der Gesamtspalten im Grid. |
| `grid_gap` | `int` | `0` | Abstand (`Spacing`) zwischen den Zellen in Pixeln. |
| `grid_template_area` | `Optional[List[List[str]]]` | `None` | **Modus 1**: CSS-ähnliche Text-Matrix. Schließt `grid_area` aus. |
| `grid_area` | `Optional[List[Tuple[int,int,int,int]]]` | `None` | **Modus 2**: Manuelle Übergabe von Koordinaten-Tupeln `(row, col, row_span, col_span)`. |
| `grid_tst` | `bool` | `False` | Debug-Flag: Gibt die generierten Koordinaten bei Aktivierung auf der Konsole aus. |

#### Funktions-Logik (Fallbacks & Modi)
1. **CSS-Template (Modus 1)**: Falls `grid_template_area` übergeben wird, werden die Regionen automatisch berechnet und über ihre Text-IDs (z. B. `"a"`, `"b"`) registriert.
2. **Manuelle Koordinaten (Modus 2)**: Falls `grid_area` direkt übergeben wird, generiert das System automatische Namen (`"a0"`, `"a1"`, etc.) für die Tupel-Bereiche.
3. **Zellen-Fallback (Modus 3)**: Wenn beide Optionen `None` sind, wird jede Zelle einzeln als eigener Bereich (`"cell_0"`, `"cell_1"`, etc.) über das gesamte Raster hinweg partitioniert.
