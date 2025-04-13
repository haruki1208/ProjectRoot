import random

def number_guessing_game():
    print("数当てゲームへようこそ！")
    print("1から100までの数字を当ててください。")

    # ランダムな数を生成
    target_number = random.randint(1, 100)
    attempts = 0

    while True:
        try:
            # ユーザーの入力を取得
            guess = int(input("あなたの予想: "))
            attempts += 1

            if guess < target_number:
                print("もっと大きい数字です！")
            elif guess > target_number:
                print("もっと小さい数字です！")
            else:
                print(f"正解です！{attempts}回で当たりました！")
                break
        except ValueError:
            print("数字を入力してください。")

if __name__ == "__main__":
    number_guessing_game()