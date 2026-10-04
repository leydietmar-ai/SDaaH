# viewer/loader/debug_loader.py

class DebugLoader:
    @staticmethod
    def load(path: str) -> list[str]:
        with open(path, "r", encoding="utf-8") as f:
            return f.readlines()
