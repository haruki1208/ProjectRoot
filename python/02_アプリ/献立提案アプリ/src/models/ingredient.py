class Ingredient:
    def __init__(self, name, check_date, expiration_date):
        self.name = name
        self.check_date = check_date
        self.expiration_date = expiration_date

    def is_expired(self, current_date):
        return current_date > self.expiration_date

    def days_until_expiration(self, current_date):
        return (self.expiration_date - current_date).days

    def __repr__(self):
        return f"Ingredient(name={self.name}, check_date={self.check_date}, expiration_date={self.expiration_date})"