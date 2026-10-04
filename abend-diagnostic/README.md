# Abend Diagnostics System (IPCS für PHP)

Ein hochstrukturiertes, vom Mainframe-Prinzip (ABEND/SNAP) inspiriertes Diagnose-Subsystem für PHP. Es ermöglicht die lückenlose Erfassung des Systemzustands bei Fehlern sowie das kontinuierliche Tracing ohne Prozessunterbrechung.

Die gesammelten Daten sind standardisiert und für die Visualisierung im zugehörigen **PySide6 DumpViewer** optimiert.

---

## 🏗️ Architektur & Funktionsweise

Das System arbeitet vollständig objektorientiert, nutzt das ressourcenschonende **PSR-4 Lazy Loading** und verzichtet komplett auf globale Variablen (`$GLOBALS`).

### 1. ABEND (Abnormal End)

Fängt kritische Laufzeitfehler über einen globalen Exception-Handler ab.

- Spiegelt die betroffene Closure via Reflection.
- Extrahiert lokale Variablen (`use`-Scope), Funktionsargumente und den Live-Trace.
- Generiert ein umfassendes JSON-Protokoll im Ordner `AbendDumps/`.

### 2. SNAP (Snapshot Dump)

Erlaubt es, an definierten Stellen im Code gezielte System-Snapshots zu erstellen, ohne das Skript mit `die()` oder `exit` zu beenden.

- Filtert interne Framework-Frames automatisch aus dem Stacktrace heraus.
- Schreibt strukturierte Snapshots nach `SnapDumps/`.

### 3. DEBUG TRACE (Kontinuierliche var_dump-Kette)

Ermöglicht das fortlaufende Sammeln von `var_dump`-Inhalten während eines Requests.

- Nutzt Output-Buffering (`ob_start`), um Ausgaben abzufangen.
- Schreibt Daten via `FILE_APPEND` sequenziell auf die Festplatte (`DebugDumps/`).
- Verhindert RAM-Überlastung bei langen Schleifen oder großen Datenmengen.

---

## 📁 Ordnerstruktur (Paket-Layout)

```code
src/
├── Collector/
│   ├── AbendCapture.php           # Überwacht riskante Code-Blöcke (Reflection)
│   └── DumpCollector.php          # Das Herzstück: Führt alle Daten für den ABEND-Dump zusammen
├── Debug/
│   └── DebugDumper.php            # Sequenzieller Stream-Logger für var_dumps
├── Environment/
│   └── EnvironmentCollector.php   # Erfasst PHP-Version, SAPI, OS und ini-Konfigurationen
├── Globals/
│   └── GlobalsCollector.php       # Normalisiert Superglobale (\$_GET, \(_POST,\)_SERVER etc.)
├── Memory/
│   └── MemoryCollector.php        # Erfasst aktuellen und maximalen RAM-Verbrauch
├── Normalizer/
│   └── ValueNormalizer.php        # Schützt vor Endlosschleifen (Objekte/Ressourcen -> String)
├── Snap/
│   └── SnapDump.php               # Erzeugt die manuellen Zwischen-Snapshots
├── Stacktrace/
    ├── LocalVariableCollector.php # Isoliert und filtert lokale Variablen
    ├── SignatureCollector.php     # Baut detaillierte Funktions- und Methoden-Signaturen
    ├── SourceSnippetCollector.php # Holt den Code-Ausschnitt rund um die Fehlerzeile (Padding)
    ├── StacktraceCollector.php    # Sammelt den vollständigen, erweiterten Stacktrace einer Exception
    └── SnapStacktraceCollector.php# Erstellt saubere, gefilterte Traces für SNAP-Dumps
├── Trace/
    └── GtfTrace.php               # Schreibt einen fortlaufenden Trace-Record im JSON-Lines-Format
```

---

## 🚀 Integration & Verwendung

### Autoloading aktivieren

Das System wird über PSR-4 in der `composer.json` registriert:

```json
{
    "name": "abend/diagnostic",
    "description": "Mainframe-inspired Abend, Snap and GTF Trace environment for PHP",
    "type": "library",
    "license": "MIT",
    "minimum-stability": "stable",
    "authors": [
        {
            "name": "Dietmar Ley",
            "email": "leydietmar@gmail.com"
        }
    ],
    "require": {
        "php": ">=8.0"
    },
    "autoload": {
        "psr-4": {
            "Abend\\": "src/"
        },
        "files": [
            "src/bootstrap.php"
        ]
    }
}
```

