import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
# import pdb

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
# タイピング単語テーブル
cursor.execute('''CREATE TABLE IF NOT EXISTS typing_words (
                    id INTEGER,
                    genre TEXT NOT NULL,
                    word TEXT,
                    PRIMARY KEY (id, genre)
                )''')
# スコアテーブル
cursor.execute('''CREATE TABLE IF NOT EXISTS game_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    score INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users (id)
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
        with sqlite3.connect(db_file) as conn:
            # コネクションを作成した際にカーソルも作成される
            # withブロックを抜けると自動的にカーソルとコネクションがクローズされる

            # INSERT文を作成
            columns_str = ', '.join(columns)
            print('columns_str:',columns_str)
            values_placeholder = ', '.join(['?'] * len(values))
            print('values_placeholder:',values_placeholder)
            sql_query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_placeholder})"
            print('values:',values)

            # SQL文を実行
            conn.execute(sql_query, values) 
            conn.commit()  # コミット

            # # 最後に挿入された行のIDを取得
            # last_inserted_id = conn.lastrowid
            # return last_inserted_id
            return 0

    except sqlite3.Error as e:
        print("Error insert SQL:", e)
        return 8

# デリート文を実行する関数

# アップデート文を実行する関数

# データベースからジャンルごとの単語を取得する関数
def get_words_from_genre(selected_genre_name):
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
        table_name = "users"    # INSERTするテーブル名を指定
        columns = ["username"]  # INSERTするカラム名を指定
        values = [username]     # INSERTする値を指定
        return_code = execute_insert_sql(table_name, columns, values)
        if return_code == 0:
            return {"username": username, "message": "ユーザー登録が完了しました。"}
        else:
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

# ユーザー名からidを取得する
@app.route('/get_id', methods=['POST'])
def get_id():
        try:
            data = request.get_json()
            username = data['username']
            sql_select_query = f"SELECT id FROM users WHERE username = '{username}'"
            id = execute_select_sql(sql_select_query)   # idを取得
            # JSON形式でクライアントにデータを返す
            return jsonify({'userId': id}), 200
        except Exception as e:
            return jsonify({'error': str(e)})


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
    
# ゲーム結果をデータベースに保存するAPI
@app.route('/save_score', methods=['POST'])
def save_score():
    # pdb.set_trace()
    data = request.get_json()
    user_id = data.get('user_id')
    score = data.get('score')
    print('user_id',user_id[0][0])
    print('score',score)

    if user_id is None or score is None:
        return jsonify({'message': 'User ID and score are required.'}), 400

    try:
        table_name = "game_results"    # INSERTするテーブル名を指定
        columns = ["user_id","score"]  # INSERTするカラム名を指定
        values = [user_id[0][0], score]     # INSERTする値を指定
        execute_insert_sql(table_name, columns, values)
        return jsonify({'message': 'Score saved successfully.'}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to save score.', 'error': str(e)}), 500

# 既存ジャンルの複数単語を登録するエンドポイント
@app.route('/register_existing_words', methods=['POST'])
def register_existing_words():
    data = request.get_json()
    genre = data.get('genre')
    words = data.get('words')  # 複数の単語が配列として送信される
    
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        for word in words:
            cursor.execute("INSERT INTO typing_words (genre, word) VALUES (?, ?)", (genre, word.strip()))  # 単語をトリムして登録
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        print("Error inserting words:", e)
        return jsonify({'success': False})

# 新規ジャンルと複数単語を登録するエンドポイント
@app.route('/register_new_words', methods=['POST'])
def register_new_words():
    data = request.get_json()
    genre = data.get('genre')
    words = data.get('words')  # 複数の単語が配列として送信される
    
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        for word in words:
            cursor.execute("INSERT INTO typing_words (genre, word) VALUES (?, ?)", (genre, word.strip()))  # 単語をトリムして登録
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        print("Error inserting words:", e)
        return jsonify({'success': False})

# メイン処理開始
if __name__ == '__main__':
    app.run()
    # app.run(debug=True)
    