<?php

namespace Abend\Collector;

use ReflectionFunction;
use Throwable;

class AbendCapture
{
    /**
     * @var array Speicher für die lokalen Variablen der Closure
     */
    private static array $lastLocals = [];

    /**
     * Führt eine Closure aus und fängt den Zustand im Fehlerfall ab.
     */
    public static function execute(callable $fn)
    {
        try {
            return $fn();
        } catch (Throwable $e) {
            // Die Closure selbst reflektieren
            $ref = new ReflectionFunction($fn);

            // Alle Variablen, die per "use" in die Closure kommen
            self::$lastLocals = $ref->getStaticVariables();

            throw $e;
        }
    }

    /**
     * Ermöglicht es anderen Klassen (z. B. collect_locals), die Variablen auszulesen
     */
    public static function getLastLocals(): array
    {
        return self::$lastLocals;
    }
}
