import sqlite3
import os

# データベースファイルが保存されているディレクトリのパス
database_directory = 'C:/Users/yamah/OneDrive/ドキュメント/ProjectRoot/backend/memo_app/database'

# データベース名
dbname = 'Memo.db'

# データベースに接続
database_file = os.path.join(database_directory, dbname)
conn = sqlite3.connect(database_file)
cursor = conn.cursor()

# 2.sqliteを操作するカーソルオブジェクトを作成
cur = conn.cursor()

# 3.テーブルのデータを取得
# 例では、memosテーブルデータを全件取得
cur.execute('SELECT * FROM memos')

# 取得したデータを出力
for row in cur:
    print(row)

# 4.データベースの接続を切断
cur.close()
conn.close()