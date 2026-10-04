import json
from pathlib import Path

class GtfLoader:
    @staticmethod
    def load(file_path: str) -> dict:
        """
        Liest eine *.jsonl GTF-Trace-Datei ein und bereitet ALLE Daten
        inklusive des Calling-Stacks mit erzwungenen Zeilenumbrüchen auf.
        """
        path = Path(file_path)
        if not path.exists():
            return {"logs": ["GTF-Trace-Datei nicht gefunden.\n"]}

        formatted_logs = []
        
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                    
                    # 1. Haupt-Metriken extrahieren
                    timestamp = record.get("timestamp", "").split("T")[-1][:8]
                    component = record.get("component", "UNKNOWN").ljust(12)
                    event = record.get("event", "UNKNOWN").ljust(20)
                    context = json.dumps(record.get("context", {}), ensure_ascii=False)
                    
                    mem_data = record.get("memory", {})
                    mem_usage = mem_data.get("usage", 0) / 1024 / 1024
                    mem_str = f"[{mem_usage:.2f} MB]"

                    # Hauptzeile mit explizitem Zeilenumbruch am Ende
                    log_line = f"{timestamp} | {component} | {event} | {mem_str} | Context: {context}\n"
                    formatted_logs.append(log_line)
                    
                    # 2. Den Calling-Stack auslesen und eingerückt darunter hängen
                    calling_stack = record.get("calling_stack", [])
                    if calling_stack:
                        for idx, frame in enumerate(calling_stack):
                            file_path = frame.get("file", "unknown")
                            file_name = Path(file_path).name 
                            line_num = frame.get("line", 0)
                            func_name = frame.get("function", "unknown")
                            cls_name = frame.get("class", "")
                            
                            call_target = f"{cls_name}->{func_name}()" if cls_name else f"{func_name}()"
                            
                            # Stackzeile mit explizitem Zeilenumbruch am Ende
                            stack_line = f"         └── [Stack #{idx}] {file_name}:{line_num} -> {call_target}\n"
                            formatted_logs.append(stack_line)
                            
                        # Eine saubere Trennzeile vor dem nächsten Event
                        formatted_logs.append("\n")
                    
                except json.JSONDecodeError:
                    continue

        return {"logs": formatted_logs}
