import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List


class PathBackup:
    """Manages snapshots of PATH environment variables."""

    def __init__(self, storage_dir: str = None):
        if storage_dir is None:
            self.storage_dir = Path.home() / ".winpath_doctor" / "backups"
        else:
            self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def create_backup(self, path_str: str, label: str = "manual") -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"path_backup_{timestamp}_{label}.json"
        file_path = self.storage_dir / filename
        data = {
            "timestamp": datetime.now().isoformat(),
            "label": label,
            "path_string": path_str,
            "entries": path_str.split(os.pathsep),
        }
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return str(file_path)

    def list_backups(self) -> List[Dict[str, Any]]:
        backups = []
        for p in sorted(self.storage_dir.glob("*.json"), reverse=True):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    data["filepath"] = str(p)
                    backups.append(data)
            except (json.JSONDecodeError, OSError):
                continue
        return backups
