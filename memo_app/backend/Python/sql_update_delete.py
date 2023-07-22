import sqlite3

dbname = 'TEST.db'
# 1.データベースに接続
conn = sqlite3.connect(dbname)

# 2.sqliteを操作するカーソルオブジェクトを作成
cur = conn.cursor()

# 3.テーブルのデータを更新・削除
# データ更新
cur.execute('UPDATE memos SET tag = "メモ1" WHERE tag = "メモ"')

# データ削除
cur.execute('DELETE FROM memos WHERE sentence = "こんにちは"')

# 取得したデータはカーソルの中に入る
for row in cur:
    print(row)

# 4.データベースにデータをコミット
conn.commit()

# 5.データベースの接続を切断
cur.close()
conn.close()