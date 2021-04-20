from datetime import datetime


def validate_string(string: str, min_length=0):
    return len(string) >= min_length


def validate_date(iso_date_string: str):
    try:
        datetime.fromisoformat(iso_date_string)
    except:
        return False
    return True


def validate_number_from_string(number: str):
    try:
        float(number)
    except:
        return False
    return True
