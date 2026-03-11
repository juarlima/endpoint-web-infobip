"""Load and index CSV data files for range-based CEP lookup."""

import csv
import os
from typing import Optional


_fm_rows: list[dict] = []
_lm_rows: list[dict] = []
_loaded = False

DATA_DIR = os.path.normpath(
    os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "data")
)


def _load_csv(filename: str) -> list[dict]:
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        row["ZIP_CODE_INIT"] = int(row["ZIP_CODE_INIT"])
        row["ZIP_CODE_END"] = int(row["ZIP_CODE_END"])
        row["TIPO_VEICULO"] = row["TIPO_VEICULO"].strip().upper()
    return rows


def load_data() -> None:
    """Load CSVs into memory."""
    global _fm_rows, _lm_rows, _loaded  # noqa: PLW0603

    _fm_rows = _load_csv("TABELA_API_FM.csv")

    lm_path = os.path.join(DATA_DIR, "TABELA_API_LM.csv")
    if os.path.exists(lm_path):
        _lm_rows = _load_csv("TABELA_API_LM.csv")

    _loaded = True


def _ensure_loaded() -> None:
    if not _loaded:
        load_data()


def _find_rows(
    rows: list[dict], cep: int, vehicle_type: Optional[str] = None
) -> list[dict]:
    """Find all rows where cep is within ZIP_CODE_INIT..ZIP_CODE_END range."""
    results = []
    for row in rows:
        if row["ZIP_CODE_INIT"] <= cep <= row["ZIP_CODE_END"]:
            if vehicle_type is None or row["TIPO_VEICULO"] == vehicle_type.strip().upper():
                results.append(row)
    return results


def query_fm(cep: int, vehicle_type: Optional[str] = None) -> list[dict]:
    """Query FM table by CEP and optional vehicle type."""
    _ensure_loaded()
    return _find_rows(_fm_rows, cep, vehicle_type)


def query_lm(cep: int, vehicle_type: Optional[str] = None) -> list[dict]:
    """Query LM table by CEP and optional vehicle type."""
    _ensure_loaded()
    return _find_rows(_lm_rows, cep, vehicle_type)


def query_location(cep: int) -> Optional[dict]:
    """Return location info (bairro, cidade, uf) for a CEP, searching FM then LM."""
    _ensure_loaded()
    for rows in (_fm_rows, _lm_rows):
        for row in rows:
            if row["ZIP_CODE_INIT"] <= cep <= row["ZIP_CODE_END"]:
                return {
                    "cep": cep,
                    "BAIRRO": row.get("BAIRRO", ""),
                    "CIDADE_PRINCIPAL": row.get("CIDADE_PRINCIPAL", ""),
                    "UF": row.get("UF", ""),
                }
    return None


def get_valid_vehicle_types(table: str = "fm") -> set[str]:
    """Return the set of valid vehicle types."""
    _ensure_loaded()
    rows = _fm_rows if table == "fm" else _lm_rows
    return {r["TIPO_VEICULO"] for r in rows}
