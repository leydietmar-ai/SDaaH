# System Architecture: PHP Error Environment & PySide6 DumpViewer

This overall system combines robust error capturing in PHP (Backend) with a convenient, graphical analysis interface in PySide6 (Frontend). It uses separate communication channels to guarantee maximum stability and simplicity.

---

## Part 1: The PHP Backend (Data Acquisition)

The PHP component runs within the MVC framework and provides four diagnostic tools:

### 1. AbendDump (`ABEND`) & 2. SnapDump (`SNAP`)

* **Data Format:** **JSON**
* **Behavior:** Generate highly structured JSON payloads for post-mortem analyses (stack traces, variable scopes, system context).

### 3. DebugDump (`DEBUG`)

* **Data Format:** **Raw Text Log File** (Line-by-Line)
* **Behavior:** Chronologically collects all classic developer inspections across the entire lifecycle of the HTTP request.
* **Data Loss Protection:** Direct, unbuffered disk writes. No output is lost during HTTP redirects or AJAX calls.

### 4. GtfTrace (`GTF`)

* **Data Format:** **JSON Lines (JSONL)**
* **Behavior:** Sequentially logs the actual control flow at the MVC boundaries (Router, Controller, Model) with high performance during normal operation, including memory metrics and a reduced live call chain (`calling_stack`).
* **Activation:** Controllable "on demand" via central parameters or secret URL triggers to prevent performance overhead in production.

---

## Part 2: The PySide6 Frontend (The DumpViewer)

The DumpViewer is a native desktop application that seamlessly unifies all data sources into a single interface, thanks to the flexible `Grid` subroutine.

### Processing Different Data Sources in the Grid

```text
                         ┌──(Structured Errors)──► [ JSON File  ] ──► [ Grid: stack, locals, code, etc. ]
                         │
[ PHP MVC Application ] ─┼──(Ongoing Debugs)   ──► [ Text Log   ] ──► [ Grid: debuglog (Plaintext) ]
                         │
                         └──(Control Flow Trace)─► [ JSONL File ] ──► [ Grid: debuglog (Collapsed UI) ]
```

1. **Structured Views (via JSON):** The `stack`, `code`, `locals`, `globals` areas, etc., are dynamically populated from the generated JSON file.
2. **Direct Log View (via Text File):** The `debuglog` area reads the raw text log file directly.
3. **Flight Recorder View (via JSONL):** The `debuglog` area reads the sequential JSON Lines via a dedicated `GtfLoader`.
4. **Dynamic Collapsing:** The main routine hides all upper, unused MVC widgets (`stack`, `locals`, `code`, etc.) using `.hide()`.
   * **Grid Auto-Resize:** The `Grid_Layout_Generator` recalculates the areas live so that the `debuglog` area claims the entire screen space for the formatted log.
   * **Syntax Highlighting:** The integrated `PHPHighlighter` has been extended with regular expressions that automatically colorize timestamps, subsystems, and calling stacks.

---

## Architectural Principle: Strict Modularity

To ensure high maintainability and prevent the main classes from bloating, both the PHP backend and the PySide6 frontend follow a strictly modular design.

### 1. Modular PHP Backend

* Each dump and trace type (`ABEND`, `SNAP`, `DEBUG`, `GTF`) encapsulates its own logic within self-contained namespaces and subroutines.
* This keeps the MVC application decoupled from the internal mechanics of error capturing.

### 2. Modular PySide6 Frontend

* **Lean Main Component:** The `DumpViewer` (`QMainWindow`) acts solely as an orchestrator for routing the file type and loading the stylesheet.
* **Encapsulated Subroutines & Sub-Widgets:** Visual components such as the `status_bar` or design helpers (`Color`) are separated into their own files.
* **Dedicated Data Models & Loaders:** The system strictly separates visual presentation from data processing. New data streams (such as the `GtfLoader`) are prepared in isolation before being passed to the existing UI.
