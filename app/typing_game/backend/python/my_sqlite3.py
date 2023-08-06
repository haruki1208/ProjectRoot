import sqlite3

# データベース接続
database_directory = 'C:/Users/yamah/OneDrive/ドキュメント/ProjectRoot/app/typing_game/backend/database/'
dbname = 'tyren_game.db'  # データベース名
conn = sqlite3.connect(database_directory+dbname)

# カーソルオブジェクトを作成
cursor = conn.cursor()

# SQLクエリを実行
# クリエイトテーブル
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE
                )''')
cursor.execute('''CREATE TABLE IF NOT EXISTS typing_words (
                    id INTEGER,
                    genre TEXT NOT NULL,
                    word TEXT,
                    PRIMARY KEY (id, genre)
                )''')
# スコアテーブル
cursor.execute('''CREATE TABLE IF NOT EXISTS game_results (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    score INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )''')

# インサート
# cursor.execute('''INSERT INTO users (username)
#                    VALUES ("test")
#                 ''')
# cursor.execute('''INSERT INTO typing_words (id,genre,word)
#                    VALUES (1,"料理","寿司"),
#                           (2,"料理","ラーメン"),
#                           (3,"料理","ピザ"),
#                           (4,"料理","パスタ"),
#                           (5,"料理","カレーライス"),
#                           (6,"料理","グラタン"),
#                           (7,"料理","オムライス"),
#                           (8,"料理","ハンバーガー"),
#                           (9,"料理","サラダ"),
#                           (10,"料理","ステーキ"),
#                           (11,"料理","寄せ鍋"),
#                           (12,"料理","寿司ロール"),
#                           (13,"料理","シーフード"),
#                           (14,"料理","餃子"),
#                           (15,"料理","シチュー"),
#                           (16,"料理","お好み焼き"),
#                           (17,"料理","たこ焼き"),
#                           (18,"料理","カツ丼"),
#                           (19,"料理","うどん"),
#                           (20,"料理","そば"),
#                           (21,"料理","串カツ"),
#                           (22,"料理","フライドチキン"),
#                           (23,"料理","グリルチキン"),
#                           (24,"料理","ラーメン二郎"),
#                           (25,"料理","カルボナーラ"),
#                           (26,"料理","フォンダンショコラ"),
#                           (27,"料理","クリームブリュレ"),
#                           (28,"料理","タコス"),
#                           (29,"料理","タイ料理"),
#                           (30,"料理","インドカレー"),
#                           (31,"料理","ハワイアンピザ"),
#                           (32,"料理","チキンカレー"),
#                           (33,"料理","チャーハン"),
#                           (34,"料理","タンメン"),
#                           (35,"料理","ラーメンアート"),
#                           (36,"料理","チーズバーガー"),
#                           (37,"料理","カニ料理"),
#                           (38,"料理","鮪料理"),
#                           (39,"料理","焼肉"),
#                           (40,"料理","ホットドッグ"),
#                           (41,"料理","ポテトフライ"),
#                           (42,"料理","カジキマグロ料理"),
#                           (43,"料理","麻婆豆腐"),
#                           (44,"料理","ビーフシチュー"),
#                           (45,"料理","パエリア"),
#                           (46,"料理","焼き鳥"),
#                           (47,"料理","おでん"),
#                           (48,"料理","グリル野菜"),
#                           (49,"料理","焼きそば"),
#                           (50,"料理","クッキー")
#                  ''')


# デリート
# cursor.execute('''DELETE FROM users
#                     WHERE username = "haruki"
#                 ''')
# cursor.execute('''DELETE FROM typing_words
#                 ''')

# ドロップ
# cursor.execute('''DROP TABLE users
#                  ''')
# cursor.execute('''DROP TABLE typing_words
#                  ''')
# cursor.execute('''DROP TABLE game_results
#                  ''')


# セレクト
print("ユーザー")
cursor.execute('''SELECT * FROM users
                ''')
rows = cursor.fetchall()
for row in rows:
    print(row)

# print("タイピングワード")
# cursor.execute('''SELECT * FROM typing_words
#                 ''')
# rows = cursor.fetchall()
# for row in rows:
#     print(row)
    
print("スコア")
cursor.execute('''SELECT * FROM game_results
                ''')
rows = cursor.fetchall()
for row in rows:
    print(row)

# コミット
conn.commit()

# データベースとの接続を切る
conn.close()
