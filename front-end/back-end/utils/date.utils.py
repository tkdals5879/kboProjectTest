from datetime import datetime

def today_str():
    return datetime.now().strftime("%Y-%m-%d")

def parse_kbo_date(kbo_date_str: str):
    """
    '2025.05.01' → datetime.date(2025, 5, 1)
    """
    return datetime.strptime(kbo_date_str, "%Y.%m.%d").date()
