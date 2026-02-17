<?php

/**
 * Framework 3.1
 *
 * /app/Config/Config.php - C O N F I G
 */

// Helfer für Pfade
define('APPROOT', dirname(dirname(__FILE__)));
define('URLROOT', $_ENV['APP_URL'] ?? 'http://localhost');
define('POSTS_UPLOAD_PATH', '/blogposts/');
// Springt zwei Ebenen nach oben, um aus /app/config oder /app direkt ins Rootverzeichnis zu kommen
define('DATAPATH', dirname(__DIR__, 2) . '/data/');
// Der physische Pfad zum Public-Ordner auf dem Server
define('PUBLICPATH', dirname(__DIR__, 2) . '/public');
// Der physische Pfad zum storage-Ordner und code-Ordner
define('STORAGE_PATH', realpath(__DIR__ . '/../../storage'));
define('CODE_PATH', STORAGE_PATH . DIRECTORY_SEPARATOR . 'code');

// --------------------------------------------------------------
//  Rollen & Berechtigungen
// --------------------------------------------------------------
define('ROLE_TEMPLATES', [
    "editor_base" => [
        "can_edit_all"   => true,
        "can_view_all"   => true,
    ],
    "owner_base" => [
        "can_edit_own"   => true,
        "can_delete_own" => true,
        "can_view_role"  => true,
        "can_view_own"   => true,
    ]
]);

define('PERMISSIONS', [
    "admin" => array_merge(ROLE_TEMPLATES['editor_base'], [
        "can_manage_users" => true,
    ]),
    "moderator" => ROLE_TEMPLATES['editor_base'],
    "user" => ROLE_TEMPLATES['owner_base'],
    "guest" => [
        "can_view_own" => true,
    ],
]);

define('DEFAULT_ROLE', 'guest');

define('ROLE_DESCRIPTIONS', [
    "admin" => "Vollzugriff auf alle Funktionen und Benutzerverwaltung",
    "moderator" => "Kann Inhalte bearbeiten und moderieren",
    "user" => "Kann eigene Inhalte verwalten und Beiträge der Gruppe sehen",
    "guest" => "Kann eigene Inhalte sehen",
]);

define('ROLE_LABELS', [
    'admin' => 'Administrator',
    'moderator' => 'Moderator',
    'user' => 'Privatnutzer',
    'guest' => 'Gast',
]);

define('PUBLIC_CATEGORIES', ['Sonstiges', 'Fachbeiträge', 'News']);

return [
    "app" => [
        "name"      => "...Projekt-Name...",
        "url"       => $_ENV['APP_URL'] ?? 'http://deine URL',
        // Alt:
        // "base_path" => $_ENV['APP_BASE_PATH'] ?? '/...Pprojekt-Verzeichnis...',

        // Neu (Sicherer für 2026):
        "base_path" => $_SERVER['APP_BASE_PATH'] ?? getenv('APP_BASE_PATH') ?: '/...Projekt-Verzeichnis...',
        "env"       => $_ENV['APP_ENV'] ?? 'production',
    ],

    // Datenbank
    "mysql" => [
        "host"    => $_ENV['DB_HOST'],
        "name"    => $_ENV['DB_NAME'],
        "user"    => $_ENV['DB_USER'],
        "pass"    => $_ENV['DB_PASS'],
        "charset" => "utf8mb4"
    ],

    // Session (Wichtig für index.php Punkt 5)
    "session" => [
        "timeout" => $_ENV['SESSION_TIMEOUT'] ?? 1800,
    ],

    "mailer" => [
        "username" => $_ENV['MAIL_USER'],
        "clientId" => $_ENV['MAIL_CLIENT_ID'],
        "clientSecret" => $_ENV['MAIL_CLIENT_SECRET'],
        "refreshToken" => $_ENV['MAIL_REFRESH_TOKEN'],
        "from" => $_ENV['MAIL_FROM'],
        "port" => 587,
        "host" => "smtp.gmail.com",
        "authType" => "XOAUTH2",

        "email_password_reset" => "PASSWORD_RESET",
        "email_password_reset_subject" => "Passwort zurücksetzen",
        "email_password_reset_url"     => BASE_URL . "/auth/reset-password",
    ],

    "auth" => [
        "default_role" => "guest",
        "roles" => [
            "admin" => ["label" => "Administrator", "can_manage" => true],
            "moderator" => ["label" => "Moderator", "can_edit" => true],
            "guest" => ["label" => "Gast", "can_view" => true]
        ]
    ]
];
