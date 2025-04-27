import os
import shutil
from datetime import datetime

# 整理したいフォルダのパス（ダウンロードフォルダなど）
download_folder = os.path.expanduser("C:/Users/yamah/Downloads")
screenshot_folder = os.path.expanduser("C:/Users/yamah/Desktop/ギャラリー/壁紙")

# フォルダチェック
if not os.path.exists(download_folder):
    print(f"エラー: 指定されたフォルダが見つかりません → {download_folder}")
else:
    print("フォルダが見つかりました！")

# フォルダチェック
if not os.path.exists(screenshot_folder):
    print(f"エラー: 指定されたフォルダが見つかりません → {screenshot_folder}")
else:
    print("フォルダが見つかりました！")

# 整理先フォルダの定義
sorted_folders = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "PDFs": [".pdf"],
    "Archives": [".zip", ".rar", ".7z"],
    "Documents": [".docx", ".xlsx", ".txt"]
}

# ダウンロードフォルダの整理
def organize_downloads():
    for file in os.listdir(download_folder):
        file_path = os.path.join(download_folder, file)
        if os.path.isfile(file_path):
            ext = os.path.splitext(file)[1].lower()
            for folder, extensions in sorted_folders.items():
                if ext in extensions:
                    target_folder = os.path.join(download_folder, folder)
                    os.makedirs(target_folder, exist_ok=True)
                    shutil.move(file_path, target_folder)
                    print(f"Moved: {file} → {target_folder}")

# スクリーンショットの整理（年月ごとにフォルダ分け）
def organize_screenshots():
    for file in os.listdir(screenshot_folder):
        file_path = os.path.join(screenshot_folder, file)
        if os.path.isfile(file_path) and file.lower().endswith((".png", ".jpg", ".jpeg")):
            file_time = os.path.getmtime(file_path)
            date_folder = datetime.fromtimestamp(file_time).strftime("%Y-%m")
            target_folder = os.path.join(screenshot_folder, date_folder)
            os.makedirs(target_folder, exist_ok=True)
            shutil.move(file_path, target_folder)
            print(f"Moved: {file} → {target_folder}")

# 実行
organize_downloads()
organize_screenshots()
print("整理完了！")
