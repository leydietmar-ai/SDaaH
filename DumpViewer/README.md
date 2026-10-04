# System-Architektur: PHP Error Environment & PySide6 DumpViewer

Dieses Gesamtsystem verbindet eine robuste Fehlererfassung in PHP (Backend) mit einer komfortablen, grafischen Analyse-Oberfläche in PySide6 (Frontend). Es nutzt getrennte Kommunikationswege, um maximale Stabilität und Einfachheit zu garantieren.

---

## Teil 1: Das PHP-Backend (Datenbeschaffung)

Die PHP-Komponente läuft innerhalb des MVC-Frameworks und stellt vier Diagnose-Werkzeuge bereit:

### 1. AbendDump (`ABEND`) & 2. SnapDump (`SNAP`)

* **Datenformat:** **JSON**
* **Verhalten:** Erzeugen hochstrukturierte JSON-Payloads für Post-Mortem-Analysen (Stacktraces, Variablen-Scopes, System-Kontext).

### 3. DebugDump (`DEBUG`)

* **Datenformat:** **Rohe Text-Logdatei** (Line-by-Line)
* **Verhalten:** Sammelt alle klassischen Entwickler-Inspektionen chronologisch über den gesamten Lebenszyklus des HTTP-Requests.
* **Schutz vor Datenverlust:** Direkte, unpufferte Festplattenschreibung. Keine Ausgaben gehen bei HTTP-Redirects oder AJAX-Aufrufen verloren.

### 4. GtfTrace (`GTF`)

* **Datenformat:** **JSON Lines (JSONL)**
* **Verhalten:** Protokolliert im Normalbetrieb sequentiell und hochperformant den echten Kontrollfluss an den MVC-Grenzen (Router, Controller, Model) inklusive Speicher-Metriken und einer reduzierten Live-Aufrufkette (`calling_stack`).
* **Aktivierung:** "Bei Bedarf" steuerbar über zentrale Parameter oder geheime URL-Trigger, um Performance-Overhead in Produktion zu verhindern.

---

## Teil 2: Das PySide6-Frontend (Der DumpViewer)

Der DumpViewer ist eine native Desktop-Applikation, die dank der flexiblen `Grid`-Subroutine alle Datenquellen nahtlos in einer einzigen Oberfläche vereint.

### Verarbeitung der unterschiedlichen Datenquellen im Grid

```text
                        ┌──(Strukturierte Fehler)──► [ JSON-Datei  ] ──► [ Grid: stack, locals, code etc. ]
                        │
[ PHP MVC-Anwendung ] ──┼──(Laufende Debugs)     ──► [ Text-Log    ] ──► [ Grid: debuglog (Plaintext) ]
                        │
                        └──(Kontrollfluss-Trace) ──► [ JSONL-Datei ] ──► [ Grid: debuglog (Kollabiertes UI) ]
```

1. **Strukturierte Ansichten (via JSON):** Die Bereiche `stack`, `code`, `locals`, `globals` etc. werden dynamisch aus der generierten JSON-Datei befüllt.
2. **Direkte Log-Ansicht (via Textdatei):** Der Bereich `debuglog` liest die rohe Text-Logdatei direkt ein.
3. **Flugschreiber-Ansicht (via JSONL):** Der Bereich `debuglog` liest die sequentiellen JSON Lines über einen dedizierten `GtfLoader` ein.
4. **Dynamisches Kollabieren:** Die Haupt-Routine blendet alle oberen, ungenutzten MVC-Widgets (`stack`, `locals`, `code` etc.) über `.hide()` aus.
   * **Grid-Autoresize:** Der `Grid_Layout_Generator` berechnet die Flächen live neu, sodass die Area `debuglog` den gesamten Bildschirmplatz für das formatierte Protokoll beansprucht.
   * **Syntax Highlighting:** Der integrierte `PHPHighlighter` wurde um reguläre Ausdrücke erweitert, die Zeitstempel, Subsysteme und Calling-Stacks automatisch einfärben.

---

## Architektur-Prinzip: Strikte Modularität

Um eine hohe Wartbarkeit zu garantieren und das Anschwellen der Hauptklassen zu verhindern, sind sowohl das PHP-Backend als auch das PySide6-Frontend strikt modular aufgebaut.

### 1. Modulares PHP-Backend

* Jede Dump- und Trace-Art (`ABEND`, `SNAP`, `DEBUG`, `GTF`) kapselt ihre eigene Logik in autarken Namespaces und Subroutinen.
* Die MVC-Anwendung bleibt dadurch entkoppelt von der internen Funktionsweise der Fehlererfassung.

### 2. Modulares PySide6-Frontend

* **Schlanke Hauptkomponente:** Der `DumpViewer` (`QMainWindow`) fungiert lediglich als Orchestrator für die Weichenstellung des Dateityps und lädt das Stylesheet.
* **Gekapselte Subroutines & Sub-Widgets:** Visuelle Komponenten wie die `status_bar` oder Design-Hilfen (`Color`) sind in eigene Dateien ausgelagert.
* **Dedizierte Datenmodelle & Loader:** Das System trennt strikt zwischen visueller Darstellung und Datenverarbeitung. Neue Datenströme (wie der `GtfLoader`) werden isoliert aufbereitet, bevor sie an das bestehende UI übergeben werden.
