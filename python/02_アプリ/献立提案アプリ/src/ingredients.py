import json
import os

# from utils import get_user_choice

DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/ingredients.json")


def load_ingredients():
    """JSONファイルから食材リストを読み込む"""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_ingredients(ingredients):
    """食材リストをJSONファイルに保存する"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(ingredients, f, ensure_ascii=False, indent=2)


def add_ingredient(ingredients, name):
    """新しい食材を追加する"""
    # 重複チェック
    if any(ingredient["name"] == name for ingredient in ingredients):
        return False  # 既に存在する場合は追加しない

    # 新しい食材を追加
    ingredients.append({"name": name, "checked": True})
    save_ingredients(ingredients)
    return True


def remove_ingredient(ingredients, name):
    """指定された食材を削除する"""
    updated_ingredients = [
        ingredient for ingredient in ingredients if ingredient["name"] != name
    ]
    if len(updated_ingredients) == len(ingredients):
        return False  # 削除対象が見つからない場合

    save_ingredients(updated_ingredients)
    return True


def update_ingredient_check(ingredients, name, checked):
    """指定された食材のチェック状態を更新する"""
    for ingredient in ingredients:
        if ingredient["name"] == name:
            ingredient["checked"] = checked
            save_ingredients(ingredients)
            return True
    return False


# def manage_ingredients():
#     """ターミナル上で食材を管理するメイン関数"""
#     ingredients = load_ingredients()

#     while True:
#         print("\n--- 食材管理メニュー ---")
#         print("1. 食材を表示する")
#         print("2. 食材を追加する")
#         print("3. 食材を削除する")
#         print("4. 保存して終了")
#         print("5. 保存せずに終了")

#         choice = get_user_choice("番号を選んでください: ")

#         if choice == 1:
#             display_ingredients(ingredients)
#         elif choice == 2:
#             add_ingredient(ingredients)
#         elif choice == 3:
#             remove_ingredient(ingredients)
#         elif choice == 4:
#             save_ingredients(ingredients)
#             print("保存しました。終了します。")
#             break
#         elif choice == 5:
#             print("保存せずに終了します。")
#             break
#         else:
#             print("無効な選択です。もう一度入力してください。")


# if __name__ == "__main__":
#     manage_ingredients()
