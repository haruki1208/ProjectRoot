# Menu Suggestion App

このプロジェクトは、冷蔵庫の食材を管理し、ユーザーにメニューを提案するアプリケーションです。食材のチェック、メニューの提案、消費期限の管理などの機能を提供します。

## 機能

- 食材の追加、削除、検索
- チェックされた食材を基にしたメニュー提案
- 食材の消費期限に基づく優先度の設定
- 過去のメニュー作成履歴の記録と次回提案への反映

## プロジェクト構成

```
menu-suggestion-app
├── src
│   ├── main.py                  # アプリケーションのエントリーポイント
│   ├── controllers
│   │   ├── ingredient_controller.py  # 食材操作を管理
│   │   └── menu_controller.py        # メニュー操作を管理
│   ├── models
│   │   ├── ingredient.py             # 食材モデル
│   │   └── menu.py                   # メニューモデル
│   ├── services
│   │   ├── ingredient_service.py      # 食材ビジネスロジック
│   │   └── menu_service.py            # メニュービジネスロジック
│   ├── utils
│   │   └── date_utils.py              # 日付ユーティリティ
│   └── views
│       ├── cli_view.py               # CLIビュー
│       └── gui_view.py               # GUIビュー
├── requirements.txt                  # 必要なパッケージリスト
├── README.md                         # プロジェクトの説明
└── .gitignore                        # Git管理外ファイル
```

## 使用方法

1. リポジトリをクローンします。
2. 必要なパッケージをインストールします。
   ```
   pip install -r requirements.txt
   ```
3. アプリケーションを起動します。
   ```
   python src/main.py
   ```

## 貢献

このプロジェクトへの貢献は大歓迎です。バグ報告や機能提案は、GitHubのイシューを通じて行ってください。

## ライセンス

このプロジェクトはMITライセンスの下で提供されています。詳細はLICENSEファイルを参照してください。