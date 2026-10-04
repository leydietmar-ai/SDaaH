class FrameKind:
    USER = "user"
    VENDOR = "vendor"
    SYSTEM = "system"
    NATIVE = "native"
    FUNCTION = "function"
    CLOSURE = "closure"
    UNKNOWN = "unknown"


def detect_frame_kind(frame):
    fn = frame.get("function") or ""
    file = (frame.get("file") or "").replace("\\", "/").lower()

    # Closure
    if "{closure" in fn:
        return FrameKind.CLOSURE

    # Vendor / Composer
    if "/vendor/" in file or "/composer/" in file:
        return FrameKind.VENDOR

    # System / PHP intern
    if "php" in file or "zend" in file or "apache" in file:
        return FrameKind.SYSTEM

    # Native / OS
    if "windows" in file or "system32" in file:
        return FrameKind.NATIVE

    # Freie Funktion
    if frame.get("class") is None and fn:
        return FrameKind.FUNCTION

    # Default: User Code
    return FrameKind.USER
