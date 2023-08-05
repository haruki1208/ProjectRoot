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
# データベース関連 CREATE TABLE
######################
# データベースセット
database_directory = 'C:/Users/yamah/OneDrive/ドキュメント/ProjectRoot/app/typing_game/backend/database/'
dbname = 'tyren_game.db'  # データベース名
db_file = database_directory+dbname
conn = sqlite3.connect(db_file)
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
                    genre TEXT NOT NULL,
                    word TEXT,
                    PRIMARY KEY (id, genre)
                )''')
conn.commit()


###################
# 関数定義
###################
### SQL ###
# セレクト文を実行して結果を取得
def execute_select_sql(sql_select_query):
    try:
        # SQLiteデータベースに接続
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        # SQL文を実行
        cursor.execute(sql_select_query)
        # 結果を取得
        result = cursor.fetchall()
        # コミットとクローズ
        conn.commit()
        conn.close()

        return result

    except sqlite3.Error as e:
        print("Error select SQL:", e)
        return None

# インサート文を実行する関数
def execute_insert_sql(table_name, columns, values):
    try:
        # SQLiteデータベースに接続
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # 使用例
        # table_name = "my_table"  # INSERTするテーブル名を指定
        # columns = ["column1", "column2", "column3"]  # INSERTするカラム名を指定
        # values = ["value1", "value2", "value3"]  # INSERTする値を指定
        # INSERT文を作成
        columns_str = ', '.join(columns)
        values_placeholder = ', '.join(['?'] * len(values))
        sql_query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_placeholder})"

        # SQL文を実行
        cursor.execute(sql_query, values)
        conn.commit()   # コミット
        conn.close()    # クローズ

        return cursor.lastrowid

    except sqlite3.Error as e:
        print("Error executing SQL:", e)
        return None

# デリート文を実行する関数

# アップデート文を実行する関数

# データベースからジャンルごとの単語を取得する関数
def get_words_from_genre(selected_genre_name):
    # ここでデータベースから単語を取得するクエリを実行する
    # 例: words = ['寿司', 'ラーメン', 'ピザ', 'パスタ']
    sql_select_query = f"SELECT word FROM typing_words WHERE genre = '{selected_genre_name}'"
    words = execute_select_sql(sql_select_query)   # ジャンル名を取得
    return words

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
            # insert_user(username)
            table_name = "users"    # INSERTするテーブル名を指定
            columns = ["username"]  # INSERTするカラム名を指定
            values = [username]     # INSERTする値を指定
            execute_insert_sql(table_name, columns, values)
            return {"username": username, "message": "ユーザー登録が完了しました。"}
        except sqlite3.IntegrityError:
            return {"message": "そのユーザー名は既に存在します。"}, 409
    else:
        return {"message": "ユーザー名を入力してください。"}, 400

# ユーザー名取得 ログイン時選択するため
@app.route('/get_user_names', methods=['GET'])
def get_user_names():
    sql_select_query = "SELECT username FROM users"
    user_names = execute_select_sql(sql_select_query)   # ユーザー名を取得
    # JSON形式でクライアントにデータを返す
    return jsonify(user_names)

# ジャンル名取得 ゲーム開始時に選択するため
@app.route('/get_genre_names', methods=['GET'])
def get_genre_names():
    sql_select_query = "SELECT DISTINCT genre FROM typing_words"
    genre_names = execute_select_sql(sql_select_query)   # ジャンル名を取得
    # JSON形式でクライアントにデータを返す
    return jsonify(genre_names)

# ジャンルを受け取って単語を返す
@app.route('/get_words', methods=['POST'])
def get_words():
    try:
        data = request.get_json()
        selected_genre_name = data['selectedGenreName']
        words = get_words_from_genre(selected_genre_name)
        response = {'words': words}
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run()
    