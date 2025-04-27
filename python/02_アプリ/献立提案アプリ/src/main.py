from recipes import search_youtube_videos, display_recipes
from ingredients import load_ingredients, remove_selected_ingredients

def main():
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
        user_choice = input("気に入った献立があれば選んで、なければ「別のを探す」と入力してください: ")
        
        if user_choice.lower() == "別のを探す":
            print("別の献立を探します...")
            continue  # リトライする
        
        # 献立を選んだ場合、その食材を登録解除
        selected_recipe = recipes[int(user_choice) - 1]
        remove_selected_ingredients(selected_recipe, ingredients)
        seen_recipes.append(selected_recipe)  # 提案した献立を記録
        print(f"{selected_recipe['title']}を選択しました！")
        break

if __name__ == "__main__":
    main()
