<?php

namespace Abend\Stacktrace;

use ReflectionException;
use ReflectionFunction;
use ReflectionFunctionAbstract;
use ReflectionMethod;

class SignatureCollector
{
    /**
     * Erstellt eine detaillierte String-Signatur für ein Stack-Frame.
     */
    public static function collect(array $frame): string
    {
        // 1. Closure?
        if (isset($frame['function']) && str_starts_with($frame['function'], '{closure')) {
            return self::buildClosureSignature($frame);
        }

        // 2. Normale Funktion oder Methode
        $function = $frame['function'] ?? null;
        $class    = $frame['class'] ?? null;

        if (!$function) {
            return 'callable {unknown}';
        }

        try {
            if ($class) {
                $ref = new ReflectionMethod($class, $function);
                return self::buildMethodSignature($ref);
            } else {
                $ref = new ReflectionFunction($function);
                return self::buildFunctionSignature($ref);
            }
        } catch (ReflectionException $e) {
            return "function {$function}()";
        }
    }

    private static function buildClosureSignature(array $frame): string
    {
        $file = $frame['file'] ?? 'unknown';
        $line = $frame['line'] ?? '?';
        $origin = $frame['function'];

        return "closure at {$origin} ({$file}:{$line})";
    }

    private static function buildMethodSignature(ReflectionMethod $ref): string
    {
        $parts = [];

        if ($ref->isPrivate()) {
            $parts[] = 'private';
        } elseif ($ref->isProtected()) {
            $parts[] = 'protected';
        } else {
            $parts[] = 'public';
        }

        if ($ref->isStatic()) {
            $parts[] = 'static';
        }

        $name = $ref->getDeclaringClass()->getName() . '::' . $ref->getName();
        $params = self::buildParameterList($ref);

        $signature = implode(' ', $parts) . " function {$name}({$params})";

        if ($ref->hasReturnType()) {
            $signature .= ': ' . (string)$ref->getReturnType();
        }

        return $signature;
    }

    private static function buildFunctionSignature(ReflectionFunction $ref): string
    {
        $name = $ref->getName();
        $params = self::buildParameterList($ref);

        $signature = "function {$name}({$params})";

        if ($ref->hasReturnType()) {
            $signature .= ': ' . (string)$ref->getReturnType();
        }

        return $signature;
    }

    private static function buildParameterList(ReflectionFunctionAbstract $ref): string
    {
        $params = [];

        foreach ($ref->getParameters() as $param) {
            $p = '';

            if ($param->hasType()) {
                $p .= (string)$param->getType() . ' ';
            }

            if ($param->isPassedByReference()) {
                $p .= '&';
            }

            if ($param->isVariadic()) {
                $p .= '...';
            }

            $p .= '$' . $param->getName();

            if ($param->isOptional() && $param->isDefaultValueAvailable()) {
                $p .= ' = ' . json_encode($param->getDefaultValue());
            }

            $params[] = $p;
        }

        return implode(', ', $params);
    }
}
