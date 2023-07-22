import os
from flask import Flask, jsonify, request
import sqlite3
import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# データベースファイルを作成するディレクトリを指定
database_directory = 'C:/Users/yamah/OneDrive/ドキュメント/ProjectRoot/backend/memo_app/database'
dbname = 'Memo.db'  # データベース名
database_file = os.path.join(database_directory, dbname)

##########
# 関数定義
##########

# データベース接続関数
def get_db_connection():
    return sqlite3.connect(database_file)

# テーブルの作成
def create_table():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS memos (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            tag TEXT,
                            sentence TEXT,
                            date DATE
                        )''')
        connection.commit()
        connection.close()
        return True
    except Exception as e:
        print("テーブルの作成に失敗しました:", str(e))
        return False

# メモの一覧を取得する関数
def get_memos():
    try:
        # メモを全て取得
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM memos")
        memos = cursor.fetchall()
        connection.close()

        # メモを辞書型のリストに変換
        memo_list = []
        for memo in memos:
            memo_dict = {
                'id': memo[0],
                'tag': memo[1],
                'sentence': memo[2],
                'date': memo[3]
            }
            memo_list.append(memo_dict)

        return memo_list
    except Exception as e:
        return {'error': 'Failed to fetch memos: ' + str(e)}
    
# メモを作成する関数
def create_memo(tag, sentence):
    try:
        # 新しいメモを作成
        date = datetime.date.today().isoformat()  # 今日の日付を取得

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO memos (tag, sentence, date) VALUES (?, ?, ?)', (tag, sentence, date))
        connection.commit()
        connection.close()

        return True, 'Memo created successfully!'
    except Exception as e:
        return False, 'Failed to create memo: ' + str(e)


# テーブルがなければ作成
create_table()

# メモのAPIエンドポイント
@app.route('/api/memos', methods=['GET', 'POST'])
def memos():
    if request.method == 'GET':
        # メモを全て取得
        memos = get_memos()
        return jsonify(memos)

    elif request.method == 'POST':
        try:
            data = request.get_json()
            tag = data['tag']
            sentence = data['sentence']

            success, message = create_memo(tag, sentence)

            if success:
                return jsonify({'message': message}), 201
            else:
                return jsonify({'error': message}), 500
        except Exception as e:
            return jsonify({'error': 'Failed to create memo: ' + str(e)}), 500


if __name__ == '__main__':
    # app.run(debug=True)
    app.run()
