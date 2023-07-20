import sqlite3

dbname = 'TEST.db'
# 1.データベースに接続
conn = sqlite3.connect(dbname)

# 2.sqliteを操作するカーソルオブジェクトを作成
cur = conn.cursor()

# 3.テーブルのデータを更新・削除
# データ更新（例ではカラム「name」の「Takahashi」を「Tanaka」に変更します）
cur.execute('UPDATE persons SET name = "Tanaka" WHERE name = "Takahashi"')

# データ削除（例ではカラム「name」の「Suzuki」を削除します）
cur.execute('DELETE FROM persons WHERE name = "Suzuki"')

# 取得したデータはカーソルの中に入る
for row in cur:
    print(row)

# 4.データベースにデータをコミット
conn.commit()

# 5.データベースの接続を切断
cur.close()
conn.close()