import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # すべてのリクエストに対してCORSを有効にする


######################
# アプリ停止 → python停止
######################
# ウィンドウを閉じたらpythonも閉じる
@app.route('/close', methods=['POST'])
def shutdown_server():
    # 後でもう少しちゃんと停止する関数にする
    os._exit(0)


######################
# データベース関連
######################
# データベースセット
database_directory = 'C:/Users/yamah/OneDrive/ドキュメント/ProjectRoot/app/typing_game/backend/database/'
dbname = 'tyren_game.db'  # データベース名
conn = sqlite3.connect(database_directory+dbname)
cursor = conn.cursor()
# ユーザーテーブル
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE
                )''')
# スコアテーブル
cursor.execute('''CREATE TABLE IF NOT EXISTS game_results (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    count INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )''')
# タイピング単語テーブル
cursor.execute('''CREATE TABLE IF NOT EXISTS typing_words (
                    id INTEGER,
                    genre TEXT NOT NULL UNIQUE,
                    word TEXT,
                    PRIMARY KEY (id, genre)
                )''')
conn.commit()

###################
# 関数定義
###################

# ユーザー名をテーブルに登録する関数
def insert_user(username):
    conn = sqlite3.connect(database_directory+dbname)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
    conn.commit()
    conn.close()
    
# ユーザー名を取得
def select_username():
    try:
        # データベースに接続
        conn = sqlite3.connect(database_directory+dbname)
        cursor = conn.cursor()
        # ユーザーテーブルからユーザー名を取得
        cursor.execute("SELECT username FROM users")
        # usernames = cursor.fetchall()
        user_names = [row[0] for row in cursor.fetchall()]
        # データベース接続を閉じる
        cursor.close()
        conn.close()

        return user_names
    except Exception as e:
        return {'error': 'Failed to fetch user_names: ' + str(e)}
    

########################
# エンドポイント
########################
# ユーザー登録
@app.route('/register', methods=['POST'])
def register():
    data = request.json # JSON形式のデータを取得
    username = data.get('username')
    if username:
        try:
            insert_user(username)
            return {"username": username, "message": "ユーザー登録が完了しました。"}
        except sqlite3.IntegrityError:
            return {"message": "そのユーザー名は既に存在します。"}, 409
    else:
        return {"message": "ユーザー名を入力してください。"}, 400

@app.route('/get_user_names', methods=['GET'])
def get_user_names():
    user_names = select_username()   # ユーザー名を取得
    # JSON形式でクライアントにデータを返す
    return jsonify(user_names)

if __name__ == '__main__':
    app.run()
