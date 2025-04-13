class MenuService:
    def __init__(self):
        self.menu_history = []
        self.suggested_menus = []

    def suggest_menus(self, ingredients):
        # 食材に基づいてメニューを提案するロジックを実装
        pass

    def record_menu_creation(self, menu):
        # 作成されたメニューを履歴に記録
        self.menu_history.append(menu)

    def prioritize_menus(self):
        # 優先度の高いメニューを設定するロジックを実装
        pass

    def get_menu_history(self):
        # メニュー履歴を取得
        return self.menu_history

    def update_suggested_menus(self, menus):
        # 提案されたメニューを更新
        self.suggested_menus = menus

    def get_suggested_menus(self):
        # 提案されたメニューを取得
        return self.suggested_menus