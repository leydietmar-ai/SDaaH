# Technische Dokumentation: Abend Diagnostics Internals

Diese Dokumentation beschreibt die internen Mechanismen, Design-Entscheidungen und technischen Lösungen des Abend-Systems. Sie dient als Referenz für die Wartung, Erweiterung und das Verständnis der zugrundeliegenden PHP-Laufzeit-Phänomene.

---

## 1. Die State-Capture-Architektur (Reflection vs. Engine-State)

Eine der größten Herausforderungen in PHP ist es, nach dem Auftreten einer Exception an die lokalen Variablen (`$foo`, `$bar`) des aktuellen Scopes zu gelangen. `Throwable::getTrace()` liefert zwar Argumente von Funktionsaufrufen, aber **nicht** die im Funktionskörper deklarierten lokalen Variablen.

### Die Lösung: Closure-Reflection-Brücke (`AbendCapture`)

Das System erzwingt durch das Design-Pattern der kontrollierten Ausführung via Closure einen isolierten Scope:

```php
AbendCapture::execute(function () use (&\(foo, &\)bar) { ... });
```

Tritt eine `Throwable` auf, greift die PHP-Reflection-API in der `AbendCapture`-Klasse:

1. **`ReflectionFunction`**: Instanziiert die anonyme Funktion im `catch`-Block.
2. **`getStaticVariables()`**: Holt die internen Bindungen der Closure. In PHP werden Variablen, die per `use` an eine anonyme Funktion übergeben werden, intern als "statische Variablen" der Closure-Instanz geführt.
3. **Zustandssicherung**: Die Variablen werden atomar im statischen Property `self::$lastLocals` gesichert, bevor die Exception mit `throw $e` weitergereicht wird. Dadurch bleibt der Zustand für den globalen Exception-Handler konserviert.

---

## 2. Das Dual-Trace-Verfahren im Stacktrace (Exception vs. Live)

Wenn der `DumpCollector` anspringt, kombiniert er zwei verschiedene Traces, um ein lückenloses Bild zu zeichnen:

1. **Der Exception-Trace (`$e->getTrace()`)**: Zeigt den statischen Weg des Fehlers. Er wird zum Zeitpunkt des `throw`-Befehls eingefroren.
2. **Der Live-Trace (`debug_backtrace()`)**: Zeigt den echten, dynamischen Aufruf-Stack zum Zeitpunkt der Dump-Generierung.

### Synchronisation in `StacktraceCollector`

Da beide Arrays synchron aufgebaut sind (der Index `$i` korreliert in der Regel), fusioniert der `StacktraceCollector` das passende `liveFrame` mit dem `exceptionFrame`. Nur der Live-Trace enthält das aktuelle `object` (`$this`), wodurch wir im Dump das exakte Objekt-Inhalt-Abbild des abgestürzten Controllers mitsichern können.

---

## 3. Die Stream-Appending-Strategie im `DebugDumper`

Klassische Debugging-Tools sammeln Logs oft im Arbeitsspeicher (RAM) und schreiben sie am Ende des Requests. Das birgt bei Schleifen oder massiven Datendumps das Risiko eines `Fatal Error: Allowed memory size exhausted` (wodurch das Debug-Tool selbst das System crasht).

### Technische Umsetzung `DebugDumper`

Der `DebugDumper` entkoppelt sich vollständig vom RAM:

- **Output-Buffering**: `ob_start()` und `ob_get_clean()` fangen die native `var_dump()`-Formatierung der PHP-Engine ab. Dieser String wird sofort verarbeitet.
- **I/O-Streaming via `FILE_APPEND`**: `file_put_contents($file, $entry, FILE_APPEND)` führt auf Betriebssystemebene einen direkten Schreibvorgang am Ende der Datei durch. Der Hauptspeicher von PHP bleibt zu jedem Zeitpunkt frei.
- **Request-Idempotenz**: Durch die Nutzung einer klassen-statischen Variablen `private static ?string $file` bleibt der Dateiname über den gesamten Request identisch, wechselt aber beim nächsten HTTP-Aufruf vollautomatisch.

---

## 4. Das On-Demand JSON-Lines Event-Streaming (`GtfTrace`)

Klassische Logging-Tools sammeln Event-Daten oft im RAM oder modifizieren ein geschlossenes JSON-Array. Bei hochfrequenten Events oder langlaufenden Prozessen führt dies zu hohem Speicherverbrauch, und Systemabstürze können die gesamte Log-Datei korrumpieren.

### Technische Umsetzung

`GtfTrace` entkoppelt sich vom RAM und ermöglicht sicheres Live-Tracing:

- **O(1) Speicherverbrauch (JSONL)**: `json_encode($record) . "\n"` schreibt jeden Eintrag als autarke Zeile via `FILE_APPEND`. Der Hauptspeicher bleibt frei, und die Datei ist bei Abstürzen niemals korrupt.
- **Transiente Aktivierung**: `isset($_GET['gtf_trace'])` wertet die Superglobale direkt in `init()` aus. Im inaktiven Zustand reduziert sich der Overhead bei `write()` auf eine hocheffiziente Bool-Prüfung.
- **Request-Isolierung**: `bin2hex(random_bytes(8))` erzeugt eine kryptografisch sichere ID. Diese verknüpft alle asynchronen Logzeilen desselben HTTP-Aufrufs im globalen Datenstrom.
- **Pfad-Normierung**: `dirname($_SERVER['SCRIPT_FILENAME'])` ermittelt die Projekt-Wurzel außerhalb des `public/`-Ordners, während `DIRECTORY_SEPARATOR` Windows- und Linux-Pfade vor dem `mkdir()` angleicht.

## 5. Speicher-Sicherheit und JSON-Konformität (`ValueNormalizer`)

Der `ValueNormalizer` ist die Sicherheitsbarriere vor der `json_encode()`-Zentrale. Ohne diese Barriere würde das Diagnose-Subsystem bei komplexen Projekten instabil werden.

### Abwehr von Zirkulären Referenzen (Circular References)

Wenn Objekt A auf Objekt B verweist, und Objekt B zurück auf Objekt A, führt eine parataktische Serialisierung zum unendlichen Loop und PHP-Absturz.

- **Lösung**: Der `ValueNormalizer` führt einen `depth`-Zähler mit. Erreicht die Rekursionsebene den Wert `5`, bricht der Ast hart ab und liefert den String `**depth_limit**`.

### Kapselung von I/O-Ressourcen & Closures

Datenbankverbindungen (z. B. PDO-Instanzen, Datei-Handles oder cURL-Ressourcen) können nicht in JSON übersetzt werden (`json_encode` liefert `null` oder Fehler).

- `is_resource()` fängt diese Typen ab und maskiert sie sicher als `**resource**`.
- Objekte werden über `get_object_vars()` in assoziative Arrays zerlegt, wodurch private und geschützte Properties für den Analyzer sichtbar gemacht werden, ohne die Kapselung im Live-Code zu verletzen.
