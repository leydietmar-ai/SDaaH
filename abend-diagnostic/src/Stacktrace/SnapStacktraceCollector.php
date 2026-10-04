<?php

namespace Abend\Stacktrace;

class SnapStacktraceCollector
{
    /**
     * Erstellt einen gefilterten Stacktrace speziell für SNAP-Snapshot-Dumps.
     */
    public static function collect(): array
    {
        $trace = debug_backtrace(DEBUG_BACKTRACE_PROVIDE_OBJECT);

        // SnapDump‑interne Frames entfernen
        $filtered = array_filter($trace, function ($frame) {
            if (!isset($frame['file'])) {
                return true;
            }
            return !str_contains($frame['file'], 'SnapDump.php');
        });

        $frames = [];

        foreach ($filtered as $frame) {
            $file = $frame['file'] ?? 'unknown';
            $line = $frame['line'] ?? 0;

            $frames[] = self::normalizeFrame([
                'file'      => $file,
                'line'      => $line,
                'function'  => $frame['function'] ?? null,
                'class'     => $frame['class'] ?? null,
                'type'      => $frame['type'] ?? null,
                'signature' => SignatureCollector::collect($frame),
                'locals'    => LocalVariableCollector::collect($frame, $frame),
                'snippet'   => SourceSnippetCollector::collect($file, $line),
            ]);
        }

        return array_values($frames);
    }

    /**
     * Normalisiert ein einzelnes Stack-Frame für eine saubere JSON-Struktur.
     */
    private static function normalizeFrame(array $frame): array
    {
        return [
            'file'      => $frame['file'] ?? 'unknown',
            'line'      => isset($frame['line']) ? (int)$frame['line'] : 0,
            'function'  => $frame['function'] ?? 'unknown',
            'class'     => $frame['class'] ?? null,
            'type'      => $frame['type'] ?? null,
            'signature' => $frame['signature'] ?? 'callable {unknown}',
            'locals'    => is_array($frame['locals'] ?? null) ? $frame['locals'] : [],
            'snippet'   => $frame['snippet'] ?? [],
        ];
    }
}
