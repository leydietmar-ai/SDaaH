<?php

namespace Abend\Environment;

class EnvironmentCollector
{
    /**
     * Sammelt System- und Konfigurationsdaten der PHP-Umgebung.
     */
    public static function collect(): array
    {
        return [
            'php_version'   => PHP_VERSION,
            'sapi'          => PHP_SAPI,
            'os'            => PHP_OS_FAMILY,
            'extensions'    => get_loaded_extensions(),
            'ini'           => [
                'memory_limit'    => ini_get('memory_limit'),
                'error_reporting' => ini_get('error_reporting'),
                'display_errors'  => ini_get('display_errors'),
                'log_errors'      => ini_get('log_errors'),
            ],
        ];
    }
}
