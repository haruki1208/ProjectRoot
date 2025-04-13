import pygame # type: ignore
from game.game_logic import initialize_game, update_game_state, check_win_condition, check_lose_condition

# 初期化
pygame.init()

# ウィンドウサイズとタイトル
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("キーボード操作ゲーム")

# フォントと色
font = pygame.font.Font(None, 36)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def draw_game_state(screen, game_state):
    """ゲームの状態を画面に描画する"""
    screen.fill(WHITE)  # 背景を白で塗りつぶす

    # スコアとレベルを描画
    score_text = font.render(f"スコア: {game_state['score']}", True, BLACK)
    level_text = font.render(f"レベル: {game_state['level']}", True, BLACK)
    screen.blit(score_text, (50, 50))
    screen.blit(level_text, (50, 100))

    # 勝利・敗北メッセージ
    if check_win_condition(game_state):
        win_text = font.render("おめでとうございます！勝利です！", True, BLACK)
        screen.blit(win_text, (200, 300))
    elif check_lose_condition(game_state):
        lose_text = font.render("残念！敗北です！", True, BLACK)
        screen.blit(lose_text, (200, 300))

def main():
    # ゲームの初期化
    game_state = initialize_game()
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # キーボード入力の処理
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # スペースキーでスコアを増やす
                    update_game_state(game_state, 'score')
                elif event.key == pygame.K_l:  # 'l'キーでレベルアップ
                    update_game_state(game_state, 'level_up')
                elif event.key == pygame.K_q:  # 'q'キーで終了
                    running = False

        # 勝利条件と敗北条件をチェック
        if check_win_condition(game_state) or check_lose_condition(game_state):
            game_state['is_running'] = False

        # ゲームの状態を描画
        draw_game_state(screen, game_state)
        pygame.display.flip()

        # フレームレートを制御
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()