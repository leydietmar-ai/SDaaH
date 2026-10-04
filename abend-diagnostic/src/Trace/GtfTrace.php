<?php

namespace Abend\Trace;

use Abend\Memory\MemoryCollector;
use Abend\Stacktrace\StacktraceCollector;

class GtfTrace
{
    private static bool $active = false;
    private static ?string $traceFile = null;
    private static string $requestId = '';

    /**
     * Initialisiert den Trace und prüft das "Bei-Bedarf"-Flag.
     */
    public static function init(bool $enabled = false): void
    {
        if ($enabled || isset($_GET['gtf_trace'])) {
            self::$active = true;
        }

        if (!self::$active) {
            return;
        }

        if (self::$traceFile === null) {
            self::$requestId = bin2hex(random_bytes(8));

            // 1. Projekt-Wurzel über die ausgeführte index.php ermitteln
            $projectRoot = dirname($_SERVER['SCRIPT_FILENAME']);
            if (basename($projectRoot) === 'public') {
                $projectRoot = dirname($projectRoot);
            }

            // 2. Pfad für Windows/Linux normieren
            $dir = $projectRoot . '/Dumps/GtfTraces';
            $dir = str_replace(['/', '\\'], DIRECTORY_SEPARATOR, $dir);

            // 3. Ordner anlegen
            if (!is_dir($dir)) {
                mkdir($dir, 0777, true);
            }

            // 4. Finaler Pfad mit korrekten Trennzeichen
            self::$traceFile = $dir . DIRECTORY_SEPARATOR . date('Ymd_His') . '_gtf.jsonl';
        }
    }

    /**
     * Schreibt einen fortlaufenden Trace-Record im JSON-Lines-Format.
     */
    public static function write(string $component, string $event, array $context = []): void
    {
        if (self::$traceFile === null && !self::$active) {
            self::init();
        }

        if (!self::$active) {
            return;
        }

        $record = [
            'timestamp'  => date('c'),
            'request_id' => self::$requestId,
            'component'  => strtoupper($component),
            'event'      => strtoupper($event),
            'context'    => $context,
            'memory'     => MemoryCollector::collect(),
            'calling_stack' => StacktraceCollector::collectCurrent(2)
        ];

        file_put_contents(
            self::$traceFile,
            json_encode($record, JSON_UNESCAPED_SLASHES) . "\n",
            FILE_APPEND
        );
    }
}
