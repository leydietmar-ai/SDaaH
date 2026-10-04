# WebDev - Web Development für Windows 11 ohne WSL (Der Verzeichnisname ist frei wählbar!)

## Installation einer lokalen Serverumgebung mit den Komponenten Apache Webserver, MariaDB, PHP und phyMyAdmin

***Die folgenden Informationen habe ich mir alle aus dem Internet zusammengetragen und entsprechend umgesetzt.***
***Bis dahin hatte ich auf XAMPP gesetzt, das aber seit langer Zeit nicht mehr aktualisiert wird!***

### Download der einzelnen Komponenten (mit den eingesetzten und getesteten Versionen)

#### Apache Webserver (Apache Lounge)

> Apache 2.4.68-260920 Win64
> httpd-2.4.68-260920-win64-VS17.zip  
>
> Sicherstellen, dass die letzte Version von Visual C++ Redistributable Visual Studio 2017-2026 > installiert ist (Bei mir ist das 14.51.36247)!
> Kann sonst auch von dieser Webseite geladen und installiert werden.

Heruntergeladen von <http://www.apachelounge.com/download>

#### PHP for Windows

> VS17 x64 Thread Safe 2026-Sep-22 14:35:07 UTC PHP 8.5.11
>
> Wichtig ist es, die "Thread-Safe-Version" zu wählen (ZIP)!

Heruntergeladen von <https://windows.php.net/download>

#### MariaDB (Windows Installer)

> MariaDB Version 13.0.2

Heruntergeladen von <https://mariadb.com/downloads>

#### phpMyAdmin (ZIP-Datei)

> Download Button rechts oben auf der Seite **(z.Zt. 5.2.3)**

Heruntergeladen von <https://www.phpmyadmin.net/>

#### Für die weniger Erfahrenen

- Die ZIP-Dateien erstmal irgendwohin entpacken (z.B. unter Downloads), da die Produkte auch die Version mit enthalten (apache24, usw.).
- Aus diesen entpackten Ordnern dann nur die Unterordner und Dateien so in das Zielverzeichnis kopieren (apache, php), wobei phpmyadmin unter apache/conf/phpmyadmin kopiert werden muss!
- Für die MariaDB wird der Zielordner direkt im GUI-Dialog gesetzt!

### Anlegen der Ordnerstruktur (Meine Version - kann natürlich frei gewählt werden!)

    Windows (C):/
    ├── WebDev/
    │   ├── apache/
    │   │   ├── ...
    │   │   ├── conf/
    │   │   │   │   ├── ...
    │   │   │   │   ├── httpd.conf
    │   │   │   │   └── ...
    │   │   ├── ...
    │   │   ├── htdocs/
    │   │   │   ├── phpmyadmin/
    │   │   │   │   ├── ...
    │   │   │   │   ├── config.inc.php
    │   │   │   │   └── ...
    │   │   └── ...
    │   ├── mariadb/
    │   ├── php/
    │   │   ├── ...
    │   │   ├── php.ini
    │   │   ├── ...
    │   ├── projects/
    │   │   ├── ...
    │   │   ├── ...
    │   │   ├── ...
    │   │   └── ...

Die Unterordner werden natürlich durch die Installation der einzelnen Anwendungen angelegt.

Anpassungen sind in den namentlich aufgeführten Dateien erforderlich!

Alle folgenden Punkte beziehen sich auf diese Struktur und müssen bei Abweichungen berücksichtigt werden!

### Erforderliche Anpassungen

#### Anpassungen Apache Webserver (httpd.conf)

##### Server Root anpassen

        Define SRVROOT "C:/WebDev/apache"
        ServerRoot "${SRVROOT}"

##### PHP bezogene Angaben (nach dem letzten #LoadModule ... einfügen)

        #PHP-Modul laden
        LoadModule php_module "C:/WebDev/php/php8apache2_4.dll" 
        #PHP-Dateien an das Modul übergeben
        AddHandler application/x-httpd-php .php
        #Pfad zur php.ini
        PHPIniDir "C:/WebDev/php"

