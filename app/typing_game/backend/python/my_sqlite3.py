import sqlite3

# データベース接続
database_directory = 'C:/Users/yamah/OneDrive/ドキュメント/ProjectRoot/app/typing_game/backend/database/'
dbname = 'tyren_game.db'  # データベース名
conn = sqlite3.connect(database_directory+dbname)

# カーソルオブジェクトを作成
cursor = conn.cursor()

# SQLクエリを実行
# クリエイトテーブル
# cursor.execute('''CREATE TABLE IF NOT EXISTS users (
#                     id INTEGER PRIMARY KEY AUTOINCREMENT,
#                     username TEXT NOT NULL UNIQUE
#                 )''')

# インサート
# cursor.execute('''INSERT INTO users (username)
#                    VALUES ("haruki")
#                 ''')

# デリート
# cursor.execute('''DELETE FROM users
#                     WHERE username = "haruki"
#                 ''')

# ドロップ
# cursor.execute('''DROP TABLE users
#                  ''')

# セレクト
cursor.execute('''SELECT * FROM users
                ''')

rows = cursor.fetchall()
for row in rows:
    print(row)


# コミット
conn.commit()

# データベースとの接続を切る
conn.close()
