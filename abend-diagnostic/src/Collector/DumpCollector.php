<?php

namespace Abend\Collector;

use Abend\Globals\GlobalsCollector;
use Abend\Environment\EnvironmentCollector;
use Abend\Memory\MemoryCollector;
use Abend\Stacktrace\StacktraceCollector;
use Throwable;

class DumpCollector
{
    /**
     * Erstellt einen vollständigen ABEND-Dump im Fehlerfall.
     */
    public static function collect(Throwable $e): array
    {
        $liveTrace = debug_backtrace(DEBUG_BACKTRACE_PROVIDE_OBJECT);

        return [
            'meta' => [
                'timestamp'  => date('c'),
                'version'    => '1.1.0',
                'session_id' => session_id() ?: null,
                'request_id' => $_SERVER['UNIQUE_ID'] ?? bin2hex(random_bytes(8)),
            ],

            'message'     => $e->getMessage(),
            'file'        => $e->getFile(),
            'line'        => $e->getLine(),
            'type'        => get_class($e),

            'stacktrace'  => StacktraceCollector::collect($e, $liveTrace),
            'globals'     => GlobalsCollector::collect(),
            'environment' => EnvironmentCollector::collect(),
            'memory'      => MemoryCollector::collect(),
        ];
    }

    /**
     * NEU: Schreibt die gesammelten Dump-Daten in das Projekt-Wurzelverzeichnis
     */
    public static function save(array $data): string
    {
        $projectRoot = dirname($_SERVER['SCRIPT_FILENAME']);
        if (basename($projectRoot) === 'public') {
            $projectRoot = dirname($projectRoot);
        }

        // Hier wird "Dumps" als Zwischenordner eingefügt
        $dir = $projectRoot . '/Dumps/AbendDumps';
        $dir = str_replace(['/', '\\'], DIRECTORY_SEPARATOR, $dir);

        if (!is_dir($dir)) {
            mkdir($dir, 0777, true);
        }

        $dumpFile = $dir . DIRECTORY_SEPARATOR . date('Ymd_His') . '_abend.json';

        // Datei als formatiertes JSON schreiben (nur einmal!)
        file_put_contents(
            $dumpFile,
            json_encode($data, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT)
        );

        return $dumpFile;
    }
}