##### **Bei einer neuen Apache-Version muss die Zeile (php_module…) eventuell angepasst werden!**

        *Bibliotheken für PHP 8.5.11 (ICU 77)*
        LoadFile "C:/WebDev/php/icuuc77.dll"
        LoadFile "C:/WebDev/php/icuin77.dll"
        LoadFile "C:/WebDev/php/icudt77.dll"
        LoadFile "C:/WebDev/php/icuio77.dll"

##### Dokument Root und Alias für phpMyAdmin (ersetzt DocumentRoot - so übernehmen)

        #
        # DocumentRoot: The directory out of which you will serve your
        # documents. By default, all requests are taken from this directory, but
        # symbolic links and aliases may be used to point to other locations.
        #
        # Statt Standard-htdocs jetzt der eigene projects-Ordner
        DocumentRoot "C:/WebDev/projects"
        <Directory "C:/WebDev/projects">
            Options Indexes FollowSymLinks
            AllowOverride All
            Require all granted
        </Directory>

        # Alias für phpMyAdmin
        Alias /phpmyadmin "C:/WebDev/apache/htdocs/phpmyadmin"

        <Directory "C:/WebDev/apache/htdocs/phpmyadmin">
            Options Indexes FollowSymLinks
            AllowOverride All
            Require all granted
        </Directory>

        # http://localhost/phpmyadmin zeigt nur die Directory Struktur an
        # wenn index.php nicht gesetzt ist!
        #
        # DirectoryIndex: sets the file that Apache will serve if a directory
        # is requested.
        #
        <IfModule dir_module>
            DirectoryIndex index.php index.html
        </IfModule>

### Installation der MariaDB (unbedingt als Administrator ausführen) erfolgt als GUI

#### Angabe des Ordners in die die Anwendung installiert werden soll

        C:/WebDev/mariadb

#### Weiteres Fenster für Passwort-Vergabe und anderes (nicht ändern)

Hier eintscheidet man, ob die Umgebung geschützt werden soll oder nicht. Dieses Passwort muss dann bei Aufruf von phpMyAdmin angegeben werden (siehe Startfenster).

Wichtig! Nach der Installation müssen die Ordner mariadb/bin und mariadb/data vorhanden sein, da sonst die Installation nicht mit Admin-Rechten erfolgt ist!

Standardmäßig wird in das Verzeichnis C:/Programme/MariDB ... installiert.

Hinweis: MariaDB wird automatisch als Dienst eingerichtet und gestartet

Vor einer eventuellen Neuinstallation mit Entfernen der alten Version muss dieser Dienst vorher über den Taskmanager gestoppt werden!

### phpMyAdmin (config.inc.php)

#### Neue Datei config.inc.php anlegen und config.sample.inc.php da hineinkopieren

        "blowfish_secret" wird beim Aufruf von phpMyAdmin bemängelt, wenn nicht gesetzt!
        
        /**
        * This is needed for cookie based authentication to encrypt the cookie.
        * Needs to be a 32-bytes long string of random bytes. See FAQ 2.10.
        */

        $cfg['blowfish_secret'] = 'KjN2MWjuaoxro03DbHCdjq76IAY5VEMt';

