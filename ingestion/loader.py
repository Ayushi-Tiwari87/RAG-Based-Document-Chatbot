"""Document loading helpers."""

from __future__ import annotations

from pathlib import Path
from typing import List


def load_documents(source_dir: str | Path) -> List[Path]:
    """Return documents found under the source directory."""
    path = Path(source_dir)
    if not path.exists():
        return []
    return [item for item in path.rglob("*") if item.is_file()]
