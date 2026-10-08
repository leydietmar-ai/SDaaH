# 🚀 SDaaH‑Framework

Ein leichtgewichtiges, modernes und sicheres PHP‑MVC‑Framework mit Dependency Injection, Attribute‑Routing, Middleware‑Pipeline, Reflection‑Engine und Response‑Objekt.

- [🚀 SDaaH‑Framework](#-sdaahframework)
  - [MVC-Struktur](#mvc-struktur)
  - [🔄 Der Weg einer Anfrage (Request Lifecycle)](#-der-weg-einer-anfrage-request-lifecycle)
    - [🧩 1. Der Eintritt (Front‑Controller)](#-1-der-eintritt-frontcontroller)
    - [🛣️ 2. Das Routing (Die Weiche)](#️-2-das-routing-die-weiche)
    - [🧱 3. Middleware‑Pipeline (Routing \& CSRF)](#-3-middlewarepipeline-routing--csrf)
    - [🎼 4. Der Controller (Der Dirigent)](#-4-der-controller-der-dirigent)
    - [🎨 5. Die View (Die Präsentation)](#-5-die-view-die-präsentation)
  - [🧰 Logik‑Trennung: Helpers vs. Services](#-logiktrennung-helpers-vs-services)
  - [🧠 Services – Die Spezialisten](#-services--die-spezialisten)
  - [🔐 Das Auth‑System (Sicherheit \& 2FA)](#-das-authsystem-sicherheit--2fa)
    - [AuthController](#authcontroller)
  - [🔑 Passwort‑Reset \& ID‑Verschlüsselung](#-passwortreset--idverschlüsselung)
    - [Workflow](#workflow)
    - [Sicherheits‑Features](#sicherheitsfeatures)
  - [🧭 Workflow‑Helper: Session \& Redirect](#-workflowhelper-session--redirect)
    - [Session](#session)
  - [⏱️ Nice to know: TOTP](#️-nice-to-know-totp)
  - [🧩 Neue Features im Überblick](#-neue-features-im-überblick)

## MVC-Struktur

```Codeblock
├── app/
│   ├── Config/          # Konfigurations-Klassen (DB, Mail, API-Keys)
│   ├── Controllers/     # Meine Logik (BaseController.php + spezifische)
│   ├── Core/            # Router, DI-Container, Response, Model, Reflection
│   ├── Helpers/         # Statische Tools (Session, Redirect, Form)
│   ├── Mail/            # Mailables (ContactMail, ...)
│   ├── Middleware/      # Routing-Middleware, CSRF, Auth, Logging
│   ├── Models/          # Datenbank-Klassen (BaseModel.php + spezifische)
│   ├── Routes/          # Routen (klassisch + Attribute)
│   ├── Services/        # Komplexe Logik (AuthService inkl. OTP, Mailer)
│   ├── Traits/          # "Misch-Komponenten" (CrudTrait, ResponseTrait)
│   └── Views/           # Templates (auth/, layouts/, modal/)
├── data/                # BlogPost-Archiv
├── public/              # Einziger öffentlich erreichbarer Ordner
│   ├── .htaccess        # Leitet alles auf index.php um
│   ├── index.php        # Front-Controller
│   ├── assets/          # CSS, JS, Bilder
│   └── blogposts/       # Images der geposteten Beiträge
├── storage/             # Logfiles, Code, Bildergalerie
├── vendor/              # Composer Libraries
├── .env                 # Sensible Daten (nicht in Git!)
└── composer.json        # Autoloading-Konfiguration
```

---

## 🔄 Der Weg einer Anfrage (Request Lifecycle)

Das Framework folgt einem klaren, sicheren und erweiterbaren Ablauf.
Neu hinzugekommen: DI‑Container, Attribute‑Routing, Middleware‑Pipeline, Reflection‑Analyse, Response‑Objekt.

### 🧩 1. Der Eintritt (Front‑Controller)

**Die .htaccess leitet jede Anfrage auf public/index.php.**

Dort passiert:

- Laden der .env
- Start des Composer‑Autoloadings
- Initialisierung des DI‑Containers
- Initialisierung des Routers
- Aufbau der Middleware‑Pipeline
- Übergabe des Requests an den Router

Der Front‑Controller erzeugt keine direkte Ausgabe mehr — alles läuft über das neue Response‑Objekt.

---

### 🛣️ 2. Das Routing (Die Weiche)

Der Router wurde modernisiert und unterstützt jetzt:

**✔ Klassisches Routing**
Weiterhin möglich über app/Routes/.

**✔ Attribute‑Routing (empfohlen)**
Controller‑Methoden können direkt annotiert werden:

```php
#[Route('/user/profile/{id}', methods: ['GET'], middleware: ['auth'])]
public function profile(int $id) { ... }
```

**✔ Reflection‑basierte Analyse**
Der Router scannt automatisch:

- alle Controller
- alle Methoden mit #[Route]
- Parameter‑Typen
- benötigte Services (DI)
- Middleware‑Definitionen

**✔ Automatisches Parameter‑Binding**
*Beispiel:*

```php
public function store(Request $request, UserService $service)
```

***→ Der DI‑Container injiziert automatisch passende Objekte.***

### 🧱 3. Middleware‑Pipeline (Routing & CSRF)

Middleware wird vor dem Controller ausgeführt und kann:

- CSRF‑Tokens prüfen
- Authentifizierung erzwingen
- Logging durchführen
- Requests blockieren
- Responses zurückgeben

*Beispiel:*

```php
class CsrfMiddleware {
    public function handle(Request $request) {
        if ($request->method() === 'POST' && !Csrf::validate($request->input('_token'))) {
            return Response::json(['error' => 'Invalid CSRF token'], 419);
        }
    }
}
```

*Aktivierung per Attribut:*

```php
#[Route('/post/create', methods: ['POST'], middleware: ['csrf'])]
```

### 🎼 4. Der Controller (Der Dirigent)

Controller bleiben schlank, profitieren aber jetzt von:

✔ Dependency Injection

```php
public function login(AuthService $auth, Request $request)
```

✔ Automatisches Response‑Handling

```php
return Response::view('dashboard', ['user' => $user]);
```

*oder JSON:*

```php
return Response::json(['success' => true]);
```

**✔ Reflection‑basierte Validierung**
Der Router prüft:

- existiert die Methode?
- stimmen die Parameter?
- sind alle Abhängigkeiten verfügbar?

### 🎨 5. Die View (Die Präsentation)

*Unverändert, aber jetzt sauber eingebettet in das Response‑Objekt:*

```php
return Response::view('auth/login', compact('errors'));
```

## 🧰 Logik‑Trennung: Helpers vs. Services

🔧 Helpers – Die Werkzeugkiste

*Statische, zustandslose Tools:*

- Session::set()
- Redirect::to()
- Form::old()

***„Helper sind die Schweizer Taschenmesser – klein, scharf und universell einsetzbar.“***

## 🧠 Services – Die Spezialisten

*Zustandsbehaftete Business‑Logik:*

- AuthService (Passwort, OTP, Brute‑Force‑Schutz)
- MailerService (PHPMailer‑Integration)

***„Services sind die Abteilungsleiter – sie steuern komplette Workflows.“***

## 🔐 Das Auth‑System (Sicherheit & 2FA)

### AuthController

- Nimmt HTTP‑Daten entgegen, validiert Eingaben, ruft den AuthService auf.
- AuthService
- Regelt:
- Passwort‑Prüfung
- OTP‑Validierung
- Brute‑Force‑Schutz
- Login‑Zähler
- QR‑Code‑Generierung

## 🔑 Passwort‑Reset & ID‑Verschlüsselung

### Workflow

- User gibt E‑Mail ein
- Token wird generiert und gehasht gespeichert
- Link enthält:
  - verschlüsselte ID
  - Klartext‑Token
  - Encryption‑Helper
  - encryptId() → Integer → unleserlicher String
  - decryptId() → String → Integer
  - Token‑Validierung

```php
try {
    $userId = Encryption::decryptId($encryptedId);
    // Token + Ablaufdatum prüfen
} catch (\Exception $e) {
    Redirect::to('/login');
}
```

### Sicherheits‑Features

- zeitliche Begrenzung
- Einmaligkeit
- verschlüsselte IDs
- Tokens nur gehasht gespeichert

'''

## 🧭 Workflow‑Helper: Session & Redirect

### Session

- set()
- get()
- flash()
- Redirect
- to()
- back()

## ⏱️ Nice to know: TOTP

**SDaaH-Framework unterstützt TOTP‑basierte Zwei‑Faktor‑Authentifizierung.**

*Test‑Tool:*
<https://totp.danhersam.com/>

***Empfohlene App: Google Authenticator***

## 🧩 Neue Features im Überblick

Feature Beschreibung

| Begriff                | Kurzbeschreibung                                    |
| :--------------------- | :-------------------------------------------------- |
| ⚙️ Dependency Injection | Automatische Bereitstellung von Services & Objekten |
| 🏷️ Attribute‑Routing    | Moderne, deklarative Routen direkt im Controller    |
| 🧵 Middleware‑Pipeline  | CSRF, Auth, Logging, Custom‑Middleware              |
| 📦 Response‑Objekt      | Saubere Trennung von Logik & Ausgabe                |
| 🔍 Reflection‑Engine    | Automatische Analyse von Controllern & Parametern   |
