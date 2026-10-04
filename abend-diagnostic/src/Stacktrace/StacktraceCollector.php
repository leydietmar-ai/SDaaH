<?php

namespace Abend\Stacktrace;

use Throwable;

class StacktraceCollector
{
    /**
     * Sammelt den vollständigen, erweiterten Stacktrace einer Exception.
     */
    public static function collect(Throwable $e, array $liveTrace): array
    {
        $exceptionTrace = $e->getTrace();
        $frames = [];

        foreach ($exceptionTrace as $i => $frame) {

            // Das passende Live-Frame holen
            $liveFrame = $liveTrace[$i] ?? [];

            // Datei & Zeile bestimmen
            $file = $frame['file'] ?? $e->getFile();
            $line = $frame['line'] ?? $e->getLine();

            // Frame bauen und normalisieren
            $frames[] = self::normalizeFrame([
                'file'      => $file,
                'line'      => $line,
                'function'  => $frame['function'] ?? null,
                'class'     => $frame['class'] ?? null,
                'type'      => $frame['type'] ?? null,
                'signature' => SignatureCollector::collect($frame),
                'locals'    => LocalVariableCollector::collect($frame, $liveFrame), // Unsere neue Klasse!
                'snippet'   => SourceSnippetCollector::collect($file, $line),

            ]);
        }

        return $frames;
    }

    /**
     * Sammelt den aktuellen Stacktrace im laufenden Betrieb (für den GTF-Trace).
     */
    public static function collectCurrent(int $limit = 3): array
    {
        // Holt die aktuellen Aufrufe im System (Limit schont die Performance)
        $trace = debug_backtrace(DEBUG_BACKTRACE_IGNORE_ARGS, $limit + 1);

        // Den ersten Frame abschneiden, da das dieser Collector selbst ist
        array_shift($trace);

        $frames = [];
        foreach ($trace as $frame) {
            $file = $frame['file'] ?? 'unknown';
            $line = $frame['line'] ?? 0;

            $frames[] = self::normalizeFrame([
                'file'      => $file,
                'line'      => $line,
                'function'  => $frame['function'] ?? 'unknown',
                'class'     => $frame['class'] ?? null,
                'type'      => $frame['type'] ?? null,
                'signature' => 'callable',
                'locals'    => [], // Im schnellen Trace lassen wir locals weg
                'snippet'   => []  // Snippets sparen wir uns für echte ABENDs/Snaps
            ]);
        }

        return $frames;
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

            // WICHTIG: locals als Array lassen!
            'locals'    => is_array($frame['locals'] ?? null) ? $frame['locals'] : [],

            'snippet'   => $frame['snippet'] ?? [],
        ];
    }
}
