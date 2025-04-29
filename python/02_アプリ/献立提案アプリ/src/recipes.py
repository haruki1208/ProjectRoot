import os
from dotenv import load_dotenv
import requests
import random  # ランダム選択のために追加

# .envファイルから環境変数を読み込み
load_dotenv()

# APIキーを取得
API_KEY = os.getenv("YOUTUBE_API_KEY")


# YouTube動画を検索する関数
def search_youtube_videos(ingredients, max_results=3):
    # チェックが入っている食材のみを抽出
    checked_ingredients = [
        ingredient["name"] for ingredient in ingredients if ingredient["checked"]
    ]

    # チェックされた食材がない場合は空のリストを返す
    if not checked_ingredients:
        return []

    # チェックされた食材からランダムに 1 から 3 個の値を取得
    num_to_select = random.randint(1, 3)  # 1〜3のどれかをランダムに決める
    random_ingredients = random.sample(
        checked_ingredients, k=min(len(checked_ingredients), num_to_select)
    )
    query = " ".join(random_ingredients) + " レシピ"
    url = "https://www.googleapis.com/youtube/v3/search"

    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": max_results,
        "key": API_KEY,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    results = response.json()

    recipes = []
    for item in results.get("items", []):
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        link = f"https://www.youtube.com/watch?v={video_id}"
        recipes.append(
            {"title": title, "link": link, "used_ingredients": random_ingredients}
        )

    return recipes


# 献立候補を表示する関数
def display_recipes(recipes):
    """献立候補をターミナルに表示"""
    print("\n--- 献立候補 ---")
    for idx, recipe in enumerate(recipes, 1):
        print(f"{idx}. {recipe['title']}\n   {recipe['link']}\n")
