import pygame # type: ignore[import]
import random
import sys

# 初期化
pygame.init()

# ウィンドウサイズとタイトル
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("シューティングゲーム")

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# フォントの設定
try:
    font = pygame.font.Font("C:/Windows/Fonts/meiryo.ttc", 24)  # 日本語対応フォントを指定
    title_font = pygame.font.Font("C:/Windows/Fonts/meiryo.ttc", 36)  # タイトル用フォント
    instruction_font = pygame.font.Font("C:/Windows/Fonts/meiryo.ttc", 20)  # 説明用フォント
except FileNotFoundError:
    font = pygame.font.Font(None, 36)  # フォールバックとしてデフォルトフォントを使用

# FPS
clock = pygame.time.Clock()
FPS = 60

# 難易度設定
difficulty = "Normal"  # デフォルトの難易度
difficulty_settings = {
    "Easy": {"enemy_bullet_speed": 1, "enemy_hp": 200, "enemy_bullet_interval": 20},
    "Normal": {"enemy_bullet_speed": 2, "enemy_hp": 400, "enemy_bullet_interval": 10},
    "Hard": {"enemy_bullet_speed": 3, "enemy_hp": 600, "enemy_bullet_interval": 5},
}

# プレイヤーの設定
player_size = 25
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT - 100
player_speed = 5
def_player_hp = 100
player_hp = def_player_hp

# 弾の設定
player_bullets = []
bullet_speed = -5
bullet_size = 5

# プレイヤーの弾の発射間隔を設定
bullet_interval = 300  # ミリ秒
last_bullet_time = 0   # 最後に弾を発射した時間

# 敵の設定
enemy_size = 50
enemy_x = SCREEN_WIDTH // 2
enemy_y = 50
enemy_bullets = []

# アイテムの設定
item_types = ["invincibility", "heal", "bullet_increase"]  # アイテムの種類
items = []  # 現在のアイテムを格納するリスト
item_spawn_interval = 10000  # アイテムの生成間隔（ミリ秒）
last_item_spawn_time = 0  # 最後にアイテムを生成した時間
item_effect_duration = 10000  # アイテム効果の持続時間（ミリ秒）
active_effects = {"invincibility": False, "bullet_increase": False}  # 現在の効果
effect_start_time = {"invincibility": 0, "bullet_increase": 0}  # 効果開始時間

