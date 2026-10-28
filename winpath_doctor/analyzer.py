import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Tuple


class PathEntry:
    """Represents a single entry within the PATH environment variable."""

    def __init__(self, raw: str, index: int):
        self.raw = raw
        self.index = index
        self.cleaned = self.normalize(raw)
        self.exists = Path(self.cleaned).exists() if self.cleaned else False
        self.is_dir = Path(self.cleaned).is_dir() if self.exists else False

    @staticmethod
    def normalize(path_str: str) -> str:
        if not path_str:
            return ""
        s = path_str.strip().strip('"').strip("'")
        return os.path.normpath(s)


class PathAnalyzer:
    """Analyzes PATH string for duplicates, dead directories, and formatting issues."""

    def __init__(self, path_str: str = None):
        if path_str is None:
            path_str = os.environ.get("PATH", "")
        self.raw_path = path_str
        self.entries = [
            PathEntry(p, idx)
            for idx, p in enumerate(path_str.split(os.pathsep))
            if p.strip()
        ]

    def get_duplicates(self) -> List[Tuple[int, str]]:
        seen = set()
        duplicates = []
        is_win = sys.platform == "win32"
        for entry in self.entries:
            key = entry.cleaned.lower() if is_win else entry.cleaned
            if key in seen:
                duplicates.append((entry.index, entry.raw))
            else:
                seen.add(key)
        return duplicates

    def get_dead_paths(self) -> List[Tuple[int, str]]:
        return [(e.index, e.raw) for e in self.entries if not e.exists or not e.is_dir]

    def clean(self) -> List[str]:
        seen = set()
        cleaned_list = []
        is_win = sys.platform == "win32"
        for entry in self.entries:
            if not entry.cleaned or not entry.exists or not entry.is_dir:
                continue
            key = entry.cleaned.lower() if is_win else entry.cleaned
            if key not in seen:
                seen.add(key)
                cleaned_list.append(entry.cleaned)
        return cleaned_list

    def generate_report(self) -> Dict[str, Any]:
        duplicates = self.get_duplicates()
        dead = self.get_dead_paths()
        cleaned = self.clean()
        return {
            "total_entries": len(self.entries),
            "duplicate_count": len(duplicates),
            "dead_count": len(dead),
            "duplicates": duplicates,
            "dead_paths": dead,
            "cleaned_entries": cleaned,
            "cleaned_path_str": os.pathsep.join(cleaned),
        }