Es gibt einige Blowfish-Generatoren im Internet, die man benutzen kann:
Zum Beispiel: <https://yawpp.com/tools/blowfish-secret-generator/>

        Zu ändernde Server-Angaben:

        /**
        * First server
        */
        $i++;
        /* Authentication type */
        $cfg['Servers'][$i]['auth_type'] = 'cookie';
        /* Server parameters */
        $cfg['Servers'][$i]['host'] = 'localhost';
        $cfg['Servers'][$i]['user'] = 'root'; /* mein Standard, oder welchen Benutzer auch immer */
        $cfg['Servers'][$i]['password'] = '...password aus MariaDB Konfigurations-Dialog... sonst leer';  
        $cfg['Servers'][$i]['AllowNoPassword'] = false; /* true -> kein Password erforderlich */

        /**
        * phpMyAdmin configuration storage settings.
        */
        /* User used to manipulate with storage */
        // $cfg['Servers'][$i]['controlhost'] = '';
        // $cfg['Servers'][$i]['controlport'] = '';
        $cfg['Servers'][$i]['controluser'] = 'pma';
        $cfg['Servers'][$i]['controlpass'] = 'pmapass';

        /* Storage database and tables */
        $cfg['Servers'][$i]['pmadb'] = 'pmadb';
        $cfg['Servers'][$i]['bookmarktable'] = 'pma__bookmark';
        $cfg['Servers'][$i]['relation'] = 'pma__relation';
        $cfg['Servers'][$i]['table_info'] = 'pma__table_info';
        $cfg['Servers'][$i]['table_coords'] = 'pma__table_coords';
        $cfg['Servers'][$i]['pdf_pages'] = 'pma__pdf_pages';
        $cfg['Servers'][$i]['column_info'] = 'pma__column_info';
        $cfg['Servers'][$i]['history'] = 'pma__history';
        $cfg['Servers'][$i]['table_uiprefs'] = 'pma__table_uiprefs';
        $cfg['Servers'][$i]['tracking'] = 'pma__tracking';
        $cfg['Servers'][$i]['userconfig'] = 'pma__userconfig';
        $cfg['Servers'][$i]['recent'] = 'pma__recent';
        $cfg['Servers'][$i]['favorite'] = 'pma__favorite';
        $cfg['Servers'][$i]['users'] = 'pma__users';
        $cfg['Servers'][$i]['usergroups'] = 'pma__usergroups';
        $cfg['Servers'][$i]['navigationhiding'] = 'pma__navigationhiding';
        $cfg['Servers'][$i]['savedsearches'] = 'pma__savedsearches';
        $cfg['Servers'][$i]['central_columns'] = 'pma__central_columns';
        $cfg['Servers'][$i]['designer_settings'] = 'pma__designer_settings';
        $cfg['Servers'][$i]['export_templates'] = 'pma__export_templates';

        /**
        * End of servers configuration
        */

#### PMA-Controluser anlegen und Passwort ändern (unter phpMyAdmin per SQL)

Oft findet man statt „pmadb“ auch „phpmyadmin“. Das muss dann in folgendem Statement berücksichtigt werden:

        $cfg['Servers'][$i]['pmadb'] = 'pmadb | phpmyadmin'; (config.inc.php)

        Control-User für phpMyAdmin anlegen
        CREATE USER 'pma'@'localhost' IDENTIFIED BY 'dein_passwort';

        Rechte für die Konfigurationsdatenbank vergeben
        (Datenbankname je nach Installation: pmadb oder phpmyadmin)

        GRANT SELECT, INSERT, UPDATE, DELETE
        ON pmadb.* TO 'pma'@'localhost';

        Alternative:
        GRANT SELECT, INSERT, UPDATE, DELETE ON phpmyadmin.* TO 'pma'@'localhost';

        Passwort ändern (optional)
        ALTER USER 'pma'@'localhost' IDENTIFIED BY 'neues_passwort';

        Änderungen aktivieren
        FLUSH PRIVILEGES;

*Siehe Quick Reference am Ende des Dokuments mit den SQL-Statements zum Kopieren!*

*Nach der Änderung des Passworts muss dieses natürlich in der config.inc.php „controlpass“ angepasst werden!*

##### Weitere Aktionen für den Fall, dass jemand keine pmadb angelegt hat und diese später nutzen möchte

1. Unter phpMyAdmin einloggen
2. Neue Datenbank "pmadb" anlegen
3. Unter dieser Datenbank „Importieren“ auswählen
4. Unter zu importierende Datei „Durchsuchen“ anklicken
5. Folgendes Verzeichnis öffnen: WebDev/apache/htdocs/phpmyadmin/sql/create_tables.sql doppelklicken und unten auf der Seite (phpMyAdmin) den Button „importieren“ drücken.

### Anpassungen PHP (php.ini) nicht vorhanden, sondern erstellen aus php.ini-development oder -production

#### Änderungen sind nutzerabhängig. Hier meine angepassten Teile

##### Angepasst aus der kopierten php.ini-development

