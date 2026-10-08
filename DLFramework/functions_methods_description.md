# DLFramework-Next6 Beschreibung der Funktionen / Methoden

## 📑 Inhalt

***Die hier verwendeten Emojis sind frei verfügbar über <https://emojipedia.org>!***

<!-- Muss noch erstellt werden -->

## 🤭 Aktualisierungen 04-08/2026

### **Knowledge Hub**

Vorbereitung einer KI-ähnlichen

### **abend-diagnostic**

Die abend-diagnostic-Umgebung wird per composer mit eingebunden. Dies hat auch eine Änderung des eigenen ErrorHandlers erfordert. Dort werden jetzt nur noch logStatus-Informationen ausgegeben! Fehlerinformationen nur noch über die abend-diagnostic-Umgebung. Damit gibt es an de Stelle keine Redundanzen mehr.

Die Ausgaben aus der abend-diagnostic Routine können per DumpViewer analysiert werden. Dieser ist als Python/PySide6-Anwendung realisiert.

### **Routing**

Routing ist der Prozess, eingehende HTTP‑Requests einer passenden Controller‑Methode zuzuordnen.
Der Router vergleicht die angeforderte URI und das HTTP‑Verb mit den registrierten Routen, extrahiert Parameter aus der URL, löst den Controller über den DI‑Container auf und führt anschließend die Middleware‑Pipeline sowie die Zielmethode aus.
Durch die Nutzung von Attributen (#[Route]) bleibt das Routing deklarativ, übersichtlich und flexibel.

---

### Erweiterung um Middleware

Middleware in PHP MVC kann auch als eine Art „Klebstoff“ oder „Brücke“ zwischen Anwendungen und Betriebssystemen betrachtet werden, die die Anwendungsentwicklung optimiert und die Markteinführungszeit verkürzt. Es ermöglicht die Kommunikation zwischen verschiedenen Anwendungen oder Komponenten in einem verteilten Netzwerk und kann verschiedene Arten von Middleware umfassen, wie Nachrichtenvermittler, Webanwendungsserver oder Cloudbasierte Integration Plattformen.

#### **Dependency Injection (DI)**

Dependency Injection (DI) ist ein Entwurfsmuster, bei dem Objekte ihre benötigten Abhängigkeiten nicht selbst erzeugen, sondern von außen bereitgestellt bekommen.
In diesem Framework übernimmt ein zentraler Container die Aufgabe, Instanzen zu erstellen und zu verwalten. Controller, Services und Modelle erhalten ihre Abhängigkeiten automatisch, was den Code entkoppelt, testbarer macht und die Wiederverwendbarkeit erhöht.

#### **Reflection**

Reflection ermöglicht es, zur Laufzeit Informationen über Klassen, Methoden, Parameter und Attribute auszulesen.
Das Framework nutzt Reflection, um Controller‑Methoden automatisch zu analysieren, Parameter korrekt zu befüllen und Attribute wie #[Route] oder #[Middleware] auszuwerten. Dadurch wird der Router dynamisch und konfigurationsarm: Der Code beschreibt sich selbst, und das Framework leitet daraus automatisch das Verhalten ab.

#### **Response Objects**

In einem PHP-MVC-Pattern ist ein Response-Objekt dafür zuständig, die HTTP-Antwort zu kapseln — also Statuscode, Header und Body. Es trennt die Logik (Controller/Model) von der eigentlichen Ausgabe und erleichtert Tests, Middleware und Wiederverwendung.  

#### **CSRF**

Cross‑Site Request Forgery (CSRF) ist ein Sicherheitsmechanismus, der verhindert, dass Angreifer im Namen eines eingeloggten Benutzers Aktionen ausführen.
Dazu wird jedem Formular ein eindeutiger Token hinzugefügt, der in der Session gespeichert ist.
Beim Absenden des Formulars prüft die Anwendung, ob der Token mit dem Session‑Token übereinstimmt.
Fehlt der Token oder ist er ungültig, wird der Request blockiert.
So wird verhindert, dass externe Websites oder Skripte unautorisierte POST‑Requests auslösen.

---

## ⚙️ Config.php – Übersicht

Die Datei `Config.php` dient als zentrale Konfigurationsstelle des Frameworks. Sie definiert globale Konstanten, Rollen- und Berechtigungsstrukturen sowie alle anwendungsrelevanten Einstellungen. Viele Werte werden sicher aus Umgebungsvariablen (`.env`) eingelesen.

---

### 📂 1. Systempfade und Konstanten

Diese Konstanten verhindern hartcodierte Pfade und erleichtern den Dateizugriff:

* **APPROOT** – Basisverzeichnis der Anwendung
* **URLROOT** – Basis-URL (aus `.env` oder Fallback)
* **POSTS_UPLOAD_PATH** – Upload-Pfad für Blogposts
* **DATAPATH** – Pfad zum `/data`-Verzeichnis
* **PUBLICPATH** – Pfad zum `/public`-Verzeichnis
* **STORAGE_PATH / CODE_PATH** – Pfade zu Storage- und Code-Ordnern

---

### 🛡️ 2. Rollen- und Berechtigungssystem

Bildet die Grundlage für Zugriffskontrolle (Autorisierung):

* **ROLE_TEMPLATES** – Vorlagen für wiederkehrende Rechte
* **PERMISSIONS** – Konkrete Rollen (admin, moderator, user, guest)
* **DEFAULT_ROLE** – Standardrolle für neue/nicht eingeloggte Nutzer
* **ROLE_DESCRIPTIONS** – Textliche Beschreibung der Rollen
* **ROLE_LABELS** – Anzeigenamen für die Benutzeroberfläche
* **PUBLIC_CATEGORIES** – Öffentlich sichtbare Kategorien

---

### 🚀 3. App-Konfiguration (Array-Block)

* 🌐 **app**
  * Name der Anwendung & Basis-URL
  * Basis-Pfad (via `$_SERVER` oder `getenv()`)
  * Umgebung (`production`, `development`, …)
* 🗄️ **mysql** (Vollständig aus `.env`)
  * Host, Datenbankname, Benutzer, Passwort, Charset
* ⏱️ **session**
  * Session-Timeout (Standard: 1800 Sekunden)
* 📧 **mailer** (SMTP & OAuth)
  * Benutzername, Client-ID, Client-Secret, Refresh-Token
  * Absenderadresse, Host, Port, Auth-Typ
  * Templates für Passwort-Reset-E-Mails
* 🔑 **auth**
  * Vereinfachte Struktur: Standardrolle & Rollen mit Basisrechten

---

### ⚖️ Unterschied zwischen Config.php und .env

| Merkmal        | **Config.php**                    | **.env**                                    |
| :------------- | :-------------------------------- | :------------------------------------------ |
| **Inhalt**     | Framework-Logik, Rollen, Pfade    | Sensible Daten (Passwörter, Tokens)         |
| **Sicherheit** | Wird versioniert (Teil des Codes) | **Nicht** versioniert (Umgebungsspezifisch) |
| **Format**     | PHP-Logik & Strukturen            | Einfache Key-Value-Paare                    |

> **Kurz:** `.env` enthält geheime, serverabhängige Werte, während `Config.php` die feste Logik bereitstellt.

---

## 🎮 Controllers

### **AdminController**

Der `AdminController` dient als zentrale Steuereinheit für administrative Aufgaben und kombiniert Datenbank-CRUD-Operationen mit Systemdiensten.

* **json(array $data)** – Sendet eine JSON-Antwort inklusive passendem Header und bricht die Ausführung ab.
* **checkAdmin()** – Validiert die Session-Rolle und verweigert bei fehlenden Rechten den Zugriff via JSON-Fehler.
* **updateFlag()** – Schaltet Benutzer-Statuswerte (z. B. Sperrung) um, versendet eine Info-Mail und loggt den Vorgang.
* **updateRole()** – Ändert die Benutzerrolle in der Datenbank, informiert den User per E-Mail und erstellt einen Log-Eintrag.
* **addCategory() / updateCategory() / deleteCategory()** – Standard-CRUD-Schnittstellen für die Tabellen-Verwaltung über das Category-Model.
* **updateGalleryCaptions()** – Überschreibt die gesamte JSON-Datei für Bildunterschriften eines bestimmten Galerie-Themas.
* **updateSingleCaption()** – Aktualisiert oder ergänzt gezielt eine einzelne Bildunterschrift innerhalb einer JSON-Konfiguration.
* **reassignOrphan()** – Überträgt die Eigentümerschaft von Beiträgen ohne gültigen Besitzer auf einen neuen Benutzer.

---

### **AuthController**

Der `AuthController` steuert sämtliche Authentifizierungsprozesse des Frameworks (Login, MFA, Registrierung, Passwort-Reset). Er nutzt den `AuthService`, um die Logik klar zu trennen.

#### 🏗️ Konstruktor

* Initialisiert eine Instanz von **AuthService** für alle Sicherheitsprüfungen.

#### 🔐 Login-Prozess

* **showLogin** – Zeigt das Login-Formular an.
* **login** – Verarbeitet den Login-Vorgang:
  * 📥 Liest E-Mail, Passwort und OTP aus dem Formular.
  * 🛡️ Prüft Existenz, Status (nicht gelöscht/gesperrt) und Brute-Force-Schutz (Fehlversuche).
  * 🔑 Validiert Zugangsdaten via `AuthService` (Passwort & OTP).
  * ✅ Bei Erfolg: Reset der Fehlversuche, Login via `AuthHelper::login()` und Dashboard-Redirect.
  * ❌ Bei Fehler: Erhöht Fehlversuche und gibt Fehlermeldung an die View zurück.
* **logout** – Meldet den Benutzer ab und leitet zum Login weiter.

#### 📝 Registrierung und OTP-Einrichtung

* **showRegister** – Zeigt das Registrierungsformular.
* **register** – Verarbeitet die Neuanlage:
  * 📏 Validiert Daten und Passwortlänge (**mindestens 12 Zeichen**).
  * 💾 Registriert den Benutzer über `AuthService`.
  * 📱 Generiert lokalen QR-Code für die Zwei-Faktor-Authentifizierung (OTP-Secret).
  * 🖥️ Zeigt die OTP-Setup-View mit QR-Code und Secret an.

#### ✉️ Passwort vergessen und Reset-Link

* **showForgotPassword** – Formular zum Anfordern eines Reset-Links.
* **sendResetLink** – Workflow für den Versand:
  * 🔗 Erzeugt Token via `AuthService` und verschlüsselt die User-ID (`Encryption::encryptId`).
  * 📧 Baut Link zusammen und versendet E-Mail über `EmailService::sendEmail`.
  * ℹ️ Zeigt Erfolgsmeldung an (unabhängig davon, ob die E-Mail existiert).
* **showResetForm** – Zeigt Reset-Formular (liest verschlüsselte ID/Token aus URL und entschlüsselt diese).
* **updatePassword** – Validiert Mindestlänge und aktualisiert das Passwort über `AuthService`.

#### 🔄 Passwort ändern (eingeloggt)

* **showChangePassword** – Zeigt Formular (Gäste werden zum Login umgeleitet).
* **changePassword** – Prozess-Validierung:
  * 📋 Prüft aktuelles Passwort, Übereinstimmung und Mindestlänge.
  * 💾 Update via `AuthService`; bei Erfolg `AuthHelper::logout` und Redirect zum Login.

> **Zusammenfassung:** Der `AuthController` bildet die komplette Sicherheitslogik ab, inklusive Schutz vor Brute-Force, MFA-Setup und sicherer Token-Verarbeitung durch gekapselte Services.

---

### **BaseController**

Der `BaseController` dient als abstrakte Basisklasse für alle Controller im Framework und stellt gemeinsame Grundfunktionalitäten bereit.

* **view(string $view, array $data = [])** – Zentrale Methode zum Laden von View-Dateien und zur Übergabe von Datenarrays an das Frontend.

---

## 📝 **BlogPostController**

Zentrale Steuereinheit für alle Blogfunktionen. Er verwaltet das Rendering von Markdown-Beiträgen, Zugriffsrechte, Bildverarbeitung und die Archiv-Generierung.

**Genutzte Komponenten:** `BlogPostModel`, `CategoryModel`, `UserModel`, `AccessManager`, `AuthHelper`, `Redirect`, `GithubFlavoredMarkdownConverter`.

### 🏗️ BlogPost-Konstruktor

* Initialisiert Models (`BlogPost`, `Category`).
* Erfasst Benutzerrolle und ID aus der Session für den **AccessManager**, um die Sichtbarkeit von Beiträgen zu steuern.

### 🔍 Anzeige & Filterung

* **index()** – Hauptübersicht der Blogposts:
  * 🛡️ **Rollenlogik:** Admin/Moderator sehen alles; User sehen eigene & Rollen-Beiträge; Gäste nur öffentliche Kategorien (ID >= 9).
  * 📊 Lädt Kategorien, Archivmonate und die neuesten Titel für die View `blogpost`.
* **archive()** – Monatsbasiertes Archiv:
  * 📅 Filtert Beiträge nach Monat aus der `posts_index.php`.
  * 🛡️ Berechtigungsprüfung via `AccessManager` (Öffentlich vs. Privat).
  * 📉 Sortierung der Ergebnisse absteigend nach Datum.
* **show()** – Einzeldarstellung eines Beitrags:
  * 📂 Prüft Existenz von Index-Eintrag und physischer Markdown-Datei via Slug.
  * ⚙️ **Transformation:** Ersetzt Upload-Pfade durch `URLROOT` und konvertiert Markdown zu HTML (GFM).
  * 🖥️ Übergabe von Metadaten und Inhalt an `post_show`.

### 🛠️ CRUD & Content-Management

* **getModalContent()** – Dynamischer Inhalts-Loader:
  * ⚡ Lädt via `type`-Parameter die passende View für Anzeigen, Bearbeiten, Hinzufügen oder Löschen.
* **add()** – Erstellt einen neuen Post:
  * 📸 Verarbeitet Bilder via `processUploadedImage`.
  * 💾 Speichert Header, Text und Metadaten über `BlogPostModel::create`.
  * 🔄 **Post-Action:** Generiert das Archiv neu und leitet zum Dashboard weiter.
* **update()** – Aktualisiert bestehende Beiträge:
  * 🔄 Verarbeitet optional neue Bilder und setzt Änderungs-Zeitstempel (`post_date_chg`).
  * 💾 Update via `BlogPostModel::update` mit anschließendem Archiv-Rebuild.
* **delete()** – Löscht einen Beitrag:
  * 🗑️ Entfernt den Datenbankeintrag und das zugehörige Bild (außer "noimage.jpg").

### ⚙️ Interne Dienste & Archivierung

* **processUploadedImage()** (private) – Bildverarbeitung:
  * ✂️ Schneidet Bilder mit *Intervention Image* auf **1200x800 (cover)** zu.
  * 📁 Speichert unter `/public/blogposts/` mit zeitstempelbasiertem Namen.
* **generateFullArchive()** – Öffentlicher Trigger für den Archiv-Rebuild.
* **generateFullArchiveInternal()** (private) – Erzeugt das Markdown-Archiv:
  * 🧹 Bereinigt `/data/posts/` und exportiert alle DB-Einträge als MD-Dateien.
  * 📑 Erzeugt die `posts_index.php` als schnellen PHP-Datenindex mit allen Metadaten (Autor, Rolle, Bild, Tags).

> **Zusammenfassung:** Der `BlogPostController` orchestriert das gesamte Ökosystem von der DB-Eingabe über die Bildskalierung bis hin zur performanten Markdown-basierten Dateiausgabe.

---

## 🖥️ **DashboardController**

Der `DashboardController` steuert die zentrale Benutzeroberfläche für eingeloggte Nutzer. Er bereitet Daten wie Benutzerlisten, Kategorien und Blogposts rollenbasiert auf.

### **index()** – Zentrale Dashboard-Anzeige

Diese Methode validiert den Zugriff und stellt das Datenpaket für die View bereit.

* **🛡️ Login-Prüfung** – Nicht eingeloggte Nutzer werden sofort zur Login-Seite umgeleitet.
* **📦 Daten-Initialisierung** – Lädt `UserModel`, `CategoryModel` und `BlogPostModel`.
* **👤 Rollenbasierte Logik** – Die Session-Rolle bestimmt den Sichtbarkeitsumfang:
  * **Admin & Moderator:** Vollzugriff auf alle Benutzer, Kategorien und verwaiste Posts.
  * **User:** Sichtbarkeit beschränkt auf die eigene Benutzergruppe und deren Posts.
  * **Guest:** Sieht ausschließlich das eigene Profil und eigene Beiträge.
* **🖼️ Bildergalerie (Admin/Mod)** – Automatisches Einlesen von `/storage/gallery/`:
  * Scannt Unterverzeichnisse (Themes) nach Bilddateien (`jpg`, `png`, `gif`).
  * Verknüpft Bilder mit Metadaten aus der jeweiligen `captions.json`.
* **🖥️ View-Übergabe** – Alle gesammelten Informationen (User-Daten, Gallery, Kategorien) werden im Haupt-Array an die View `dashboard` übergeben.

> **Zusammenfassung:** Das Dashboard fungiert als dynamisches Herzstück der UI, das Berechtigungen strikt trennt und Administratoren zusätzliche Werkzeuge wie die Galerie-Verwaltung bietet.

---

## ⚠️ **ErrorController**

Verantwortlich für die standardisierte Behandlung von Fehlzuständen innerhalb des Routings.

### **index()** – 404 Fehlerseite

* **📡 HTTP-Status** – Setzt den Header explizit auf **404 Not Found**.
* **🖼️ View** – Lädt die dedizierte Fehler-View `404`.

> **Hinweis:** Dieser Controller besitzt keine Geschäftslogik und dient rein der sauberen Signalisierung nicht existierender Routen oder Ressourcen.

---

## 🖼️ GalleryController

Der `GalleryController` ist für die Anzeige und Auslieferung von Bildern zuständig. Er arbeitet direkt mit dem Dateisystem und benötigt keine Datenbank-Models.

* **index()** – Zeigt die Galerieansicht für ein bestimmtes Thema:
  * 📂 Liest das Thema aus der URL (Standard: „umgebung“).
  * 📝 Scannt den Ordner nach Bilddateien (`jpg`, `jpeg`, `png`, `gif`).
  * 🏷️ Lädt zugehörige Untertitel aus der `captions.json` (falls vorhanden).
  * 🖥️ Übergabe von Bildern, Captions und Thema an die View `gallery/index`.
* **getGalleryData()** – JSON-Schnittstelle für Admin-Oberflächen:
  * 📊 Scannt `/storage/gallery/` nach allen Unterthemen.
  * 📡 Erzeugt eine flache Liste aller Bilder inklusive Metadaten als JSON-Antwort.
  * ⚙️ Optimiert für die Verwendung in Tabellen-Grids oder Admin-Dashboards.
* **getGalleryImage()** – Direkte Bildauslieferung an den Browser:
  * 🛰️ Streamt Bilder direkt aus dem Storage-Ordner (nicht öffentlich im Webroot).
  * 🛠️ Ermittelt MIME-Typ und setzt den korrekten `Content-Type`-Header.
  * ⚠️ Sendet einen **404-Status**, falls die Datei physisch nicht existiert.

---

## 📄 PagesController

Ein schlanker Controller für statische Seiten und die öffentliche Galerieansicht. Er dient als Einstiegspunkt für nicht-authentifizierte Nutzer.

* **index() / about() / contact()** – Lädt die statischen Views `home`, `about` und `contact`.
* **gallery()** – Die öffentliche (login-freie) Variante der Galerie:
  * 📂 Scannt alle verfügbaren Themenordner für die Navigation.
  * 🖼️ Sammelt Bilder und Untertitel des gewählten oder standardmäßigen Themas.
  * 📦 Stellt ein Datenpaket (Themes, Images, Captions) für die View `gallery` bereit.

---

## 🚀 ProjectController

Steuert die Darstellung von Software- und Webprojekten im Dashboard und wickelt die dynamische Bereitstellung von Inhalten für Detail-Modals ab.

* **index()** – Lädt über das Modell alle verfügbaren Datensätze via all() und rendert die Projektübersicht (geschützt durch Login-Prüfung).
* **getModalContent()** – Lädt spezifische Projektdetails dynamisch für Modal-Fenster nach:
  * **🛡️ Bereinigt den target-Parameter via basename zum Schutz vor Pfadmanipulation (Directory Traversal).
  * **🔍 Sucht das Projekt anhand seines Bezeichners (project_name) in der Datenbank. Falls kein Eintrag existiert, wird ein Fallback-Array initialisiert.
  * **⚙️ Bereitet Strukturdaten (projectTitle, projectBadge) auf und decodiert die JSON-Dateiliste (codeFiles) für die Übergabe an die Basis-View modal/projects/project_base.

---

### 💡 Zusammenfassung der Controller-Architektur

| Controller  | Fokus              | Datenquelle    | Zugriff    |
| :---------- | :----------------- | :------------- | :--------- |
| **Gallery** | Medien-Management  | Dateisystem    | Gemischt   |
| **Pages**   | Statischer Content | Views / Files  | Öffentlich |
| **Project** | Portfolio          | Internes Array | Nur Login  |

---

## 🏗️ Core

### **ACCESSMANAGER**

Der `AccessManager` ist die zentrale Sicherheitsinstanz zur Verwaltung von Rollen, Berechtigungen und Zugriffsregeln. Er kombiniert Rollenlogik mit individuellen Besitzprüfungen.

* **Konstruktion** – Initialisierung mit `role` und `uid`. Lädt Berechtigungen automatisch aus der globalen `PERMISSIONS`-Konfiguration.
* **🛡️ Rollen- und Rechteprüfung**
  * **hasRole(string role)** – Prüft auf exakte Übereinstimmung der aktuellen Rolle.
  * **hasAnyRole(array roles)** – Prüft, ob die Rolle in einer Liste erlaubter Rollen vorkommt.
  * **hasPermission(string key)** – Validiert spezifische Rechte aus der globalen Konfiguration.
* **👁️ Sichtbarkeitslogik (mayViewEntry)**
  * **Kategorie-Regel:** Beiträge mit Kategorie-ID >= 9 sind immer öffentlich sichtbar.
  * **Admin-Privileg:** Administratoren haben grundsätzlich Zugriff auf alle Inhalte.
  * **Public Categories:** Abgleich mit der `PUBLIC_CATEGORIES`-Liste.
  * **Regel-Check:** Validierung gegen `can_view_all`, `can_view_role` oder `can_view_own`.
* **✍️ Bearbeitungs- & Löschrechte**
  * **mayEditEntry / mayDeleteEntry** – Prüft globale Berechtigungen (`can_edit_all`) oder den Besitz des Beitrags (`can_edit_own`).
* **📊 Getter** – Bietet Zugriff auf die aktuelle `role` und `uid`.

---

### **CONFIG**

Stellt eine statische Schnittstelle zur zentralen Verwaltung von Einstellungen bereit. Ermöglicht den Zugriff auf Werte über einfache Schlüssel oder verschachtelte Punkt-Notation.

* **📦 Datenhaltung** – Nutzt ein statisches `settings`-Array zur globalen Datenverfügbarkeit ohne Instanziierung.
* **📥 load(string filePath)** – Lädt PHP-Konfigurationsdateien in das interne Array.
  * Prüft die Existenz der Datei vor dem `require`.
  * Erwartet ein zurückgegebenes Array von der eingebundenen Datei.
* **🔍 get(string path = null)** – Flexibler Datenabruf:
  * **Gesamt-Abruf:** Gibt ohne Parameter das komplette Array zurück.
  * **Punkt-Notation:** Navigiert durch verschachtelte Strukturen (z. B. `database.host`).
  * **Fehlertoleranz:** Gibt bei fehlenden Segmenten konsequent `null` zurück.

---

### **DATABASE**

Zentrale Datenbankschnittstelle basierend auf dem **Singleton-Muster**. Stellt eine einzige, wiederverwendbare PDO-Verbindung bereit und optimiert so die Ressourcen-Nutzung.

* **🏗️ Architektur** – Verhindert Mehrfachverbindungen durch privaten Konstruktor und statische `instance`-Verwaltung via `getInstance()`.
* **🔌 Verbindungsaufbau**
  * **Dynamik:** Bezieht Host, Name, User und Pass direkt aus der `Config`-Klasse.
  * **PHP 8.5 Support:** Erkennt die neue `Pdo\Mysql`-Klasse für korrekte Attribut-Initialisierung.
  * **Optionen:** Erzwingt `ERRMODE_EXCEPTION`, `FETCH_ASSOC` und deaktiviert emulierte Prepared Statements.
  * **Initialisierung:** Setzt den Zeichensatz standardmäßig auf `utf8mb4` via `SET NAMES`.
* **🛡️ Fehlerbehandlung**
  * **Development:** Gibt PDO-Exceptions direkt aus und stoppt das Skript zur Fehlersuche.
  * **Production:** Protokolliert Fehler im `ErrorHandler` und zeigt dem User eine neutrale Meldung.

---

### **ENCRYPTION**

Die `Encryption`-Klasse ist eine statische Utility-Klasse für kryptografische Operationen. Sie kombiniert AES-256-CBC Verschlüsselung mit einem HMAC-Integritätsschutz und einem System zur ID-Verschleierung.

* **🏗️ Architektur** – Rein statische Klasse; verhindert Instanziierung durch privaten Konstruktor. Nutzt `aes-256-cbc` und `sha256` zur Schlüsselableitung.
* **🔑 Kurz-ID Funktionen**
  * **encryptId(id)** – Erzeugt einen kurzen alphanumerischen String aus einer numerischen ID via `alphaID()`.
  * **decryptId(id)** – Wandelt Kurz-IDs zurück in die ursprüngliche Ganzzahl.
  * **decryptIdWithDash(id)** – Dekodiert IDs im Format `prefix-encodedId` unter Verwendung eines dynamisch sortierten Alphabets.
* **🔠 Zeichensatzgenerierung**
  * **getCharacters()** – Erzeugt ein individuelles Alphabet basierend auf einem Hash-Key aus der `Config`. Dies erschwert das Erraten von ID-Sequenzen erheblich.
* **🔐 AES-256-CBC Verschlüsselung**
  * **encrypt(plain)** – Verschlüsselt Daten und generiert einen HMAC. Der Rückgabewert besteht aus `HMAC + IV + Ciphertext`.
  * **decrypt(ciphertext)** – Validiert zuerst den HMAC (Schutz vor Manipulation), extrahiert den IV und entschlüsselt den Klartext.
* **🛡️ Sicherheits-Features**
  * **hashEquals()** – Zeitkonstanter String-Vergleich zur Abwehr von Timing-Angriffen.
  * **alphaID()** – Vielseitige Konvertierung zwischen Zahlen und Strings, optional mit Padding und Permutation.

---

### **ERRORHANDLER**

Zentrale Instanz zur Überwachung des Systemstatus und Schnittstelle zum externen Diagnose-Subsystem. Er fängt PHP-Fehler, Exceptions sowie fatale Shutdown-Ereignisse ab und leitet sie zur Tiefenanalyse weiter.

* **⚙️ Registrierung**
  * **register()** – Aktiviert die Framework-Hooks (set_error_handler, set_exception_handler, register_shutdown_function) für eine lückenlose Systemkontrolle.
* **🚨 Diagnose- & Abbruch-Schnittstelle**
  * **handleError()** – Wandelt reguläre PHP-Fehler direkt in eine ErrorException um, damit diese einheitlich verarbeitet werden.
  * **handleException(Throwable e)** – Erfasst nicht behandelte Ausnahmen über das externe Abend-Subsystem (GtfTrace / DumpCollector) und erzwingt einen kontrollierten System-Abbruch (Hard ABEND, Exit-Code 1).
  * **handleShutdown()** – Fängt fatale Abstürze (z. B. Syntaxfehler) kurz vor Prozessende ab und sichert den Speicherzustand über den externen Dump-Collector.
* **📝 Audit- & Status-Logging**
* **logStatus(level, message)** – Protokolliert kritische Benutzer- und Systemaktivitäten (z. B. AUDIT) mit Zeitstempel in einer zentralen Status-Logdatei (status.log).

#### 💡Zusammenfassung Sicherheits- & Fehlerlogik

| Modul        | Fokus              | Sicherheits-Mechanismus                               |
| :----------- | :----------------- | :---------------------------------------------------- |
| Encryption   | Vertraulichkeit    | AES-256-CBC + HMAC Integrität                         |
| ErrorHandler | Stabilität & Audit | Externe Diagnose-Erfassung (Abend) & Status-Audit-Log |

---

### **ROUTER**

Der `Router` ist das Herzstück der Request-Steuerung. Er ordnet eingehende URLs und HTTP-Methoden den entsprechenden Controllern zu und bereitet Pfade für verschiedene Serverumgebungen auf.

* **🛠️ Routen-Registrierung**
  * **add(method, uri, handler)** – Registriert GET- oder POST-Routen. Der Handler besteht aus einem Array mit Controller-Klasse und Methode.
* **📡 Dispatching-Prozess**
  * **Pfad-Normalisierung:** Bereinigt die URI um Projekt-Unterordner und das `/public`-Segment, um eine konsistente Routing-Basis zu schaffen.
  * **Matching:** Vergleicht den bereinigten Pfad und die HTTP-Methode mit der internen Routenliste.
  * **Ausführung:** Instanziiert bei Treffer den Controller und führt die Zielmethode dynamisch aus.
* **⚠️ Fehlerbehandlung**
  * **abort(code)** – Setzt den HTTP-Status (z. B. 404) und lädt den `ErrorController`.
  * **Fallback:** Bietet eine einfache HTML-Ausgabe, falls kein spezifischer Fehler-Controller gefunden wird.

---

### **TEMPLATES**

Eine statische Utility-Klasse zur Erzeugung dynamischer Textbausteine und HTML-E-Mails. Sie sorgt für ein konsistentes Branding durch Einbindung zentraler Konfigurationswerte.

* **🏗️ Grundprinzip** – Dient als zentrale Sammelstelle für wiederverwendbare Vorlagen, insbesondere für System-Benachrichtigungen.
* **🏢 Branding-Integration**
  * **getSiteName()** – Bezieht den Anwendungsnamen via `Config::get('app.name')`. Fallback ist "Administration".
* **📧 Passwort-Reset-Template**
  * **getPasswordResetBody(userName, resetLink)** – Generiert ein vollständiges HTML-Gerüst für Passwort-Anfragen.
  * **Sicherheit:** Schützt den Benutzernamen mittels `htmlspecialchars` gegen HTML-Injection.
  * **Inhalt:** Enthält Begrüßung, Instruktionen, einen klickbaren Button-Link sowie den vollständigen Link als Text-Alternative.
* **🚀 Einsatzbereich** – Optimiert für E-Mail-Dienste (wie `EmailService`), um einheitliche und wartbare Systemnachrichten zu garantieren.

---

### 💡 Zusammenfassung Steuerungs- & Template-Logik

| Modul         | Hauptaufgabe      | Fokus                                       |
| :------------ | :---------------- | :------------------------------------------ |
| **Router**    | Request-Routing   | URL-Normalisierung & Controller-Dispatching |
| **Templates** | Content-Erzeugung | Dynamische HTML-E-Mails & Branding          |

---

## 🛠️ Helpers

### **AuthHelper** (Session- & Statusverwaltung)

Der `AuthHelper` dient als statische Schnittstelle zur Verwaltung des Benutzerstatus. Er stellt sicher, dass Sessions nicht nur existieren, sondern auch durchgehend sicher und valide sind.

* **🛡️ Session-Sicherheit**
  * **isLoggedIn()** – Validiert den Login-Status unter Berücksichtigung von Timeouts und Sicherheits-Fingerprints.
  * **generateFingerprint()** – Erzeugt einen digitalen **SHA-256 Fingerabdruck** aus User-Agent und IP-Adresse, um Session-Hijacking effektiv zu verhindern.
  * **Session-Timeout** – Überwacht die Inaktivität basierend auf dem in der `Config` definierten Intervall (Standard: 1800s).

* **🚪 Login- & Logout-Management**
  * **login()** – Initialisiert eine sichere Session. Verwendet `session_regenerate_id(true)`, um Session-Fixierung zu unterbinden und setzt Standardrollen aus der Konfiguration.
  * **logout()** – Beendet die Sitzung restlos: Löscht das `$_SESSION`-Array, invalidiert das Session-Cookie und zerstört die Server-Session.

* **⚙️ Status-Aktualisierung**
  * **Aktivitäts-Tracking** – Aktualisiert bei jedem validen Aufruf den Zeitstempel `last_activity`, um die Session innerhalb des erlaubten Zeitfensters offen zu halten.

### **CodeHelper** (Sicherer Dateizugriff)

Der `CodeHelper` ist eine spezialisierte Utility-Klasse, um Quellcode sicher aus dem Dateisystem zu lesen und für die Darstellung in der Weboberfläche vorzubereiten.

* **🔒 Sicherheitsmechanismen**
  * **Directory Traversal Schutz** – Verifiziert mittels `realpath()`, dass angeforderte Dateien strikt innerhalb des definierten Storage-Verzeichnisses (`/storage/code`) liegen.
  * **XSS-Prävention** – Verarbeitet Dateiinhalte automatisch mit `htmlspecialchars()`, um eine sichere Ausgabe von Code im Browser zu gewährleisten.
  * **Zugriffskontrolle** – Validiert die Existenz und Lesbarkeit von Dateien, bevor ein Zugriff erfolgt, um Systemfehler zu vermeiden.

* **📂 File-Handling**
  * **getSafeCode()** – Die zentrale Methode zum sicheren Abruf von Datei-Inhalten. Sie liefert entweder den geschützten Code oder eine detaillierte, aber sichere Fehlermeldung zurück.
  * **Abstraktion der Pfade** – Kapselt die interne Verzeichnisstruktur, sodass Controller lediglich den Dateinamen kennen müssen.

### **Redirect** (Navigations-Steuerung)

Die `Redirect`-Klasse ist ein schlankes Utility, das einen konsistenten und sicheren HTTP-Redirect innerhalb der Applikation gewährleistet.

* **🚀 Routing & Navigation**
  * **to()** – Führt eine sofortige Weiterleitung zu einem definierten Pfad aus. Sie bricht die weitere Skriptausführung mittels `exit` sofort ab, um unnötige Serverlast zu vermeiden.
  * **Absolute URL-Auflösung** – Kombiniert den Zielpfad automatisch mit dem `app.base_path` aus der Konfiguration, um fehlerhafte Relative-Link-Sprünge zu verhindern.

* **🛡️ Header-Management**
  * **Header-Präventions-Check** – Prüft mittels `headers_sent()`, ob bereits eine Ausgabe an den Browser erfolgt ist, um PHP-Warnungen zu unterdrücken.
  * **Normalisierung** – Bereinigt Pfadangaben automatisch von führenden oder abschließenden Slashes (`/`), was eine robuste URL-Generierung garantiert.

### **TextHelper** (String-Manipulation & SEO)

Der `TextHelper` bietet spezialisierte Methoden zur Transformation von Texten, primär für die Erzeugung von suchmaschinenfreundlichen URLs und die Bereinigung von Benutzereingaben.

* **🔗 URL-Optimierung**
  * **slugify()** – Verwandelt beliebige Zeichenketten in saubere, URL-konforme "Slugs" (z. B. für Blog-Beiträge oder Profilseiten).
  * **Umlaut-Konvertierung** – Ersetzt deutsche Sonderzeichen (`ä, ö, ü, ß`) intelligent durch ihre ASCII-Pendants (`ae, oe, ue, ss`), um die Lesbarkeit in allen Browsern zu garantieren.
  * **Regex-Bereinigung** – Entfernt Sonderzeichen und transformiert Leerzeichen sowie Mehrfach-Bindestriche in einfache Trennstriche (`-`).

* **🧹 Normalisierung**
  * **Lowercase-Transformation** – Erzeugt einheitliche Kleinschreibung für konsistente URL-Strukturen.
  * **Trim-Logic** – Entfernt führende und abschließende Bindestriche automatisch, um saubere Endpunkte zu liefern.

## 🗄️ Models

### **BaseModel** (Abstrakte Basisklasse)

Das `BaseModel` dient als fundamentales Fundament für alle spezifischen Models der Anwendung. Es stellt die zentrale Datenbankverbindung bereit und definiert den strukturellen Rahmen für den Datenzugriff.

* **🏗️ Architektur & Design**
  * **Abstrakte Struktur** – Verhindert die direkte Instanziierung und erzwingt eine saubere Vererbungshierarchie für spezialisierte Models (z. B. `UserModel`).
  * **PDO-Integration** – Hält die aktive Datenbankinstanz in der Property `$db` bereit, sodass Kindklassen sofortigen Zugriff auf die Query-Methoden haben.
  * **Table-Mapping** – Definiert das geschützte Attribut `$table`, welches in den Subklassen zur dynamischen Identifizierung der Ziel-Tabelle genutzt wird.

* **🔌 Ressourcen-Management**
  * **Singleton-Anbindung** – Bezieht die Datenbankverbindung über `Database::getInstance()`, was eine effiziente Nutzung der Ressourcen durch Wiederverwendung bestehender Verbindungen garantiert.

### **BlogPostModel** (Content-Management)

Das `BlogPostModel` erweitert das `BaseModel` und bildet das Herzstück der Inhaltsverwaltung. Es implementiert komplexe Abfragen für zeitgesteuerte Inhalte, Benutzer-Berechtigungen und Datenintegrität.

* **🧩 Funktionalität & Traits**
  * **CrudTrait** – Nutzt das zentrale Trait für standardisierte Erstellungs-, Lese-, Aktualisierungs- und Löschvorgänge, um Code-Duplikate zu vermeiden.
  * **Beziehungs-Management** – Führt komplexe `LEFT JOIN` Operationen über die Tabellen `users` (Autoren & Editoren) und `categories` aus, um vollständige Datensätze zu liefern.
  * **Integritäts-Prüfung** – Beinhaltet spezialisierte Methoden wie `getOrphanedPosts()`, um Beiträge ohne gültigen Autor zu identifizieren.

* **📅 Zeit- & Archiv-Logik**
  * **Dynamische Zeitfenster** – Filtert über `getPostsByCategory()` automatisch Inhalte der letzten zwei Monate für die Hauptanzeige.
  * **Archiv-Sidebar** – `getArchiveMonths()` aggregiert alle älteren Beiträge in monatlichen Gruppierungen für eine effiziente Navigation.
  * **Sortierung** – Alle Inhaltsabfragen sind standardmäßig auf eine absteigende chronologische Sortierung (`post_date DESC`) optimiert.

* **🔐 Zugriffskontrolle & Dashboards**
  * **getPostsByAccess()** – Implementiert eine hybride Berechtigungslogik: Zeigt Beiträge basierend auf einer Liste erlaubter User-IDs oder vordefinierten öffentlichen Kategorien (ID >= 9).
  * **getManagedPosts()** – Spezialisierte Abfrage für das Admin-Dashboard, die nur Beiträge mit existierenden Autoren und deren jeweiligen Bearbeitern (`editor_name`) zurückgibt.
  * **getPostWithDetails()** – Liefert eine detaillierte Einzelansicht inklusive der Historie (wer hat den Beitrag erstellt, wer hat ihn zuletzt geändert).

* **📊 Daten-Exporte & Utilities**
  * **getAllPostsForExport()** – Bereitet den gesamten Datenbestand inklusive Rollen und Kategorienamen für externe Archiv-Systeme auf.
  * **getLatestTitles()** – Eine leichtgewichtige Methode, um performant nur die aktuellsten Schlagzeilen abzurufen.

### **CategoryModel** (Struktur & Kategorisierung)

Das `CategoryModel` dient der organisatorischen Klassifizierung von Inhalten. Es ist ein Paradebeispiel für die **DRY-Architektur** (Don't Repeat Yourself) des Frameworks, da es fast die gesamte Logik aus einem zentralen Trait bezieht.

* **🏗️ Kernkonfiguration**
  * **Tabellen-Mapping** – Verknüpft das Model explizit mit der Datenbanktabelle `categories`.
  * **Primary Key Definition** – Überschreibt den Standardwert, um das spezifische Feld `category_id` als Primärschlüssel für alle Datenbankoperationen zu nutzen.

* **⚡ Funktionalität & Abstraktion**
  * **CrudTrait-Integration** – Erbt automatisch alle Standardmethoden für *Create, Read, Update* und *Delete*, ohne dass redundanter Code im Model geschrieben werden muss.
  * **BaseModel-Anbindung** – Profitiert von der zentralen PDO-Instanz für performante Abfragen und konsistentes Verbindungsmanagement.

### 🗄️ ProjectModel

Verantwortlich für den Datenbankzugriff und die Datenhaltung der Projektentitäten auf der Tabelle projects.

* **🏗️ Kernkonfiguration**
  * **Tabellen-Mapping** – Fest verknüpft mit der Tabelle projects unter Verwendung von project_id als Primärschlüssel.
  * **Abhängigkeiten** – Löst die benötigte PDO-Instanz automatisch zum Konstruktionszeitpunkt über den Framework-Container auf.
* **⚡ Funktionalität & Datenzugriff**
  * **CrudTrait-Integration** – Erbt über den Trait alle Standard-Datenbankoperationen wie das Auslesen des Gesamtdatenbestands via all().
  * **findBy(column, value)** – Erlaubt das gezielte Abfragen einzelner Datensätze über eine Spalte.
* **🛡️ Whitelist-Schutz** – Prüft Spaltennamen (project_id, project_name, title, etc.) vor der SQL-Ausführung strikt gegen eine Whitelist, um SQL-Injections durch dynamische Spaltenbezeichner effektiv zu verhindern.

### **UserModel** (Benutzerverwaltung & Identität)

Das `UserModel` verwaltet alle benutzerbezogenen Daten. Es kombiniert standardisierte CRUD-Operationen mit spezifischen Sicherheitsabfragen für Authentifizierungs- und Autorisierungsprozesse.

* **👤 Identität & Suche**
  * **findByEmail()** – Ermöglicht den schnellen Abruf von Benutzerdatensätzen via E-Mail, essenziell für den Login-Prozess und die [Passwort-Verifizierung](https://www.php.net).
  * **findByRole()** – Filtert aktive (nicht gelöschte) Benutzer nach ihrer Berechtigungsstufe (z. B. 'Admin', 'User') für die Rechteverwaltung in der Applikation.
  * **Alphabetische Sortierung** – Liefert Listenansichten standardmäßig nach Benutzernamen sortiert zurück, um die Übersichtlichkeit im Backend zu erhöhen.

* **🔑 Sicherheits-Features**
  * **findByResetToken()** – Validiert kryptografische Reset-Tokens. Prüft dabei nicht nur den Hash, sondern stellt über `reset_expires_at > NOW()` sicher, dass das Token zeitlich noch gültig ist.
  * **Status-Filterung** – Berücksichtigt bei Abfragen automatisch Flags wie `deleted`, um die Datenintegrität und Sicherheit der aktiven User-Basis zu wahren.

* **⚡ Funktionalität**
  * **CrudTrait-Integration** – Erbt alle Basis-Methoden zur Manipulation von Benutzerdaten (`create`, `update`, `delete`, `find`).
  * **Dynamisches Tabellen-Mapping** – Ist fest mit der Tabelle `users` verknüpft und nutzt die zentrale Datenbank-Instanz des `BaseModel`.

## 🛣️ Routing-System

Die Datei `web.php` dient nun ausschließlich als **Loader** für alle Controller‑basierten Routen. Statt einer zentralen Definition enthält sie nur noch eine einzige Zeile:

```php
$router->loadAttributesFromDirectory(__DIR__ . '/../Controllers');

// --- LOGIN ---
#[Route('GET', '/login')]
public function showLogin(): void
{
    $this->view('auth/login', ['title' => 'Login']);
}

#[Route('POST', '/login')]
public function login(): void
{
    // Login-Handling
}

```

* **🌍 Öffentlicher Bereich (Gäste)**
  * **Core-Seiten** – Beinhaltet die Startseite, Kontaktformular, „About“-Seite und die Projekt‑Übersicht.  
    Alle Routen werden über `GET`‑Attribute direkt im jeweiligen Controller definiert.
  * **Content-Anzeige** – Bietet lesenden Zugriff auf Blog‑Beiträge (`/blogpost/{slug}`), Kategorien, Projekte und die Bildergalerie.
  * **Authentifizierung** – Steuert Login, Registrierung sowie den kompletten **Passwort‑Reset‑Workflow** (E-Mail‑Versand, Token‑Validierung, Reset‑Formular).  
    Die entsprechenden `GET`/`POST`‑Routen stehen unmittelbar an den Auth‑Methoden.

* **🔒 Geschützter Bereich (Dashboard & Auth)**
  * **User-Zentrale** – Verwaltung des eigenen Accounts und Zugriff auf das Dashboard nach erfolgreichem Login.  
    Diese Routen sind mit `#[Middleware('auth')]` geschützt.
  * **Sicherheits-Funktionen** – Routen für den sicheren Logout, die Änderung des Passworts sowie die erneute E-Mail‑Verifizierung.  
    Auch hier erfolgt die Absicherung über Middleware‑Attribute direkt an der Methode.

* **🛠️ Administration & API-Endpunkte**
  * **Benutzer- & Rollenmanagement** – AJAX‑Schnittstellen (`POST`) zur schnellen Aktualisierung von User‑Flags, Rollen und Berechtigungen.  
    Typischerweise geschützt durch `#[Middleware('auth')]` und `#[Middleware('role:admin')]`.
  * **Kategorie-Verwaltung** – Vollständige API für die dynamische Pflege (Add/Update/Delete) von Blog‑Kategorien über `POST`, `PUT` und `DELETE`‑Attribute.
  * **Content-Operations** – Spezialisierte Endpunkte für das Handling von „verwaisten“ Blogposts (Orphans), Markdown‑Exports und die Modal‑Inhaltsbereitstellung.
  * **Galerie-Steuerung** – Proxy‑Routen für sichere Bildauslieferung sowie API‑Endpunkte zur Verwaltung von Bildbeschreibungen (Captions).

## 🎨 Frontend-Architektur (Views)

Das Framework nutzt ein modulares Layout-System. Die Trennung in Header, Navigation und Footer ermöglicht eine konsistente Benutzeroberfläche, während das Asset-Management dynamisch auf die jeweilige Route reagiert.

### **Header** (Asset-Management & HTML-Head)

Die `header.php` fungiert als zentraler Controller für das Frontend-Setup. Sie steuert das Laden von CSS-Ressourcen und bereitet die Umgebung für Framework-interne JavaScript-Logiken vor.

* **🧩 Dynamisches Asset-Loading**
  * **Globales CSS** – Lädt Basiskomponenten wie Variablen, Fonts, Layout-Raster und Modalsysteme standardmäßig auf jeder Seite.
  * **Seitenspezifisches CSS** – Identifiziert über die URI (`$_SERVER['REQUEST_URI']`) die aktuelle Seite und lädt nur die benötigten Stylesheets (z. B. `dashboard.css` oder `tabulator.css`).
  * **Vendor-Integration** – Bindet externe Bibliotheken wie **Bootstrap Icons**, **FontAwesome** und **Tabulator** kontrolliert ein.

* **🛡️ Kontext-Erkennung**
  * **Auth-Page-Detector** – Erkennt automatisch, ob sich der Nutzer im Authentifizierungs-Flow befindet (Login, Register, Passwort-Reset), und setzt eine spezielle Body-Klasse (`auth-page`) für angepasste Layouts.
  * **URI-Normalisierung** – Bereinigt den `APP_BASE_PATH`, um auch in Unterverzeichnissen eine korrekte Ressourcen-Adressierung zu garantieren.

* **📱 Meta- & SEO-Konfiguration**
  * **Responsive Design** – Setzt Viewport-Definitionen und unterstützt das `color-scheme` (Light/Dark Mode).
  * **Dynamic Title** – Bezieht den Projektnamen direkt aus der `Config`-Klasse.

### **Navigation** (Dynamisches Menü-System)

Die `navigation.php` ist das Herzstück der Benutzerführung. Sie berechnet in Echtzeit, welche Menüpunkte basierend auf dem Authentifizierungsstatus des Nutzers angezeigt werden.

* **🧠 Intelligente Filter-Logik**
  * **Status-Awareness** – Unterscheidet strikt zwischen Gästen und authentifizierten Benutzern. Während Gäste "Login" und "Registrieren" sehen, werden diese Punkte für eingeloggte User automatisch durch "Dashboard" und "Profil-Optionen" ersetzt.
  * **Zentrales Mapping** – Verwendet ein strukturiertes `$navItems`-Array, was spätere Erweiterungen oder Umbenennungen von Routen an einer zentralen Stelle ermöglicht.

* **🎨 UI & Styling-Hooks**
  * **Kontextuelles Styling** – Identifiziert Account-Aktionen (wie Logout oder Passwortänderung) und weist ihnen die CSS-Klasse `.nav-account` zu, um sie optisch von regulären Inhaltsseiten abzuheben.
  * **Data-Attributes** – Versieht Links mit `data-page`-Attributen, was eine einfache Ansteuerung und Hervorhebung des aktiven Menüpunkts via JavaScript ermöglicht.

* **🌓 Interaktive Features**
  * **Theme-Toggle** – Beinhaltet die Steuerung für den **Dark-Mode-Wechsel**, der global über alle Views hinweg das Farbschema (`light` / `dark`) umschaltet.
  * **Base-URL Integration** – Garantiert durch die Nutzung der `BASE_URL`-Konstante eine konsistente Verlinkung, unabhängig davon, in welchem Unterverzeichnis die Applikation betrieben wird.

### **Footer** (Asset-Injektion & Modal-Container)

Der `footer.php` schließt das HTML-Dokument ab und dient als zentraler Ladepunkt für JavaScript-Ressourcen. Zudem beherbergt er die globalen Modal-Strukturen für rechtliche Inhalte, um diese am Ende des DOMs (Document Object Model) bereitzuhalten.

* **⚖️ Rechtliches & Modale Strukturen**
  * **Integrierte Rechtstexte** – Enthält die Overlay-Container für Impressum und Datenschutz, die via PHP-Include aus `Views/modal/legal/` geladen werden.
  * **Modal-Trigger-System** – Nutzt `data-modal-target`, um die Overlays ohne Neuladen der Seite über das zentrale `modal.js` anzusteuern.
  * **Footer-Branding** – Konsistente Darstellung des Logos und der Copyright-Informationen für das Framework 3.1.

* **⚙️ JavaScript Asset-Management**
  * **Optimiertes Laden** – Alle Skripte werden mit dem `defer`-Attribut eingebunden, um das Rendering der Seite nicht zu blockieren und die Performance zu steigern.
  * **Vendor-Libraries** – Einbindung externer Abhängigkeiten wie [Tabulator](https://tabulator.info) (Tabellen-Engine), [CookieConsent](https://www.osano.com) und Hilfsbibliotheken wie `he.js` (HTML-Encoding).
  * **Custom UI-Logic** – Kapselung der App-Logik in spezialisierte Module:
    * `darkModeToggle.js` – Steuert das visuelle Farbschema.
    * `blogModal.js` / `projectModal.js` – Verarbeiten die dynamischen Inhalte der Blog- und Projekt-Detailansichten.
  * **Daten-Tabellen** – Initialisierung der interaktiven Grid-Systeme (`userTable.js`, `categoryTable.js`, etc.) zur Verwaltung der Framework-Daten.

* **🏗️ DOM-Abschluss**
  * Garantiert den sauberen Abschluss der `<body>`- und `<html>`-Tags nach der Injektion aller notwendigen Skripte.

### **Modal-Basis-Templates** (Dynamische Formularsteuerung)

Die Modal-Basis-Views (z. B. für Blogposts oder Projekte) bilden ein intelligentes Templating-System. Sie passen sich dynamisch dem Kontext an, um redundanten Code für Anzeige-, Erstellungs- und Bearbeitungsmasken zu vermeiden.

* **reaktive Status-Steuerung**
  * **Dynamic States** – Nutzt die Flags `$readonly` und `$required`, um Formularfelder je nach Aktion (z. B. "Löschen" vs. "Bearbeiten") automatisch zu sperren oder als Pflichtfelder zu markieren.
  * **Helper-Abstraktion** – Verwendet interne Funktionen wie `readonlyAttr()` und `requiredAttr()`, um sauberes und valides HTML-Attribut-Handling zu garantieren.
  * **XSS-Schutz** – Konsequente Anwendung von `htmlspecialchars()` bei allen Value-Ausgaben zur Absicherung gegen Script-Injektionen.

* **🖼️ Intelligentes Medien-Handling**
  * **Kontextueller Bild-Upload** – Unterscheidet im Schreib-Modus zwischen Neu-Upload und dem Ersetzen bestehender Bilder.
  * **Vorschau-Logik** – Zeigt im Lese-Modus das aktuelle Beitragsbild an, während im Editier-Modus eine dynamische Vorschau zur Kontrolle bereitgestellt wird.
  * **Fallback-Management** – Erkennt Platzhalter wie `noimage.jpg` und passt die Benutzeroberfläche (z. B. durch Ausblenden leerer Bildcontainer) automatisch an.

* **🏷️ Datenbindung & Logik**
  * **Kategorie-Mapping** – Schaltet zwischen einer statischen Textanzeige (Readonly) und einer dynamischen `<select>`-Box um, die ihre Daten direkt aus dem `CategoryModel` bezieht.
  * **Value-Persistenz** – Füllt Formularfelder automatisch mit bestehenden Datenbankwerten (`$values`), falls diese vorhanden sind.

## 🛠️ Services

### **AuthService** (Authentifizierung & Sicherheit)

Der `AuthService` bildet das Rückgrat der Anwendungssicherheit. Er kapselt die Logik für Logins, MFA-Validierung und Brute-Force-Prüfungen.

* **🔐 Identität & Verifizierung**
  * **getUserByEmail() / verifyCredentials()** – Ruft Benutzerdaten ab und verifiziert Passwörter mittels `password_verify()`.
  * **isAccountLocked()** – Prüft den aktuellen Sperrstatus eines Kontos zum Schutz vor Brute-Force-Angriffen.
  * **handleFailedLogin() / resetLoginAttempts()** – Verwalten Fehlversuche; setzt bei Erreichen von 5 Versuchen eine temporäre **Sperre von 15 Minuten**.

* **📱 Zwei-Faktor-Authentifizierung (2FA)**
  * **registerUser()** – Erstellt neue Benutzerkonten inklusive Initialisierung eines individuellen OTP-Secrets.
  * **getLocalQRCode()** – Generiert einen Base64-kodierten Inline-SVG-QR-Code für Authenticator-Apps.
  * **verifyOTP()** – Validiert 6-stellige Einmalcodes mit einem Toleranzfenster von ±30 Sekunden.
  * **generateOTPSecret() / calculateTOTP()** – Interne Hilfsmethoden für Base32-Secrets und zeitbasierte Passwort-Berechnung.

* **🔑 Passwort-Verwaltung**
  * **createPasswordResetToken()** – Erzeugt kryptografisch sichere SHA-256 Reset-Token mit einer Gültigkeit von **60 Minuten**.
  * **resetPasswordWithToken()** – Validiert Token und setzt Passwort sowie Login-Sperren zurück.
  * **updateUserPassword()** – Ermöglicht Passwortänderungen für aktive User nach Verifizierung des Alt-Passworts.

---

### **EmailService** (Kommunikation & SMTP-Relay)

Der `EmailService` stellt die zentrale Schnittstelle für den E-Mail-Versand dar. Er abstrahiert die Komplexität der **OAuth2-Authentifizierung** und nutzt die [PHPMailer-Bibliothek](https://github.com), um eine sichere Zustellung über externe Provider zu garantieren.

* **✉️ Versand-Engine & Sicherheit**
  * **sendEmail()** – Die universelle Methode für den Versand; unterstützt HTML-Inhalte, BCC-Optionen und individuelle Absender-Konfigurationen.
  * **XOAUTH2 Authentifizierung** – Nutzt moderne Google OAuth2-Tokens anstelle unsicherer Passwörter zur Autorisierung am SMTP-Server.
  * **Zentrale Fehlerbehandlung** – Protokolliert SMTP-Transaktionen und Übertragungsfehler über den [ErrorHandler](Link-zu-deinem-ErrorHandler) für eine präzise Diagnose.

* **⚙️ Konfiguration & Protokolle**
  * **SMTP via TLS** – Standardmäßige Verschlüsselung der Kommunikation zur Sicherstellung der Datenintegrität während des Transports.
  * **Config-Integration** – Dynamische Auflösung von Mail-Parametern (Host, Port, Credentials) über die zentrale `Config`-Klasse.
  * **Smart Reply-Handling** – Setzt bei Kontaktanfragen automatisch die Besucher-Adresse als `Reply-To`, um direkte Antworten zu ermöglichen.

* **📋 E-Mail-Typen & Templates**
  * **PASSWORD_RESET** – Generiert in Zusammenarbeit mit der `Templates`-Klasse personalisierte Recovery-Mails inklusive kryptografischer Links.
  * **CONTACT & USER_STATUS** – Vordefinierte Workflows für System-Benachrichtigungen und die Verarbeitung von Kontaktformular-Daten.
  * **Multi-Format Support** – Erzeugt parallel zur HTML-Fassung eine `AltBody`-Variante (Plain Text) für maximale Kompatibilität mit allen Mail-Clients.

## 🧬 Traits

### **CrudTrait**

Das `CrudTrait` stellt eine wiederverwendbare Schnittstelle für standardisierte Datenbankoperationen bereit und sorgt für DRY-konformen (*Don't Repeat Yourself*) Code in den Models.

* **🔍 Abfrage-Methoden**
  * **find(int $id)** – Ruft einen spezifischen Datensatz anhand des Primärschlüssels ab.
  * **all()** – Gibt sämtliche Datensätze der verknüpften Tabelle als Array zurück.
  * **getPrimaryKey()** – Interne Hilfsmethode zur Ermittlung des Primärschlüssel-Feldes (Standard: `id`).
* **💾 Schreib-Operationen**
  * **create(array $data)** – Erzeugt neue Einträge durch dynamisches Mapping von Spalten und Werten.
  * **update(int $id, array $data)** – Aktualisiert bestehende Werte eines Datensatzes basierend auf der ID.
  * **delete(int $id)** – Entfernt einen Datensatz dauerhaft aus der Tabelle.
* **🛡️ Sicherheit** – Nutzt konsequent **Prepared Statements** via PDO zum Schutz gegen SQL-Injection.

---

### 💡 Zusammenfassung Service- & Trait-Logik

| Komponente      | Fokus             | Sicherheits-Feature             |
| :-------------- | :---------------- | :------------------------------ |
| **AuthService** | Zugangskontrolle  | 2FA (TOTP) & Brute-Force-Schutz |
| **CrudTrait**   | Daten-Abstraktion | SQL-Injection Schutz via PDO    |

---

## 🎨 Assets & Styling

### **variables.css** (Zentrale Design-Engine)

Die `variables.css` bildet das visuelle Fundament des Frameworks. Sie nutzt moderne CSS-Features wie native **Design-Tokens** und die neue `light-dark()` Funktion, um ein konsistentes und hochperformantes Theme-Management zu ermöglichen.

* **🌓 Modernes Theme-Management**
  * **Native Color-Scheme Support** – Nutzt `color-scheme: light dark`, um Browser-Elemente (Scrollbars, Formulare) automatisch an den User-Modus anzupassen.
  * **light-dark() Integration** – Definiert Farben in einer einzigen Variable, die je nach Modus automatisch umschaltet, ohne dass redundante Media-Queries oder CSS-Klassen geschrieben werden müssen.
  * **JS-Runtime Toggle** – Unterstützt die explizite Steuerung über das Attribut `data-theme`, um Benutzereinstellungen (LocalStorage) dauerhaft zu speichern.

* **🎨 Design-Tokens & Systematik**
  * **Farb-Abstraktion** – Trennt funktionale Farben (Hintergrund, Text, Akzente) von festen Farbwerten, was ein schnelles Re-Branding des gesamten Frameworks ermöglicht.
  * **Komponenten-Styles** – Hält spezifische Variablen für Modale, Formulare und Tabellen-Statuswerte bereit, um ein einheitliches Look-and-Feel über alle Module hinweg zu garantieren.
  * **Typografie & Spacing** – Zentralisiert globale Werte wie `--font-main` (Inter/System-Fallback) und `--radius` für eine konsistente Geometrie der UI-Elemente.

* **📊 Status-Visualisierung**
  * **Semantische Farben** – Definiert dedizierte Farbräume für Benutzerrollen (Admin, User) und Statuszustände (Banned, Active), die direkt in den **Tabulator-Tabellen** und Dashboards verwendet werden.

## 🌐 Frontend- & UI-Architektur (JavaScript)

Die clientseitige Interaktion im Dashboard folgt strikten Mustern, um den Wartungsaufwand minimal zu halten. Komplexe Oberflächen wie die Datenbank-Maintenance oder Detail-Modals sind über standardisierte Blueprints gelöst.

### 🗂️ Zentrales Tabulator-Pattern (DB-Maintenance)

Die gesamte Tabellen- und Stammdatenpflege wird global über Tabulator Data Tables abgebildet. Statt jede Tabelle einzeln zu dokumentieren, folgt die Implementierung einem einheitlichen AJAX-Schema:

* Datenbezug: Tabulator fragt die Daten asynchron über eine definierte API-Route des Frameworks ab.
* In-Line-Editing: Änderungen in den Zellen triggern via Callback direkt ein Request an den Controller, der die Validierung und das DB-Update übernimmt.

### 🎭 Dynamisches Modal-Loading-Pattern

Modale Fenster (z. B. für Projektdetails oder die Rechteverwaltung) werden nicht statisch im HTML gehalten, sondern bedarfsorientiert („lazy“) per JavaScript nachgeladen:

1. Trigger: Ein Klick auf ein UI-Element löst den globalen Event-Listener aus und übergibt einen Bezeichner (target).
2. Fetch: JavaScript sendet einen AJAX-Request an die zuständige Controller-Route (z. B. /project/getModalContent).
3. Injektion: Der Controller rendert die Teil-View serverseitig. Die JS-Routine injiziert dieses HTML in den modalen Container des Dashboards und öffnet es.

### **userTable.js** (Interaktives Daten-Management)

Die `userTable.js` steuert die administrative Benutzerverwaltung im Dashboard. Sie nutzt die [Tabulator-Engine](https://tabulator.info), um komplexe Datensätze performant darzustellen und Änderungen in Echtzeit über die Framework-API zu synchronisieren.

* **📊 Dynamisches Grid-System**
  * **Responsive Layout** – Verwendet den `collapse`-Modus, um auch auf mobilen Endgeräten alle Benutzerdaten (E-Mail, Login-Versuche, Status) übersichtlich darzustellen.
  * **Echtzeit-Editierung** – Ermöglicht Administratoren das Ändern von Benutzerrollen direkt in der Zelle (`editor: "list"`), wobei die Änderungen sofort via API validiert und gespeichert werden.
  * **Visuelles Feedback** – Ein spezialisierter `rowFormatter` weist Zeilen dynamisch CSS-Klassen zu (z. B. `.is-me`, `.is-admin`, `.is-banned`), um den Status eines Nutzers auf einen Blick erkennbar zu machen.

* **🔌 API-Integration & AJAX**
  * **apiRequest()** – Eine robuste, asynchrone Helper-Funktion für `fetch`-Requests, die CSRF-konforme JSON-Daten an die Admin-Controller sendet und Fehlerzustände abfängt.
  * **Toggle-Logik** – Implementiert schnelles Umschalten von Status-Flags (Bann, Löschmarkierung) per Mausklick, inklusive sofortiger UI-Aktualisierung durch `row.reformat()`.
  * **State-Management** – Synchronisiert den lokalen Tabellen-Status mit der Datenbank, ohne die Seite neu laden zu müssen.

* **🛡️ Berechtigungssteuerung (Frontend)**
  * **Rollenbasierte UI** – Schaltet Editier-Funktionen und Klick-Events basierend auf den in `DashboardAppData` hinterlegten Berechtigungen (`isAdmin`, `isModOrAdmin`) aktiv oder inaktiv.
  * **Self-Protection** – Erkennt den aktuell eingeloggten User (`currentUserId`), um versehentliche Selbst-Sperrungen oder Rollenänderungen visuell hervorzuheben.

* **📐 Performance & UX**
  * **ResizeObserver** – Überwacht Größenänderungen des Containers und triggert automatisch ein `table.redraw()`, um Layout-Fehler bei responsiven Umbrüchen zu verhindern.
  * **Local Pagination** – Verbessert die Übersichtlichkeit durch clientseitige Paginierung der Benutzerliste.

### **blogPostTable.js** (Content-Administration & ACL)

Die `blogPostTable.js` ist das zentrale Steuerelement für die Inhaltsverwaltung. Sie implementiert eine detaillierte **Access Control List (ACL)** direkt im Frontend, um sicherzustellen, dass Nutzer nur Aktionen ausführen können, für die sie autorisiert sind.

* **🔐 Rollenbasierte Interaktion (ACL)**
  * **roleAllowed()** – Eine Kernfunktion, die den aktuellen Nutzerstatus (Admin/Moderator) gegen die Eigentümerschaft des Datensatzes (`user_id`) prüft.
  * **Dynamische Icon-Formatter** – Generiert Aktions-Icons (Auge, Stift, Müll), die bei fehlender Berechtigung automatisch deaktiviert werden (`text-disabled`), die Interaktion unterbinden und einen erklärenden Tooltip anzeigen.
  * **Owner-Highlighting** – Der `rowFormatter` markiert eigene Beiträge farblich (via CSS-Klasse `.post-user-active`), um sie in einer Liste von Fremdbeiträgen sofort hervorzuheben.

* **🛠️ Dynamische Modal-Anbindung**
  * **openDynamicPostModal()** – Diese zentrale Brücke zwischen Tabelle und Controller öffnet je nach Aktion (`v`iew, `e`dit, `d`elete, `a`dd) das entsprechende Fenster und übergibt die notwendige `post_id`.
  * **Header-Aktionen** – Das "Plus"-Icon in der Tabellen-Header-Leiste ermöglicht das schnelle Erstellen neuer Beiträge direkt aus der Grid-Ansicht heraus.

* **📱 Intelligente Responsivität**
  * **Priorisiertes Einklappen** – Nutzt ein numerisches `responsive`-System (0 bis 20), um weniger kritische Informationen wie "Bearbeiter" oder "Änderungsdatum" sofort in das Untermenü zu verschieben, während Titel und Aktionen immer sichtbar bleiben.
  * **Placeholder-Management** – Bietet eine benutzerfreundliche Anzeige ("Keine Beiträge vorhanden"), falls die Datenbankabfrage leer zurückkehrt, inklusive Handlungsaufforderung.

* **⚙️ UX-Features**
  * **Plaintext-Vorschau** – Nutzt spezielle Formatter, um lange Beitragstexte sauber in der Tabellenansicht darzustellen.
  * **Asynchrone Datenquelle** – Bezieht die Inhalte direkt aus dem globalen `window.DashboardAppData`-Objekt, was die Initialisierungsgeschwindigkeit der Seite erhöht.

## 🚀 Core Engine

### **index.php** (Der Front-Controller)

Die `index.php` im `/public`-Ordner ist der einzige offizielle Einstiegspunkt (Entry Point) der Applikation. Sie orchestriert das Bootstrapping, die Sicherheitskonfiguration und das Routing für jeden eingehenden Request.

* **🛠️ Bootstrapping & Umgebung**
  * **Vendor Autoloading** – Initialisiert Composer zur automatischen Auflösung aller Abhängigkeiten und Namespaces.
  * **Dotenv-Integration** – Lädt sensible Umgebungsvariablen (wie DB-Credentials oder API-Keys) sicher über eine `.env`-Datei.
  * **Globale Konstanten** – Definiert zentrale Parameter wie `BASE_URL` und den `DEBUG`-Modus, um das Verhalten des Frameworks global zu steuern.

* **🔒 Session- & Fehlersicherheit**
  * **Gehärtete Sessions** – Startet Sitzungen mit modernen Sicherheitsparametern (`HttpOnly`, `Secure`-Flags und `SameSite=Lax`), um Session-Fixierung und CSRF-Angriffe zu erschweren.
  * **Zentraler ErrorHandler** – Registriert das `ErrorHandler`-Modul zur Überwachung von Laufzeitfehlern und steuert das Error-Reporting basierend auf dem aktuellen Debug-Status.

* **🗺️ Request-Processing (Der "404-Killer")**
  * **URI-Normalisierung** – Bereinigt die eingehende URL automatisch um den `BASE_URL`-Pfad. Dies ermöglicht den Betrieb des Frameworks sowohl in der Root-Domain als auch in beliebigen Unterverzeichnissen.
  * **Router Dispatching** – Übergibt die gesäuberte URI an den `Router`, der die Anfrage an den entsprechenden Controller delegiert.

* **🛡️ Exception-Handling & Fallbacks**
  * **Graceful Degradation** – Fängt schwere Systemfehler (`Throwable`) ab. Im **Debug-Modus** erfolgt eine detaillierte Fehlerausgabe zur Diagnose; im **Produktionsmodus** wird eine benutzerfreundliche `404.view.php` ausgeliefert.
