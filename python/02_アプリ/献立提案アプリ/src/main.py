from controllers.ingredient_controller import IngredientController
from controllers.menu_controller import MenuController
from views.cli_view import CLIView

def main():
    ingredient_controller = IngredientController()
    menu_controller = MenuController()
    view = CLIView()

    view.display_welcome_message()

    while True:
        user_choice = view.get_user_choice()
        
        if user_choice == '1':
            ingredient_controller.add_ingredient()
        elif user_choice == '2':
            ingredient_controller.remove_ingredient()
        elif user_choice == '3':
            menu_controller.suggest_menu()
        elif user_choice == '4':
            view.display_exit_message()
            break
        else:
            view.display_invalid_choice_message()

if __name__ == "__main__":
    main()