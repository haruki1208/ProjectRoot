import msvcrt

def handle_input():
    """
    Windows 環境でリアルタイム入力を処理する関数。
    ユーザーがキーを押すと、そのキーを返します。
    """
    char = msvcrt.getch().decode('utf-8')  # キー入力を取得
    return char