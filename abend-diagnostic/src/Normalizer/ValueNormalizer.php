<?php

namespace Abend\Normalizer;

class ValueNormalizer
{
    /**
     * Normalisiert beliebige Werte (Arrays, Objekte, Ressourcen) für die sichere JSON-Serialisierung.
     */
    public static function normalize($value, int $depth = 0)
    {
        // Rekursion begrenzen
        if ($depth > 5) {
            return '**depth_limit**';
        }

        // Skalare Werte direkt zurückgeben
        if (is_scalar($value) || $value === null) {
            return $value;
        }

        // Arrays rekursiv normalisieren
        if (is_array($value)) {
            $normalized = [];
            foreach ($value as $key => $item) {
                $normalized[$key] = self::normalize($item, $depth + 1);
            }
            return $normalized;
        }

        // Objekte normalisieren
        if (is_object($value)) {
            return [
                '__class' => get_class($value),
                '__properties' => self::normalize(get_object_vars($value), $depth + 1)
            ];
        }

        // Ressourcen
        if (is_resource($value)) {
            return '**resource**';
        }

        // Fallback
        return (string)$value;
    }
}
