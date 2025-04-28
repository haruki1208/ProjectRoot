from utils import get_user_choice
from recipes import search_youtube_videos, display_recipes
from ingredients import (
    load_ingredients,
    remove_selected_ingredients,
    manage_ingredients,
)


# 献立提案の処理
def suggest_recipes():
    ingredients = load_ingredients()
    seen_recipes = []  # 前回提案した献立を保持するリスト

    while True:
        # YouTube検索して献立を提案
        recipes = search_youtube_videos(ingredients)

        # すでに提案した献立を除外
        recipes = [recipe for recipe in recipes if recipe not in seen_recipes]

        if not recipes:  # もしリストが空なら
            print("再検索できる献立がありませんでした。")
            break

        # 献立を表示
        display_recipes(recipes)

        # ユーザーが選択するか、リトライか選ぶ
        user_choice = get_user_choice(
            "気に入った献立があれば選んで、なければ「0」と入力してください: "
        )

        if user_choice == 0:
            print("別の献立を探します...")
            seen_recipes.extend(recipes)  # 提案した献立を記録
            continue  # リトライする

        # 献立を選んだ場合、その食材を登録解除
        selected_recipe = recipes[int(user_choice) - 1]
        remove_selected_ingredients(selected_recipe, ingredients)
        # seen_recipes.append(selected_recipe)  # 提案した献立を記録 後々jsonに保存する
        print(f"{selected_recipe['title']}を選択しました！")
        break


# メイン処理
def main():
    print("献立提案アプリへようこそ！")
    print("食材を登録して、献立を提案します。")
    while True:
        print("\n--- メインメニュー ---")
        print("1. 献立提案")
        print("2. 食材管理")
        print("3. 終了")

        choice = get_user_choice("番号を選んでください: ")

        if choice == 1:
            suggest_recipes()  # 献立提案を開始
            continue
        elif choice == 2:
            manage_ingredients()  # 食材管理を開始
            continue
        elif choice == 3:
            print("アプリを終了します。")
            break
        else:
            print("無効な選択です。")
            continue


if __name__ == "__main__":
    main()
