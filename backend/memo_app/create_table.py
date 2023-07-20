import sqlite3

# 1.カレントディレクトリにTEST.dbがなければ、作成します。
# すでにTEST.dbが作成されていれば、TEST.dbに接続します。
dbname = 'Memo.db'
conn = sqlite3.connect(dbname)

# 2.sqliteを操作するカーソルオブジェクトを作成
cur = conn.cursor()

# 3.テーブルのCreate文を実行(例ではmemosテーブルを作成)
cur.execute(
    'CREATE TABLE memos(id INTEGER PRIMARY KEY AUTOINCREMENT, tag STRING, sentence STRING, date STRING)')

# 4.データベースに情報をコミット
conn.commit()

# 5.データベースの接続を切断
cur.close()
conn.close()