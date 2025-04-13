class IngredientService:
    def __init__(self):
        self.ingredients = []

    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient)

    def remove_ingredient(self, ingredient_name):
        self.ingredients = [ing for ing in self.ingredients if ing.name != ingredient_name]

    def get_ingredients(self):
        return self.ingredients

    def prioritize_ingredients(self):
        # 優先度を計算するロジックを実装
        # 例: 消費期限が近い食材を優先する
        self.ingredients.sort(key=lambda ing: ing.check_date)

    def get_ingredient_by_name(self, ingredient_name):
        for ingredient in self.ingredients:
            if ingredient.name == ingredient_name:
                return ingredient
        return None

    def update_ingredient(self, ingredient_name, new_ingredient):
        for index, ingredient in enumerate(self.ingredients):
            if ingredient.name == ingredient_name:
                self.ingredients[index] = new_ingredient
                return True
        return False