# Architektur: PHP Mainframe-style Error Environment

Dieses Subsystem bringt bewährte Diagnose-Konzepte aus der Großrechner-Welt (IBM z/OS) in das PHP MVC-Umfeld. Es fängt Fehler, Zustände und Debug-Informationen strukturiert ab und bereitet sie als standardisierte Payloads für den PySide6 'DumpViewer' vor.

## Die 4 Säulen der Diagnose

### 1. AbendDump (Abnormal End)

* **Zweck:** Post-Mortem-Analyse nach kritischen Laufzeitfehlern oder unbehandelten Exceptions.
* **Verhalten:** Bricht die Anwendung kontrolliert ab, sammelt den vollständigen Call-Stack, globale/lokale Variablen sowie den System-Environment-Status und schreibt diese als JSON-Dump auf Platte.
* **Ziel:** Exakte Rekonstruktion des Absturzes im Viewer.

### 2. SnapDump (Snapshot)

* **Zweck:** Gezielte Zustandserfassung im laufenden Betrieb (Non-destructive).
* **Verhalten:** Wird manuell im Code an strategischen Stellen aufgerufen. Erfasst den aktuellen Speicher- und Variablenzustand, erlaubt der Anwendung jedoch, ganz normal weiterzulaufen.
* **Ziel:** Analyse von Logikfehlern in Schleifen oder komplexen Algorithmen.

### 3. DebugDump (Aufgemotztes var_dump)

* **Zweck:** Request-übergreifendes Sammeln von Entwickler-Notizen und Variablen-Inspektionen.
* **Verhalten:** Verhindert das typische PHP-Problem, dass Debug-Ausgaben bei Redirects oder AJAX-Antworten verloren gehen. Alle Aufrufe akkumulieren die Daten im Hintergrund über den gesamten Programmdurchlauf hinweg.
* **Ziel:** Lückenlose Chronologie des Requests ohne erzwungenes `die()` oder `exit`.

### 4. GtfTrace (Generalized Trace Facility)

* **Zweck:** Lückenlose Aufzeichnung des Kontrollflusses und der Subsystem-Interaktionen im Normalbetrieb.
* **Verhalten:** Arbeitet rein sequentiell und hochperformant im JSON-Lines-Format (`*.jsonl`). Zeichnet bei Bedarf (gesteuert via URL-Trigger oder System-Flag) jeden Eintritt in Controller, Models oder Router inklusive Speicherallokation und einer reduzierten Live-Aufrufkette (`calling_stack`) auf.
* **Ziel:** Rekonstruktion des exakten "Flugschreiber-Films" bis zu einem potenziellen Fehlerereignis.
