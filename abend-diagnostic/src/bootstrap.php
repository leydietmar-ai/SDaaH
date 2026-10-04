<?php

namespace Abend;

use Abend\Trace\GtfTrace;
use Abend\Collector\DumpCollector;
use Abend\Snap\SnapDump;
use Abend\Debug\DebugDumper; // Neu importiert für das Start-Event

/**
 * Automatischer Systemstart des Diagnose-Subsystems.
 * Klinkt sich über den Composer-Autoloader global in den PHP-Prozess ein.
 */

// 1. GTF-Trace sofort beim Request-Start initialisieren
GtfTrace::init();

// NEU: Sofortige Start-Meldung in den GTF-Trace schreiben (falls aktiv)
GtfTrace::write('SYSTEM', 'SUBSYSTEM_INIT', [
    'message' => 'Mainframe Diagnostics Subsystem erfolgreich gestartet.',
    'script'  => $_SERVER['SCRIPT_FILENAME'] ?? 'CLI'
]);

// NEU: Sofortige Start-Meldung in den Debug-Dumper schreiben - ausgesetzt!!!
// Dadurch wird der Ordner "DebugDumps" und die .log-Datei ab sofort bei JEDEM Request erstellt!
//DebugDumper::dump('SUBSYSTEM_START', 'Diagnose-Umgebung fuer diesen Request aktiv.');

// 2. Globalen Exception-Handler registrieren (Fängt ungefangene Ausnahmen ab)
set_exception_handler(function (\Throwable $exception) {
    GtfTrace::write('SYSTEM', 'UNCAUGHT_EXCEPTION', [
        'message' => $exception->getMessage(),
        'file'    => $exception->getFile(),
        'line'    => $exception->getLine()
    ]);

    $dumpData = DumpCollector::collect($exception);
    DumpCollector::save($dumpData);

    SnapDump::snap("ABEND - Uncaught Exception", [
        'exception_class' => get_class($exception)
    ]);

    throw $exception;
});


// 3. Globalen Shutdown-Handler registrieren (Fängt fatale Parse-/Laufzeitfehler ab)
register_shutdown_function(function () {
    $error = error_get_last();

    if ($error && in_array($error['type'], [E_ERROR, E_PARSE, E_CORE_ERROR, E_COMPILE_ERROR])) {
        GtfTrace::write('SYSTEM', 'FATAL_ABEND', [
            'message' => $error['message']
        ]);

        $exception = new \ErrorException($error['message'], 0, $error['type'], $error['file'], $error['line']);
        $dumpData = DumpCollector::collect($exception);
        DumpCollector::save($dumpData);
    }
});
