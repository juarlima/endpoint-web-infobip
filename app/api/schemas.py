"""Input validation for API endpoints."""

import re
from typing import Optional

CEP_PATTERN = re.compile(r"^\d{5}-?\d{3}$")


def normalize_cep(cep: str) -> Optional[int]:
    """Normalize CEP string to integer. Returns None if invalid."""
    cleaned = cep.replace("-", "").strip()
    if not cleaned.isdigit() or len(cleaned) != 8:
        return None
    return int(cleaned)


def validate_cep(cep: str) -> tuple[bool, Optional[str]]:
    """Validate CEP format. Returns (is_valid, error_message)."""
    if not cep:
        return False, "cep is required"
    if normalize_cep(cep) is None:
        return False, "cep must be 8 numeric digits (e.g. 01001000 or 01001-000)"
    return True, None


def validate_vehicle_type(
    vehicle_type: str, valid_types: set[str]
) -> tuple[bool, Optional[str]]:
    """Validate vehicle type. Returns (is_valid, error_message)."""
    if not vehicle_type:
        return False, "vehicle_type is required"
    if vehicle_type.strip().upper() not in valid_types:
        return False, f"vehicle_type must be one of: {sorted(valid_types)}"
    return True, None
