# Pythonスクリプトをバックグラウンドで実行
Start-Job -ScriptBlock {
    c:/Users/yamah/OneDrive/ドキュメント/ProjectRoot/Scripts/python.exe "c:/Users/yamah/OneDrive/ドキュメント/ProjectRoot/app/memo_app/backend/Python/app.py"
}

# 1秒待機
Start-Sleep -Seconds 1

# index.htmlを開く
Start-Process "C:/Users/yamah/OneDrive/ドキュメント/ProjectRoot/app/memo_app/frontend/index.html"



