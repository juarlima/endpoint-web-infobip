"""Business logic for API endpoints."""

from typing import Optional

from typing import Optional as _Optional

from app.api.data_loader import get_valid_vehicle_types, query_fm, query_lm, query_location
from app.api.schemas import normalize_cep, validate_cep, validate_vehicle_type


def validate_input(
    cep: str, vehicle_type: str, table: str = "fm"
) -> dict:
    """Validate CEP + vehicle type and return result."""
    errors = []

    cep_valid, cep_err = validate_cep(cep)
    if not cep_valid:
        errors.append(cep_err)

    valid_types = get_valid_vehicle_types(table)
    vt_valid, vt_err = validate_vehicle_type(vehicle_type, valid_types)
    if not vt_valid:
        errors.append(vt_err)

    return {"valid": len(errors) == 0, "errors": errors}


def lookup(
    cep: str,
    vehicle_type: Optional[str] = None,
    table: str = "fm",
) -> list[dict]:
    """Look up rows by CEP (range match) and optional vehicle type."""
    cep_int = normalize_cep(cep)
    if cep_int is None:
        return []

    query_fn = query_fm if table == "fm" else query_lm
    return query_fn(cep_int, vehicle_type)


def lookup_location(cep: str) -> _Optional[dict]:
    """Look up location info (bairro, cidade, uf) by CEP."""
    cep_int = normalize_cep(cep)
    if cep_int is None:
        return None
    return query_location(cep_int)
