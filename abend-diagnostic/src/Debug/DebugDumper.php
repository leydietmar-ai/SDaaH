<?php

namespace Abend\Debug;

class DebugDumper
{
    /**
     * @var string|null Pfad zur Logdatei dieses Requests
     */
    private static ?string $file = null;

    /**
     * Schreibt einen var_dump-Eintrag fortlaufend in eine Logdatei.
     */
    public static function dump(string $label, mixed $value): void
    {
        if (self::$file === null) {
            // 1. Projekt-Wurzel über die ausgeführte index.php ermitteln
            $projectRoot = dirname($_SERVER['SCRIPT_FILENAME']);

            // Falls das MVC-Framework eine public/index.php nutzt, eine Ebene höher gehen
            if (basename($projectRoot) === 'public') {
                $projectRoot = dirname($projectRoot);
            }

            // 2. Pfad für Windows/Linux normieren (verhindert gemischte Slashes)
            $dir = $projectRoot . '/Dumps/DebugDumps';
            $dir = str_replace(['/', '\\'], DIRECTORY_SEPARATOR, $dir);

            // 3. Ordner anlegen, falls er noch fehlt
            if (!is_dir($dir)) {
                mkdir($dir, 0777, true);
            }

            // 4. Eine Datei pro Lauf generieren (mit korrekten Trennzeichen)
            self::$file = $dir . DIRECTORY_SEPARATOR . 'debugdump_' . date('Ymd_His') . '.log';
        }

        // Output von var_dump abfangen
        ob_start();
        var_dump($value);
        $dump = ob_get_clean();

        // Zeitstempel erzeugen
        $timestamp = date('Y-m-d H:i:s');

        // Eintrag mit Label und Zeitstempel formatieren
        $entry  = "[$timestamp] === DEBUGDUMP: $label ===\n";
        $entry .= $dump . "\n";

        // Inhalt sequenziell anhängen
        file_put_contents(self::$file, $entry, FILE_APPEND);
    }

    /**
     * Ermöglicht es, den aktuellen Log-Pfad auszulesen, falls benötigt.
     */
    public static function getLogFile(): ?string
    {
        return self::$file;
    }
}
