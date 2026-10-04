<?php

namespace Abend\Stacktrace;

class SourceSnippetCollector
{
    /**
     * Holt einen definierten Code-Ausschnitt rund um eine bestimmte Zeile.
     */
    public static function collect(string $file, int $line, int $context = 3): array
    {
        if (!is_readable($file)) {
            return [];
        }

        $lines = @file($file, FILE_IGNORE_NEW_LINES);
        if (!$lines) {
            return [];
        }

        $total = count($lines);

        // Start- und Endbereich berechnen
        $start = max(1, $line - $context);
        $end   = min($total, $line + $context);

        $snippet = [];

        for ($i = $start; $i <= $end; $i++) {
            $snippet[] = [
                'line'    => $i,
                'code'    => $lines[$i - 1] ?? '',
                'current' => ($i === $line),
            ];
        }

        // Jetzt sicherstellen, dass wir GENAU 1 + 2*$context Zeilen haben
        // (z. B. 7 Zeilen bei context=3)
        $expected = 1 + 2 * $context;

        while (count($snippet) < $expected) {
            $snippet[] = [
                'line'    => null,
                'code'    => '',
                'current' => false,
            ];
        }

        return $snippet;
    }
}
