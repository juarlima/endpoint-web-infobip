"""Load and index CSV data files for fast lookup."""

import csv
import os
from typing import Optional


_coverage_index: dict[tuple[str, str], dict] = {}
_pricing_index: dict[tuple[str, str], dict] = {}
_loaded = False


def _data_path(filename: str) -> str:
    base = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "data")
    return os.path.normpath(os.path.join(base, filename))


def _load_csv(filepath: str) -> list[dict]:
    with open(filepath, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _build_index(rows: list[dict]) -> dict[tuple[str, str], dict]:
    index: dict[tuple[str, str], dict] = {}
    for row in rows:
        key = (row["cep"].strip(), row["vehicle_type"].strip().lower())
        index[key] = row
    return index


def load_data() -> None:
    """Load CSVs into memory and build lookup indexes."""
    global _coverage_index, _pricing_index, _loaded  # noqa: PLW0603

    coverage_rows = _load_csv(_data_path("coverage.csv"))
    pricing_rows = _load_csv(_data_path("pricing.csv"))

    _coverage_index = _build_index(coverage_rows)
    _pricing_index = _build_index(pricing_rows)
    _loaded = True


def _ensure_loaded() -> None:
    if not _loaded:
        load_data()


def get_coverage(cep: str, vehicle_type: str) -> Optional[dict]:
    """Return coverage info for a CEP + vehicle_type, or None."""
    _ensure_loaded()
    return _coverage_index.get((cep.strip(), vehicle_type.strip().lower()))


def get_pricing(cep: str, vehicle_type: str) -> Optional[dict]:
    """Return pricing info for a CEP + vehicle_type, or None."""
    _ensure_loaded()
    return _pricing_index.get((cep.strip(), vehicle_type.strip().lower()))


def get_valid_vehicle_types() -> set[str]:
    """Return the set of valid vehicle types from loaded data."""
    _ensure_loaded()
    return {k[1] for k in _coverage_index}


def get_valid_ceps() -> set[str]:
    """Return the set of valid CEPs from loaded data."""
    _ensure_loaded()
    return {k[0] for k in _coverage_index}
