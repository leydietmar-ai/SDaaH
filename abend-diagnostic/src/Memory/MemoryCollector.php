<?php

namespace Abend\Memory;

class MemoryCollector
{
    /**
     * Sammelt den aktuellen und den maximalen Speicherverbrauch.
     */
    public static function collect(): array
    {
        return [
            'usage'      => memory_get_usage(true),
            'peak_usage' => memory_get_peak_usage(true),
        ];
    }
}
