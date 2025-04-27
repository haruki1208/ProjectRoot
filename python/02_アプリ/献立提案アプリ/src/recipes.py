import os
from dotenv import load_dotenv
import requests

# .envファイルから環境変数を読み込み
load_dotenv()

# APIキーを取得
API_KEY = os.getenv("YOUTUBE_API_KEY")


def search_youtube_videos(ingredients, max_results=3):
    query = " ".join(ingredients) + " レシピ"
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
        recipes.append({"title": title, "link": link})

    return recipes


def display_recipes(recipes):
    """献立候補をターミナルに表示"""
    print("\n--- 献立候補 ---")
    for idx, recipe in enumerate(recipes, 1):
        print(f"{idx}. {recipe['title']}\n   {recipe['link']}\n")
