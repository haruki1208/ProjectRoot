class Menu:
    def __init__(self, name, ingredients, suggestion_date):
        self.name = name
        self.ingredients = ingredients  # List of ingredient names
        self.suggestion_date = suggestion_date

    def __repr__(self):
        return f"Menu(name={self.name}, ingredients={self.ingredients}, suggestion_date={self.suggestion_date})"