# ゲームの難易度を選択する画面
def show_difficulty_screen():
    screen.fill(BLACK)
    
    # タイトルと説明文を描画
    title_text = title_font.render("シューティングゲーム", True, WHITE)
    instruction_text_1 = font.render("難易度を選択してください:", True, WHITE)
    instruction_text_2 = instruction_font.render("1(Easy), 2(Normal), 3(Hard)", True, WHITE)

    # テキストを画面に配置
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 4))
    screen.blit(instruction_text_1, (SCREEN_WIDTH // 2 - instruction_text_1.get_width() // 2, SCREEN_HEIGHT // 2 - 40))
    screen.blit(instruction_text_2, (SCREEN_WIDTH // 2 - instruction_text_2.get_width() // 2, SCREEN_HEIGHT // 2 + 10))

    pygame.display.flip()

    waiting = True
    global difficulty
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    difficulty = "Easy"
                    waiting = False
                elif event.key == pygame.K_2:
                    difficulty = "Normal"
                    waiting = False
                elif event.key == pygame.K_3:
                    difficulty = "Hard"
                    waiting = False

# ゲーム開始前の画面
def show_start_screen():
    screen.fill(BLACK)
    start_text = font.render("スペースキーを押してゲームを開始", True, WHITE)
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

# ゲーム終了時の画面
def show_end_screen(text):
    screen.fill(BLACK)
    end_text = font.render(text, True, WHITE)
    screen.blit(end_text, (SCREEN_WIDTH // 2 - end_text.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

# ゲームループ
def main_game():
    global player_x, player_y, enemy_x, player_hp, enemy_hp, player_bullets, enemy_bullets, last_bullet_time, last_item_spawn_time

    # 難易度設定を適用
    global enemy_bullet_speed, def_enemy_hp, enemy_bullet_interval
    enemy_bullet_speed = difficulty_settings[difficulty]["enemy_bullet_speed"]
    def_enemy_hp = difficulty_settings[difficulty]["enemy_hp"]
    enemy_hp = def_enemy_hp
    enemy_bullet_interval = difficulty_settings[difficulty]["enemy_bullet_interval"]
    
    last_item_spawn_time = pygame.time.get_ticks() # アイテム生成の初期化

    running = True
    while running:
        screen.fill(BLACK)

        current_time = pygame.time.get_ticks()  # 現在の時間を取得

        # イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # アイテムの生成
        if current_time - last_item_spawn_time > item_spawn_interval:
            item_x = random.randint(0, SCREEN_WIDTH - 30)  # アイテムのランダムなX座標
            item_y = random.randint(SCREEN_HEIGHT // 3, SCREEN_HEIGHT - 30)  # アイテムのランダムなY座標
            item_type = random.choice(item_types)  # ランダムなアイテムの種類
            items.append({"x": item_x, "y": item_y, "type": item_type})  # アイテムをリストに追加
            last_item_spawn_time = current_time  # 最後にアイテムを生成した時間を更新
        
        # アイテムの取得
        for item in items[:]:
            if player_x < item["x"] + 30 and player_x + player_size > item["x"] and player_y < item["y"] + 30 and player_y + player_size > item["y"]:
                if item["type"] == "invincibility":
                    active_effects["invincibility"] = True
                    effect_start_time["invincibility"] = current_time
                elif item["type"] == "heal":
                    player_hp = min(def_player_hp, player_hp + 20)  # HPを回復（最大値を超えない）
                elif item["type"] == "bullet_increase":
                    active_effects["bullet_increase"] = True
                    effect_start_time["bullet_increase"] = current_time
                items.remove(item)  # アイテムを削除
                
        # アイテム効果の適用
        if active_effects["invincibility"] and current_time - effect_start_time["invincibility"] > item_effect_duration:
            active_effects["invincibility"] = False  # 無敵効果を終了

        if active_effects["bullet_increase"] and current_time - effect_start_time["bullet_increase"] > item_effect_duration:
            active_effects["bullet_increase"] = False  # 弾増加を終了

        # プレイヤーの移動
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and player_y > SCREEN_HEIGHT // 4:  # スクリーンの上部に移動しないように制限
            player_y -= player_speed
        if keys[pygame.K_s] and player_y < SCREEN_HEIGHT - player_size:
            player_y += player_speed
        if keys[pygame.K_a] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_d] and player_x < SCREEN_WIDTH - player_size:
            player_x += player_speed
        
        # 敵の移動
        if enemy_x < player_x:
            enemy_x += 1
        elif enemy_x > player_x:
            enemy_x -= 1
        
        ## 敵が高速移動
        if random.randint(1, 120) == 1:
            enemy_x = random.randint(0, SCREEN_WIDTH - enemy_size)

        # プレイヤーの弾を発射
        if current_time - last_bullet_time > bullet_interval:  # 一定時間経過した場合
            if active_effects["bullet_increase"]:  # 弾増加効果があるとき
                player_bullets.append([player_x + player_size // 2, player_y, -1])  # 左斜め下
                player_bullets.append([player_x + player_size // 2, player_y, 1])   # 右斜め下
            player_bullets.append([player_x + player_size // 2, player_y, 0])  # 弾を発射
            last_bullet_time = current_time  # 最後に弾を発射した時間を更新

        # プレイヤーの弾の移動
        for bullet in player_bullets[:]:
            bullet[0] += bullet[2] * bullet_speed  # 横方向の移動（-1: 左, 0: 真下, 1: 右）
            bullet[1] += bullet_speed
            if bullet[0] < 0 or bullet[0] > SCREEN_WIDTH:
                bullet[2] = -bullet[2]  # 横方向の移動を反転
            if bullet[1] < 0:
                player_bullets.remove(bullet)

        # 敵の弾を発射
        if random.randint(1, enemy_bullet_interval) == 1:  # 弾の発射頻度を調整
            # 左斜め下、真下、右斜め下の弾を追加
            enemy_bullets.append([enemy_x + enemy_size // 2, enemy_y + enemy_size, -1])  # 左斜め下
            enemy_bullets.append([enemy_x + enemy_size // 2, enemy_y + enemy_size, -0.5])   # 左斜め下
            enemy_bullets.append([enemy_x + enemy_size // 2, enemy_y + enemy_size, 0])   # 真下
            enemy_bullets.append([enemy_x + enemy_size // 2, enemy_y + enemy_size, 0.5])   # 右斜め下
            enemy_bullets.append([enemy_x + enemy_size // 2, enemy_y + enemy_size, 1])   # 右斜め下

        # 敵の弾の移動
        for bullet in enemy_bullets[:]:
            bullet[0] += bullet[2] * enemy_bullet_speed  # 横方向の移動（-1: 左, 0: 真下, 1: 右）
            bullet[1] += enemy_bullet_speed             # 縦方向の移動
            if bullet[0] < 0 or bullet[0] > SCREEN_WIDTH:
                bullet[2] = -bullet[2]  # 横方向の移動を反転
            if bullet[1] > SCREEN_HEIGHT:
                enemy_bullets.remove(bullet)

        # プレイヤーが敵の弾に当たる判定
        for bullet in enemy_bullets[:]:
            if player_x < bullet[0] < player_x + player_size and player_y < bullet[1] < player_y + player_size:
                if not active_effects["invincibility"]:  # 無敵状態でない場合のみHPを減らす
                    player_hp -= 10
                enemy_bullets.remove(bullet)

        # 敵がプレイヤーの弾に当たる判定
        for bullet in player_bullets[:]:
            if enemy_x < bullet[0] < enemy_x + enemy_size and enemy_y < bullet[1] < enemy_y + enemy_size:
                enemy_hp -= 10
                player_bullets.remove(bullet)

        # ゲーム終了条件
        if player_hp <= 0:
            show_end_screen("ゲームオーバー！")
            running = False
        if enemy_hp <= 0:
            show_end_screen("勝利！")
            running = False

        # プレイヤーの描画
        pygame.draw.rect(screen, BLUE, (player_x, player_y, player_size, player_size))

        # プレイヤーの弾の描画
        for bullet in player_bullets:
            pygame.draw.circle(screen, GREEN, bullet[:2], bullet_size)

        # 敵の描画
        pygame.draw.rect(screen, RED, (enemy_x, enemy_y, enemy_size, enemy_size))

        # 敵の弾の描画
        for bullet in enemy_bullets:
            pygame.draw.circle(screen, WHITE, bullet[:2], bullet_size)
        
        # アイテムの描画
        for item in items:
            if item["type"] == "invincibility":
                pygame.draw.rect(screen, (255, 255, 0), (item["x"], item["y"], 30, 30))  # 黄色
            elif item["type"] == "heal":
                pygame.draw.rect(screen, (0, 255, 0), (item["x"], item["y"], 30, 30))  # 緑
            elif item["type"] == "bullet_increase":
                pygame.draw.rect(screen, (255, 0, 0), (item["x"], item["y"], 30, 30))  # 赤

        # HPの表示
        player_hp_text = font.render(f"Player HP: {player_hp}", True, WHITE)
        enemy_hp_text = font.render(f"Enemy HP: {enemy_hp}", True, WHITE)
        screen.blit(player_hp_text, (10, SCREEN_HEIGHT - 40))
        screen.blit(enemy_hp_text, (10, 10))

        # プレイヤーのHPバー
        pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH // 2 - def_player_hp, SCREEN_HEIGHT - 40, player_hp * 2, 10))  # 長さはHPに比例
        pygame.draw.rect(screen, RED, (SCREEN_WIDTH // 2 + def_player_hp - (def_player_hp - player_hp) * 2 , SCREEN_HEIGHT - 40, (def_player_hp - player_hp) * 2, 10))  # 減少部分

        # 敵のHPバー
        pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH // 2 - def_enemy_hp // 2, 10, enemy_hp, 10))  # 長さはHPに比例
        pygame.draw.rect(screen, RED, (SCREEN_WIDTH // 2 + def_enemy_hp // 2 - (def_enemy_hp - enemy_hp), 10, def_enemy_hp - enemy_hp, 10))  # 減少部分

        # 画面更新
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

# メイン処理
if __name__ == "__main__":
    show_difficulty_screen()  # 難易度選択画面を表示
    show_start_screen()
    main_game()