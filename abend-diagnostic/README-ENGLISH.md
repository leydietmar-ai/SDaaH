# Abend Diagnostics System (IPCS for PHP)

A highly structured diagnostic subsystem for PHP inspired by the mainframe principle (ABEND/SNAP). It enables comprehensive recording of the system state during errors as well as continuous tracing without interrupting processes.

The collected data is standardized and optimized for visualization in the accompanying **PySide6 DumpViewer**.

---

## 🏗️ Architecture & Functionality

The system operates entirely in an object-oriented manner, utilizes the resource-efficient **PSR-4 Lazy Loading**, and completely avoids the use of global variables (`$GLOBALS`).

### 1. ABEND (Abnormal End)

Intercepts critical runtime errors via a global exception handler.

- Mirrors the affected closure via reflection.
- Extracts local variables (`use` scope), function arguments, and the live trace.
- Generates a comprehensive JSON log in the `AbendDumps/` folder.

### 2. SNAP (Snapshot Dump)

Allows you to create targeted system snapshots at defined points in the code without terminating the script with `die()` or `exit`.

- Automatically filters internal framework frames out of the stack trace.
- Writes structured snapshots to `SnapDumps/`.

### 3. DEBUG TRACE (Continuous var_dump Chain)

Enables the continuous collection of `var_dump` content during a request.

- Uses output buffering (`ob_start`) to capture output.
- Writes data sequentially to the hard drive (`DebugDumps/`) using `FILE_APPEND`.
- Prevents RAM overload during long loops or when handling large amounts of data.

### 4. GtfTrace

This tracing mechanism is inspired by the structured logic of IBM's z/OS Generalized Trace Facility (GTF),
which I worked with deeply during my career as a 2nd level Field SE Specialist. To be absolutely clear:
This is not a system-wide OS trace like the real z/OS GTF. Instead, it is a lightweight, synchronous
In-App-Trace running directly within the PHP runtime context, designed to bring robust, mainframe-like
diagnostic visibility and structure to modern web applications.

---

## 📁 Directory Structure (Package Layout)

```code
src/
├── Collector/
│   ├── AbendCapture.php           # Monitors risky code blocks (reflection)
│   └── DumpCollector.php          # The core: Consolidates all data for the ABEND dump
├── Debug/
│   └── DebugDumper.php            # Sequential stream logger for var_dumps
├── Environment/
│   └── EnvironmentCollector.php   # Captures PHP version, SAPI, OS, and ini configurations
├── Globals/
│   └── GlobalsCollector.php       # Normalizes superglobals ($_GET, $_POST, $_SERVER, etc.)
├── Memory/
│   └── MemoryCollector.php        # Records current and maximum RAM usage
├── Normalizer/
│   └── ValueNormalizer.php        # Protects against infinite loops (objects/resources → string)
├── Snap/
│   └── SnapDump.php               # Generates manual intermediate snapshots
├── Stacktrace/
    ├── LocalVariableCollector.php # Isolates and filters local variables
    ├── SignatureCollector.php     # Builds detailed function and method signatures
    ├── SourceSnippetCollector.php # Retrieves the code snippet surrounding the error line (padding)
    ├── StacktraceCollector.php    # Collects the complete, extended stack trace of an exception
    └── SnapStacktraceCollector.php # Creates clean, filtered traces for SNAP dumps
├── Trace/
    └── GtfTrace.php               # Writes a continuous trace record in JSON-Lines format
```

---

## 🚀 Integration & Usage

### Enable Autoloading

The system is registered via PSR-4 in `composer.json`:

```json
{
    “name”: “abend/diagnostic”,
    “description”: “Mainframe-inspired Abend, Snap, and GTF Trace environment for PHP”,
    “type”: “library”,
    “license”: “MIT”,
    “minimum-stability”: “stable”,
    “authors”: [
        {
            “name”: “Dietmar Ley”,
            “email”: “leydietmar@gmail.com”
        }
    ],
    “require”: {
        “php”: “>=8.0”
    },
    “autoload”: {
        “psr-4”: {
            “Abend\\”: “src/”
        },
        “files”: [
            “src/bootstrap.php”
        ]
    }
}
```

### 1. Register a global ABEND handler

In the central startup file of your MVC (e.g., `bootstrap/bootstrap.php` or `public/index.php`):

```php
use Abend\Collector\DumpCollector;

\$dumpDir = __DIR__ . ‘/../AbendDumps’;

set_exception_handler(function (Throwable \$e) use (\(dumpDir) {\)dump = DumpCollector::collect(\(e);\)filename = date(‘Ymd_His’) . ‘.json’;

    file_put_contents(
        \(dumpDir . ‘/’ .\)filename,
        json_encode(\$dump, JSON_PRETTY_PRINT)
    );
});
```

### 2. Monitoring Risky Blocks (`AbendCapture`)

In the controller, critical operations are wrapped in a closure:

```php
use Abend\Collector\AbendCapture;

AbendCapture::execute(function () use (&\$foo, &\(bar, &\)result) {
    // If this block crashes, \$foo and \(bar are saved in the dump\)result = \(foo / \)bar;
});
```

### 3. Continuous tracing (`DebugDumper`)

Log variable states without stopping the process:

```php
use Abend\Debug\DebugDumper;

DebugDumper::dump(“User before login”, \$user);
DebugDumper::dump(“Data array”, \$myArray);
```

### 4. Creating Manual Snapshots (`SnapDump`)

Force a full system snapshot at strategic points:

```php
use Abend\Snap\SnapDump;

SnapDump::snap(“State before API call”, [“payload” => \$data]);
```

---

### 5. On-Demand Performance & Event Tracing (GtfTrace)

Continuous tracing of system events in JSON-Lines format (JSONL). Activation can be done flexibly via code or dynamically in the browser using a GET parameter (?gtf_trace). In the central startup file (e.g., public/index.php)

```php
use Abend\Trace\GtfTrace;

// Initialization (triggered by default via ?gtf_trace in the URL)
GtfTrace::init();
```

```php
use Abend\Trace\GtfTrace;

// Log important system events with context
GtfTrace::write(‘Database’, ‘QueryExecuted’, [‘sql’ => $sql, ‘duration_ms’ => 12]);
GtfTrace::write(‘Auth’, ‘UserLoginAttempt’, [‘username’ => $username]);
```

Features of GtfTrace:

- **On-demand trigger**: Activates automatically as soon as `?gtf_trace` is appended to the URL.
- **Automatic file path**: Autonomously creates the `GtfTraces/` folder in the project directory and separates logs by day.
- **In-Depth Insights**: Each entry automatically includes the current memory usage (`MemoryCollector`) and the exact call stack trace (`StacktraceCollector`).
- **Request Tracking**: A unique `request_id` links all log lines from the same HTTP request.

---

## 🛠️ Data Normalization (Security)

The `ValueNormalizer` prepares all data for JSON. It actively protects the system from crashes by:

- **Maximum depth (5 levels)**: Prevents infinite loops caused by circular object references (`**depth_limit**`).
- **Object Conversion**: Converts complex instances into readable structures via `get_object_vars`.
- **Resource Handling**: Data stream connections (such as PDO) are safely marked as `**resource**`.
