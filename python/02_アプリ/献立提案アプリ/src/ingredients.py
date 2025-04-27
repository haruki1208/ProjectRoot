import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/ingredients.json")


def load_ingredients():
    """食材リストを読み込む"""
    # ファイルが存在しない、または空の場合に初期化
    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)
        print(f"初期化しました: {DATA_FILE}")
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_ingredients(ingredients_list):
    """食材リストを保存する"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(ingredients_list, f, ensure_ascii=False, indent=2)


def display_ingredients(ingredients_list):
    """現在の食材リストを表示する"""
    if not ingredients_list:
        print("\n登録されている食材はありません。")
    else:
        print("\n現在の食材リスト:")
        for idx, item in enumerate(ingredients_list, 1):
            print(f"{idx}. {item}")


def add_ingredient(ingredients_list):
    """食材を追加する"""
    new_item = input(
        "追加する食材を入力してください（キャンセルするには空欄でEnter）: "
    ).strip()
    if new_item:
        ingredients_list.append(new_item)
        print(f"「{new_item}」を追加しました。")
    else:
        print("追加をキャンセルしました。")


# 選ばれた献立に使われた食材を削除する関数
def remove_selected_ingredients(selected_recipe, ingredients_list):
    # 献立の食材を選択されたレシピから取得する
    used_ingredients = selected_recipe.get("ingredients_list", [])

    # 食材リストから使用された食材を削除
    for ingredient in used_ingredients:
        if ingredient in ingredients_list:
            ingredients_list.pop(ingredient)

    print(f"使われた食材: {used_ingredients} が削除されました。")


def remove_ingredient(ingredients_list):
    """食材を削除する"""
    display_ingredients(ingredients_list)
    try:
        idx = int(input("削除する食材の番号を入力してください（キャンセルは0）: "))
        if idx == 0:
            print("削除をキャンセルしました。")
            return
        removed_item = ingredients_list.pop(idx - 1)
        print(f"「{removed_item}」を削除しました。")
    except (ValueError, IndexError):
        print("無効な入力です。")


def manage_ingredients():
    """ターミナル上で食材を管理するメイン関数"""
    ingredients = load_ingredients()

    while True:
        print("\n--- 食材管理メニュー ---")
        print("1. 食材を表示する")
        print("2. 食材を追加する")
        print("3. 食材を削除する")
        print("4. 保存して終了")
        print("5. 保存せずに終了")

        choice = input("番号を選んでください: ").strip()

        if choice == "1":
            display_ingredients(ingredients)
        elif choice == "2":
            add_ingredient(ingredients)
        elif choice == "3":
            remove_ingredient(ingredients)
        elif choice == "4":
            save_ingredients(ingredients)
            print("保存しました。終了します。")
            break
        elif choice == "5":
            print("保存せずに終了します。")
            break
        else:
            print("無効な選択です。もう一度入力してください。")


if __name__ == "__main__":
    manage_ingredients()
