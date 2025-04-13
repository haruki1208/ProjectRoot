class MenuController:
    def __init__(self, menu_service):
        self.menu_service = menu_service

    def suggest_menu(self, ingredients):
        return self.menu_service.get_suggestions(ingredients)

    def record_menu_history(self, menu, was_cooked):
        self.menu_service.record_history(menu, was_cooked)

    def prioritize_ingredients(self, ingredients):
        return self.menu_service.calculate_priority(ingredients)