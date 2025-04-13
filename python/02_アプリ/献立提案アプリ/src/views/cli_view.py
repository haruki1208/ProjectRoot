from controllers.ingredient_controller import IngredientController
from controllers.menu_controller import MenuController

class CLIView:
    def __init__(self):
        self.ingredient_controller = IngredientController()
        self.menu_controller = MenuController()

    def display_menu(self):
        print("献立提案アプリ")
        print("1. 食材を追加")
        print("2. 食材を削除")
        print("3. 食材を検索")
        print("4. メニューを提案")
        print("5. 履歴を表示")
        print("6. 終了")

    def get_user_choice(self):
        choice = input("選択してください (1-6): ")
        return choice

    def add_ingredient(self):
        ingredient_name = input("追加する食材の名前を入力してください: ")
        self.ingredient_controller.add_ingredient(ingredient_name)

    def remove_ingredient(self):
        ingredient_name = input("削除する食材の名前を入力してください: ")
        self.ingredient_controller.remove_ingredient(ingredient_name)

    def search_ingredients(self):
        ingredients = self.ingredient_controller.get_all_ingredients()
        print("現在の食材:")
        for ingredient in ingredients:
            print(f"- {ingredient.name}")

    def suggest_menu(self):
        suggested_menus = self.menu_controller.suggest_menu()
        print("オススメのメニュー:")
        for menu in suggested_menus:
            print(f"- {menu.name}")

    def display_history(self):
        history = self.menu_controller.get_history()
        print("履歴:")
        for menu in history:
            print(f"- {menu.name}")

    def run(self):
        while True:
            self.display_menu()
            choice = self.get_user_choice()
            if choice == '1':
                self.add_ingredient()
            elif choice == '2':
                self.remove_ingredient()
            elif choice == '3':
                self.search_ingredients()
            elif choice == '4':
                self.suggest_menu()
            elif choice == '5':
                self.display_history()
            elif choice == '6':
                print("アプリを終了します。")
                break
            else:
                print("無効な選択です。もう一度お試しください。")