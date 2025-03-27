from datetime import datetime


def parse_date(date_str):
    if not date_str:
        return None
    return datetime.strptime(date_str, "%d.%m.%Y %H:%M:%S")
