<?php

namespace Abend\Snap;

use Abend\Stacktrace\SnapStacktraceCollector;
use Abend\Globals\GlobalsCollector;
use Abend\Environment\EnvironmentCollector;
use Abend\Memory\MemoryCollector;

class SnapDump
{
    public static function snap(
        string $label,
        array $context = [],
        bool $includeGlobals = false,
        bool $includeEnvironment = false
    ): void {
        $dump = [
            "type" => "SNAP",
            "label" => $label,
            "context" => $context,
            "meta" => [
                "timestamp" => date('c'),
                "version" => "1.1.0",
                "request_id" => bin2hex(random_bytes(8))
            ],
            'stacktrace' => SnapStacktraceCollector::collect(),

            // Vorher: collect_memory()
            MemoryCollector::collect()
        ];

        if ($includeGlobals) {
            $dump["globals"] = GlobalsCollector::collect();
        }

        if ($includeEnvironment) {
            $dump["environment"] = EnvironmentCollector::collect();
        }

        // 1. Projekt-Wurzel über die ausgeführte index.php ermitteln
        $projectRoot = dirname($_SERVER['SCRIPT_FILENAME']);

        // Falls das MVC-Framework eine public/index.php nutzt, gehen wir eine Ebene höher zur echten Root
        if (basename($projectRoot) === 'public') {
            $projectRoot = dirname($projectRoot);
        }

        // 2. Pfad für Windows/Linux normieren (verhindert gemischte Slashes)
        $dir = $projectRoot . '/Dumps/SnapDumps';
        $dir = str_replace(['/', '\\'], DIRECTORY_SEPARATOR, $dir);

        // 3. Ordner anlegen, falls er unter Windows physisch noch fehlt
        if (!is_dir($dir)) {
            mkdir($dir, 0777, true);
        }

        // 4. Dateiname und finaler, sicherer Schreibbefehl
        $filename = date('Ymd_His') . '_snap.json';
        $fullPath = $dir . DIRECTORY_SEPARATOR . $filename;

        file_put_contents(
            $fullPath,
            json_encode($dump, JSON_PRETTY_PRINT)
        );
    }
}
