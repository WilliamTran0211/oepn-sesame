import os
from pathlib import Path


def ensure_dir(path: str | Path) -> Path:
    path_obj = Path(path)
    path_obj.mkdir(parents=True, exist_ok=True)
    return path_obj


def get_absolute_path(relative_path: str) -> str:
    return str(Path(relative_path).resolve())
