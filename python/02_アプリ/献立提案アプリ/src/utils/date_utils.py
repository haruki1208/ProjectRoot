from datetime import datetime, timedelta

def get_current_date():
    return datetime.now().date()

def days_between_dates(start_date, end_date):
    return (end_date - start_date).days

def is_expired(check_date, shelf_life_days):
    expiration_date = check_date + timedelta(days=shelf_life_days)
    return get_current_date() > expiration_date

def format_date(date):
    return date.strftime("%Y-%m-%d")

def parse_date(date_string):
    return datetime.strptime(date_string, "%Y-%m-%d").date()