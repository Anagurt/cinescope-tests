import datetime


def validate_iso8601_datetime_string(value: str) -> str:
    """Проверяем, что строка является корректной датой и временем в формате ISO 8601."""
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    datetime.datetime.fromisoformat(normalized)
    return value