>       ; Maximum amount of memory a script may consume
>       ; https://php.net/memory-limit
>       memory_limit = 256M
>       max_memory_limit = 512M # neuer Parameter mit PHP 8.5.0

        ; Directory in which the loadable extensions (modules) reside.
        ; https://php.net/extension-dir
        ;extension_dir = "./"
        ; On windows:
        extension_dir = "C:/WebDev/php/ext"

        extension=curl
        extension=fileinfo
        extension=gd
        extension=intl
        extension=mbstring
        extension=exif      ; Must be after mbstring as it depends on it
        extension=mysqli
        extension=openssl
        extension=pdo_mysql

        .
        .
        .
        extension=zip

        [Date]
        ; Defines the default timezone used by the date functions
        ; https://php.net/date.timezone
        date.timezone = "Europe/Berlin"

Weitere Änderungen könnten noch für "memory_limit, upload_max_filesize, max_execution_time" sinnvoll sein. Das hängt aber von den Anforderungen ab.

### Ordner "projects"

*Dieser ist gleichzusetzen mit "htdocs" unter XAMPP. Also stehen hier die eigenen Projektordner.*

#### Apache Webserver starten oder als Dienst einrichten

- Einfacher Start erfolgt über apache/bin/httpd.exe
  - Wird ein nicht privilegierter Port (z. B. 8080) verwendet, reicht der normale Benutzerstart
  - Soll Apache auf Port 80 oder 443 laufen, muss der Start mit Administratorrechten erfolgen, da diese Ports unter Windows geschützt sind
- Einrichten als Dienst
  - httpd.exe -k install legt Apache als Windows-Dienst an
  - httpd.exe -k uninstall entfernt den Dienst wieder
    - *Die Installation oder Entfernung eines Dienstes erfordert Administratorrechte.*
  - Nach der Installation kann Apache mit httpd.exe -k start gestartet werden und läuft dann unabhängig vom Benutzerkonto.
  - Beim ersten Start muss der Netzwerkzugriff bestätigt werden.
  - Unter PowerShell muss der Befehl mit ./httpd.exe -k install ausgeführt werden, wenn man sich direkt im Apache-Verzeichnis befindet.

*Hinweis: Falls Port 80 oder 443 bereits durch andere Anwendungen belegt ist, kann Apache auf alternative Ports (z. B. 8080/8443) konfiguriert werden.*
*Dazu in der httpd.conf bzw. httpd-ssl.conf die Listen-Direktive anpassen. Der Zugriff erfolgt dann über <http://localhost:8080> bzw. <https://localhost:8443>.*

#### Genereller Test

Unter dem projects Ordner einfach eine info.php anlegen, die folgenden Inhalt hat

        <?php phpinfo; ?>

Nach dem Start des Servers einfach die URL <http://localhost/info.php> aufrufen und es sollte die Seite mit der PHP-Version und allen Informationen dazu erscheinen.

phpMyAdmin wird unter <http://localhost/phpmyadmin> aufgerufen (siehe Alias unter httpd.conf).

### Allgemeine Bemerkungen

Ich habe diese Dokumentation nach erfolgreicher Durchführung erstellt und hoffe damit alle Stolpersteine weggeräumt zu haben.

*Bei den Änderungen in der httpd.conf habe ich auf "VirtualHosts" verzichtet.*

Wer damit aber arbeiten möchte, findet alle Informationen unter

    <!-- https://httpd.apache.org/docs/current/de/vhosts/-->

*Verwendung von Zertifikaten unter dem Apache Webserver:*

Dazu gibt es weiterführende Informationen unter

    <!--https://www.ssldragon.com/de/how-to/install-ssl-certificate/apache/-->

### Release-Updates (neu) unter WebDev

- Alle Dienste und Services müssen beendet werden
- 1.2 MariaDB – Verzeichnis „data“ komplett sichern.
- De-Installation der mariaDB
- Rename „apache“ Verzeichnis
- Rename „php“ Verzeichnis
- De-Installation MariaDB
- Anlegen neue Verzeichnisse: apache, php, mariadb
- Unzip Apache-Dateien nach apache
- Unzip PHP-Dateien nach php
- Installation MariaDB nach WebDev/mariadb
- Kopieren apache-old/htdocs/phpmyadmin nach apache/htdocs
- Kopieren php-old/php-ini nach php/php.ini
- Folgende Zeilen an der Stelle einfügen:

