import os
import sqlite3
import datetime

# データベースファイルを作成するディレクトリを指定
database_directory = 'C:/Users/yamah/OneDrive/ドキュメント/ProjectRoot/backend/memo_app/database'
dbname = 'Memo.db'  # データベース名
database_file = os.path.join(database_directory, dbname)

# データベースに接続
conn = sqlite3.connect(database_file)
cursor = conn.cursor()

# テーブルの作成(IF NOT EXISTS：既に存在する場合は作成しない)
cursor.execute('''CREATE TABLE IF NOT EXISTS memos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tag TEXT,
                    sentence TEXT,
                    date DATE
                )''')

# メモを追加する関数
def add_memo(tag, sentence):
    date = datetime.date.today().isoformat()  # 今日の日付を取得
    cursor.execute('INSERT INTO memos (tag, sentence, date) VALUES (?, ?, ?)', (tag, sentence, date))
    conn.commit()

# # テスト用：メモを追加
# tag = '仕事'
# sentence = '重要なプレゼンテーションの準備をする'
# add_memo(tag, sentence)

# データベースとの接続を切断
cursor.close()
conn.close()
