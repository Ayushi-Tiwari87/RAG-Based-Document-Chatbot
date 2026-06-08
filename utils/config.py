"""Configuration helpers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    project_root: Path = Path(__file__).resolve().parents[1]
    documents_dir: Path = project_root / "data" / "documents"
    vector_db_dir: Path = project_root / "vectordb"
