from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# データベースファイルのパス
DATABASE = 'memos.db'

# データベース接続関数
def get_db_connection():
    return sqlite3.connect(DATABASE)

# メモのAPIエンドポイント
@app.route('/api/memos', methods=['GET', 'POST'])
def memos():
    if request.method == 'GET':
        # メモを全て取得
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM memos")
        memos = cursor.fetchall()
        connection.close()
        return jsonify(memos)

    elif request.method == 'POST':
        # 新しいメモを作成
        data = request.get_json()
        title = data['title']
        content = data['content']

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO memos (title, content) VALUES (?, ?)", (title, content))
        connection.commit()
        connection.close()

        return jsonify({'message': 'Memo created successfully!'}), 201

if __name__ == '__main__':
    app.run(debug=True)
