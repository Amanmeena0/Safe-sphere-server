from datetime import datetime
from typing import Optional

def parse_date(date_str: str, fmt: str = "%Y-%m-%d") -> Optional[datetime]:
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, fmt).date()
    except ValueError:
        return None

def parse_datetime(dt_str: str, fmt: str = "%Y-%m-%d %H:%M:%S") -> Optional[datetime]:
    if not dt_str:
        return None
    try:
        return datetime.strptime(dt_str, fmt)
    except ValueError:
        return None

def format_iso(dt: Optional[datetime]) -> Optional[str]:
    if not dt:
        return None
    return dt.isoformat()
