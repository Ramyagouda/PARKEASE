"""Utility helpers and validation functions."""
import re
from typing import Optional


def validate_vehicle_no(vehicle_no: str) -> bool:
    """Basic vehicle number validation using regex.

    Accepts common alphanumeric patterns. Caller may add stricter rules.
    """
    if not isinstance(vehicle_no, str):
        return False
    v = vehicle_no.strip().upper()
    # Allow letters, digits, hyphen and spaces (e.g., "MH12-AB1234" or "AB 1234")
    pattern = r"^[A-Z0-9\- ]{4,20}$"
    return bool(re.match(pattern, v))


def normalize_vehicle_no(vehicle_no: str) -> Optional[str]:
    if not vehicle_no:
        return None
    return vehicle_no.strip().upper()
