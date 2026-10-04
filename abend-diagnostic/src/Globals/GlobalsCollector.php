<?php

namespace Abend\Globals;

class GlobalsCollector
{
    /**
     * Sammelt und normalisiert alle superglobalen PHP-Variablen.
     */
    public static function collect(): array
    {
        return [
            'get'     => \Abend\Normalizer\ValueNormalizer::normalize($_GET ?? []),
            'post'    => \Abend\Normalizer\ValueNormalizer::normalize($_POST ?? []),
            'cookie'  => \Abend\Normalizer\ValueNormalizer::normalize($_COOKIE ?? []),
            'server'  => \Abend\Normalizer\ValueNormalizer::normalize($_SERVER ?? []),
            'files'   => \Abend\Normalizer\ValueNormalizer::normalize($_FILES ?? []),
            'session' => isset($_SESSION) ? \Abend\Normalizer\ValueNormalizer::normalize($_SESSION) : null,
        ];
    }
}
