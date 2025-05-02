import flet as ft
from ingredients import (
    load_ingredients,
    save_ingredients,
)
from recipes import search_youtube_videos


def main(page: ft.Page):
    page.title = "献立提案アプリ"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    ingredients = load_ingredients()
    seen_recipes = []

    # ウィンドウサイズを設定
    page.window_width = 1200
    page.window_height = 600

    # 1920x1080 の中央に配置したい場合（位置を調整）
    page.window_left = (1920 - 1200) // 2
    page.window_top = (1080 - 600) // 2

    # オプション（ウィンドウ枠付き・サイズ固定にする）
    page.window_resizable = False

    # あなたのUIの構築処理を書く
    page.add(ft.Text("献立提案アプリ", size=30, weight="bold"))

    def show_main_menu():
        page.clean()
        page.add(
            ft.Text("献立提案アプリへようこそ！", size=24, weight=ft.FontWeight.BOLD),
            ft.ElevatedButton("献立提案", on_click=suggest_recipes),
            ft.ElevatedButton("食材管理", on_click=manage_ingredients),
            ft.ElevatedButton("終了", on_click=lambda e: page.window_close()),
        )

    def manage_ingredients(e=None):
        page.clean()

        ingredients_list = ft.ListView(
            expand=True,
            spacing=5,
            padding=10,
        )

        for item in ingredients:
            ingredients_list.controls.append(ft.Text(item))

        new_ingredient_input = ft.TextField(label="新しい食材を追加")

        def add_ingredient(e):
            name = new_ingredient_input.value.strip()
            if name:
                ingredients.append(name)
                save_ingredients(ingredients)
                new_ingredient_input.value = ""
                manage_ingredients()

        def remove_ingredient(e):
            name = new_ingredient_input.value.strip()
            if name in ingredients:
                ingredients.remove(name)
                save_ingredients(ingredients)
                new_ingredient_input.value = ""
                manage_ingredients()

        page.add(
            ft.Text("食材管理", size=20),
            ingredients_list,
            new_ingredient_input,
            ft.Row(
                [
                    ft.ElevatedButton("追加", on_click=add_ingredient),
                    ft.ElevatedButton("削除", on_click=remove_ingredient),
                ]
            ),
            ft.ElevatedButton("戻る", on_click=lambda e: show_main_menu()),
        )

    def suggest_recipes(e):
        page.clean()
        page.add(ft.Text("献立提案", size=20))

        results = search_youtube_videos(ingredients)
        results = [r for r in results if r not in seen_recipes]

        if not results:
            page.add(ft.Text("再検索できる献立がありませんでした。"))
            page.add(ft.ElevatedButton("戻る", on_click=lambda e: show_main_menu()))
            return

        seen_recipes.extend(results)

        for recipe in results:
            page.add(
                ft.Text(recipe["title"]), ft.Text(recipe["link"], color=ft.Colors.BLUE)
            )

        page.add(ft.ElevatedButton("戻る", on_click=lambda e: show_main_menu()))

    show_main_menu()


ft.app(target=main)
