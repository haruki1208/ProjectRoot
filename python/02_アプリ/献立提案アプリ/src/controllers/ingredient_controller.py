class IngredientController:
    def __init__(self, ingredient_service):
        self.ingredient_service = ingredient_service

    def add_ingredient(self, name, check_date):
        return self.ingredient_service.add_ingredient(name, check_date)

    def remove_ingredient(self, ingredient_id):
        return self.ingredient_service.remove_ingredient(ingredient_id)

    def search_ingredients(self, query):
        return self.ingredient_service.search_ingredients(query)

    def get_ingredients(self):
        return self.ingredient_service.get_all_ingredients()