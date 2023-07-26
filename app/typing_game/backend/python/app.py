import os
from flask import Flask, jsonify, request
import random
import sqlite3

app = Flask(__name__)

# @app.route("/api/check_input", methods=["POST"])
# def check_input():
#     data = request.json
#     sentence = data["sentence"].strip()
#     typed_text = data["typed_text"].strip()
#     if typed_text == sentence:
#         return jsonify({"result": "正解！"})
#     return jsonify({"result": "不正解"})

# ウィンドウを閉じたらpythonも閉じる
@app.route('/close', methods=['POST'])
def shutdown_server():
    os._exit(0)
    # return jsonify({"message": "POSTリクエストを受け付けました"}), 200

# SQLite3 Database Setup
database_directory = 'C:/Users/yamah/OneDrive/ドキュメント/ProjectRoot/app/typing_game/backend/database/'
dbname = 'tyren_game.db'  # データベース名
# database_file = os.path.join(database_directory, dbname)
conn = sqlite3.connect(database_directory+dbname)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL UNIQUE
                )''')
cursor.execute('''CREATE TABLE IF NOT EXISTS game_results (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    count INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )''')
conn.commit()

# Sample word list
WORD_LIST = ['apple', 'banana', 'cherry', 'date', 'elderberry', 'fig', 'grape']

@app.route('/get_random_word', methods=['GET'])
def get_random_word():
    word = random.choice(WORD_LIST)
    return jsonify({'word': word})

@app.route('/save_game_result', methods=['POST'])
def save_game_result():
    data = request.get_json()
    typed_count = data.get('count')
    
    # Here, you can implement user registration/login functionality
    # and get the user ID based on the logged-in user.

    user_id = 1  # Replace this with the actual user ID

    cursor.execute('INSERT INTO game_results (user_id, count) VALUES (?, ?)', (user_id, typed_count))
    conn.commit()
    return jsonify({'message': 'Game result saved successfully!'})

if __name__ == '__main__':
    app.run()



from flask import Flask, request, jsonify
import sqlite3
import random

app = Flask(__name__)

# データベース初期化
conn = sqlite3.connect('tyren.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS scores (username TEXT, score INTEGER)')

# サンプルの単語リスト
WORDS = ['こんにちは', 'ありがとう', 'さようなら', 'おはよう', 'おやすみ']

@app.route('/get_word', methods=['GET'])
def get_word():
    word = random.choice(WORDS)
    return jsonify({'word': word})

@app.route('/save_score', methods=['POST'])
def save_score():
    data = request.get_json()
    username = data['username']
    score = data['score']

    c.execute('INSERT INTO scores (username, score) VALUES (?, ?)', (username, score))
    conn.commit()

    return jsonify({'message': 'スコアが保存されました'})

if __name__ == '__main__':
    app.run()