### In eigene PHP-MVC-Struktur einbinden (Beispiel)

```json
{
    "autoload": {
        "psr-4": {
            "App\\": "app/"
        }
    },
    "require": {
        "vlucas/phpdotenv": "^5.6",
        "pragmarx/google2fa-qrcode": "^3.0",
        "bacon/bacon-qr-code": "^3.1",
        "phpmailer/phpmailer": "^7.0",
        "intervention/image": "^3.11",
        "league/commonmark": "^2.7",
        "abend/diagnostic": "@dev"
    },
    "repositories": [
        {
            "type": "path",
            "url": "C:\\WebDev\\projects\\abend-diagnostic",
            "options": {
                "symlink": true
            }
        }
    ]
}
```

### 1. Globalen ABEND-Handler registrieren

In der zentralen Startdatei Ihres MVC (z. B. `bootstrap/bootstrap.php` oder `public/index.php`):

```php
use Abend\Collector\DumpCollector;

\$dumpDir = __DIR__ . '/../AbendDumps';

set_exception_handler(function (Throwable \$e) use (\(dumpDir) {\)dump = DumpCollector::collect(\(e);\)filename = date('Ymd_His') . '.json';

    file_put_contents(
        \(dumpDir . '/' .\)filename,
        json_encode(\$dump, JSON_PRETTY_PRINT)
    );
});
```

### 2. Riskante Blöcke überwachen (`AbendCapture`)

Im Controller werden kritische Operationen in eine Closure gepackt:

```php
use Abend\Collector\AbendCapture;

AbendCapture::execute(function () use (&\$foo, &\(bar, &\)result) {
    // Wenn dieser Block abstürzt, werden \$foo und \(bar im Dump gesichert\)result = \(foo / \)bar;
});
```

### 3. Fortlaufendes Tracing (`DebugDumper`)

Variablen-Zustände protokollieren, ohne den Prozess zu stoppen:

```php
use Abend\Debug\DebugDumper;

DebugDumper::dump("User vor Login", \$user);
DebugDumper::dump("Daten-Array", \$myArray);
```

### 4. Manuelle Snapshots erstellen (`SnapDump`)

Einen vollwertigen System-Snapshot an strategischen Punkten erzwingen:

```php
use Abend\Snap\SnapDump;

SnapDump::snap("Zustand vor API-Call", ["payload" => \$data]);
```

---

### 5. On-Demand Performance- & Event-Tracing (GtfTrace)

Fortlaufendes Tracing von System-Events im JSON-Lines-Format (JSONL). Die Aktivierung erfolgt flexibel per Code oder dynamisch im Browser via GET-Parameter (?gtf_trace).In der zentralen Startdatei (z. B. public/index.php)

```php
use Abend\Trace\GtfTrace;

// Initialisierung (wird standardmäßig über ?gtf_trace in der URL getriggert)
GtfTrace::init();
```

```php
use Abend\Trace\GtfTrace;

// Wichtige Systemereignisse mit Kontext protokollieren
GtfTrace::write('Database', 'QueryExecuted', ['sql' => $sql, 'duration_ms' => 12]);
GtfTrace::write('Auth', 'UserLoginAttempt', ['username' => $username]);
```

Features von GtfTrace:

- **On-Demand-Trigger**: Aktiviert sich automatisch, sobald `?gtf_trace` an die URL angehängt wird.
- **Automatischer Dateipfad**: Erstellt autonom den Ordner `GtfTraces/` im Projektverzeichnis und trennt Logs taggenau.
- **Tiefe Einblicke**: Jeder Eintrag enthält automatisch die aktuelle Speicherauslastung (`MemoryCollector`) sowie den exakten Aufruf-Stacktrace (`StacktraceCollector`).
- **Request-Tracking**: Eine eindeutige `request_id` verbindet alle Logzeilen desselben HTTP-Aufrufs.

---

## 🛠️ Daten-Normalisierung (Sicherheit)

Der `ValueNormalizer` bereitet alle Daten für JSON vor. Er schützt das System aktiv vor Abstürzen durch:

- **Maximale Tiefe (5 Ebenen)**: Verhindert Endlosschleifen bei zirkulären Objektreferenzen (`**depth_limit**`).
- **Objekt-Konvertierung**: Wandelt komplexe Instanzen via `get_object_vars` in lesbare Strukturen um.
- **Ressourcen-Handling**: Datenstrom-Verbindungen (wie PDO) werden sicher als `**resource**` markiert.
