import os
from PySide6.QtGui import QIcon
from subroutines.frame_kind import FrameKind

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICON_DIR = os.path.join(BASE_DIR, "assets", "icons")

# Lazy Cache
_ICON_CACHE = {}

def icon_for_frame_kind(kind):
    if kind not in _ICON_CACHE:
        filename = {
            FrameKind.USER:     "icon_user.png",
            FrameKind.VENDOR:   "icon_vendor.png",
            FrameKind.SYSTEM:   "icon_system.png",
            FrameKind.NATIVE:   "icon_native.png",
            FrameKind.FUNCTION: "icon_function.png",
            FrameKind.CLOSURE:  "icon_lambda.png",
            FrameKind.UNKNOWN:  "icon_unknown.png",
        }.get(kind, "icon_unknown.png")

        full = os.path.join(ICON_DIR, filename)
        _ICON_CACHE[kind] = QIcon(full)

    return _ICON_CACHE[kind]
