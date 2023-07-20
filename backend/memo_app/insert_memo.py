import sqlite3

dbname = 'Memo.db'
# 1.データベースに接続
conn = sqlite3.connect(dbname)

# 2.sqliteを操作するカーソルオブジェクトを作成
cur = conn.cursor()

# 3.テーブルにメモデータを登録する
# 例では、memosテーブルのsentenceカラムにデータを登録
cur.execute('INSERT INTO memos(tag,sentence) values("メモ","こんにちは")')

cur.execute('INSERT INTO memos(tag,sentence) values("メモ","こんばんは")')

cur.execute('INSERT INTO memos(tag,sentence) values("メモ","おはよう")')

# 4.データベースにデータをコミット
conn.commit()

# 5.データベースの接続を切断
cur.close()
conn.close()