- LoadModule xml2enc_module modules/mod_xml2enc.so

#### ICU-Bibliotheken für PHP 8.5.11 (ICU 77)

LoadFile "C:/WebDev/php/icuuc77.dll"
LoadFile "C:/WebDev/php/icuin77.dll"
LoadFile "C:/WebDev/php/icudt77.dll"
LoadFile "C:/WebDev/php/icuio77.dll"

#### Apache dll für PHP 8.5.11

LoadModule php_module "C:/WebDev/php/php8apache2_4.dll"

- Services und Dienste wieder starten

### Allgemeiner Haftungsausschluss

>Die Informationen in diesem Dokument werden in gutem Glauben und nur zu allgemeinen Informationszwecken
>bereitgestellt. Ich übernehme keine Gewähr für die Richtigkeit, Vollständigkeit oder Aktualität der in
>diesem Dokument enthaltenen Informationen!
>Dietmar Ley – 04.10.2026
>mailto: <leydietmar@gmail.com>

## Quick Reference: phpMyAdmin Control-User

    ========================================
    Quick Reference: phpMyAdmin Control-User
    ========================================

    1️⃣ Control-User anlegen
    Erstellt den Benutzer "pma" mit Passwort.
    SQL:
    CREATE USER 'pma'@'localhost' IDENTIFIED BY 'dein_passwort';

    2️⃣ Rechte vergeben
    Weist dem Benutzer Rechte auf die Konfigurationsdatenbank zu.
    (Datenbankname je nach Installation: pmadb oder phpmyadmin)
    SQL:
    GRANT SELECT, INSERT, UPDATE, DELETE ON pmadb.* TO 'pma'@'localhost';
    -- Alternative:
    -- GRANT SELECT, INSERT, UPDATE, DELETE ON phpmyadmin.* TO 'pma'@'localhost';

    3️⃣ Passwort ändern (optional)
    Ändert das Passwort des Control-Users.
    SQL:
    ALTER USER 'pma'@'localhost' IDENTIFIED BY 'neues_passwort';

    4️⃣ Änderungen aktivieren
    Lädt die Privilegien neu, damit sie sofort wirksam sind.
    SQL:
    FLUSH PRIVILEGES;

    ⚙️ Konfiguration in config.inc.php
    $cfg['Servers'][$i]['controluser'] = 'pma';
    $cfg['Servers'][$i]['controlpass'] = 'dein_passwort';
    $cfg['Servers'][$i]['pmadb'] = 'pmadb'; // oder 'phpmyadmin'

    📌 Hinweis

    - Nach Passwortänderung muss "controlpass" in der config.inc.php angepasst werden.
    - Falls die Datenbank (pmadb oder phpmyadmin) fehlt:
    - Neue Datenbank anlegen
    - Datei sql/create_tables.sql importieren
    =========================================

## Batch-Dateien

    ===========================================================
    Apache-/MariaDB-Dienste überprüfen, Stoppen und neu Starten
    ===========================================================

    ServiceFind.bat

    sc query type= service state= all | find "Apache2.4"
    sc query type= service state= all | find "MariaDB"

    StartStop.bat

    @echo off
    REM Apache und MariaDB stoppen
    echo Stoppe Apache und MariaDB...
    net stop "Apache2.4"
    net stop "MariaDB"

    REM 10 Sekunden warten
    echo Warte 10 Sekunden...
    timeout /t 10 /nobreak >nul

    REM Apache und MariaDB starten
    echo Starte Apache und MariaDB...
    net start "Apache2.4"
    net start "MariaDB"

    echo Fertig!
    pause

    Start.bat

    REM Apache und MariaDB starten
    echo Starte Apache und MariaDB...
    net start "Apache2.4"
    net start "MariaDB"

    echo Fertig!
    pause

    Stop.bat
    
    @echo off
    REM Apache und MariaDB stoppen
    echo Stoppe Apache und MariaDB...
    net stop "Apache2.4"
    net stop "MariaDB"

    echo Fertig!
    pause
