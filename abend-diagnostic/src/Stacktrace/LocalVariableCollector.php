<?php

namespace Abend\Stacktrace;

use Abend\Collector\AbendCapture;
use Throwable;

class LocalVariableCollector
{
    /**
     * Sammelt und bereinigt lokale Variablen aus verschiedenen Quellen.
     */
    public static function collect(array $exceptionFrame, array $liveFrame): array
    {
        $locals = [];

        // 1. Variablen aus AbendCapture (statt globalem Array)
        $capturedLocals = AbendCapture::getLastLocals();
        foreach ($capturedLocals as $name => $value) {
            $locals[$name] = $value;
        }

        // 2. Funktionsargumente aus Exception-Trace
        if (isset($exceptionFrame['args'])) {
            foreach ($exceptionFrame['args'] as $name => $value) {
                $locals[$name] = $value;
            }
        }

        // 3. Live-Trace Variablen
        if (isset($liveFrame['args'])) {
            foreach ($liveFrame['args'] as $name => $value) {
                $locals[$name] = $value;
            }
        }

        // 4. $this separat behandeln
        $thisObject = null;
        if (isset($liveFrame['object'])) {
            $thisObject = \Abend\Normalizer\ValueNormalizer::normalize($liveFrame['object']);
        }

        // 5. Filtern
        $clean = [];
        foreach ($locals as $key => $value) {
            // numerische Keys entfernen
            if (is_int($key)) {
                continue;
            }

            // Funktionsargumente entfernen
            if (str_starts_with($key, 'arg_')) {
                continue;
            }

            // $this entfernen (kommt separat)
            if ($key === 'this') {
                continue;
            }

            // Exceptions entfernen
            if ($value instanceof Throwable) {
                continue;
            }

            // Vorher: $clean[$key] = normalize_value($value);
            $clean[$key] = \Abend\Normalizer\ValueNormalizer::normalize($value);
        }

        // 6. Alphabetisch sortieren
        ksort($clean);

        // 7. $this separat anhängen
        if ($thisObject !== null) {
            $clean['this'] = $thisObject;
        }

        return $clean;
    }
}
