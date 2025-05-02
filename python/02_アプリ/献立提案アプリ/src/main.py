import tkinter as tk
import tkinter.ttk as ttk  # ttk をインポート
import webbrowser
from tkinter import messagebox
from datetime import datetime
import os
import json
from ingredients import (
    load_ingredients,
    save_ingredients,
    add_ingredient,
    remove_ingredient,
    update_ingredient_check,
)
from recipes import search_youtube_videos


class MenuSuggestionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("献立提案アプリ")
        self.ingredients = load_ingredients()
        self.seen_recipes = []

        # ウィンドウサイズ変更
        width = 1200
        height = 600
        x_position = (1920 - width) // 2
        y_position = (1080 - height) // 2
        self.root.geometry(f"{width}x{height}+{x_position}+{y_position}")
        self.root.resizable(False, False)

        style = ttk.Style()
        style.theme_use(
            "clam"
        )  # テーマを "clam" に設定（他に "default", "alt", "classic" などが利用可能）

        # Combobox のスタイルをカスタマイズ
        style.configure(
            "TCombobox",
            padding=5,
            font=("Arial", 12),  # フォントサイズとスタイル
            foreground="black",  # 文字色
            background="white",  # 背景色
        )

        # メインメニュー画面の作成（中央寄せ）
        self.main_menu_frame = tk.Frame(root)
        self.main_menu_frame.pack(expand=True, fill="both")

        inner_frame = tk.Frame(self.main_menu_frame)
        inner_frame.pack(expand=True)

        tk.Label(
            inner_frame, text="献立提案アプリへようこそ！", font=("Arial", 16)
        ).pack(pady=(20, 10))

        tk.Button(
            inner_frame, text="献立提案", command=self.suggest_recipes, width=20
        ).pack(pady=5)

        tk.Button(
            inner_frame, text="食材管理", command=self.manage_ingredients, width=20
        ).pack(pady=5)

        tk.Button(inner_frame, text="終了", command=self.root.quit, width=20).pack(
            pady=20
        )

        # 食材管理画面
        self.ingredients_frame = tk.Frame(root)

        # 献立提案画面
        self.suggestion_frame = tk.Frame(root)

        # チェックボックス用の変数
        self.ingredient_vars = {}

    def switch_frame(self, frame):
        """フレームを切り替える"""
        # 現在表示されているすべてのウィジェットを非表示にする
        for widget in self.root.winfo_children():
            widget.pack_forget()

        # 対象フレーム内のウィジェットをクリア
        if frame != self.main_menu_frame:
            for widget in frame.winfo_children():
                widget.destroy()

        # 対象フレームを表示
        frame.pack(expand=True, fill="both")

    def manage_ingredients(self):
        """食材管理画面"""
        self.switch_frame(self.ingredients_frame)
        for widget in self.ingredients_frame.winfo_children():
            widget.destroy()

        tk.Label(self.ingredients_frame, text="食材管理", font=("Arial", 16)).pack(
            pady=10
        )

        # ------- スクロール可能なキャンバスエリア（中央揃え） -------
        scroll_canvas_frame = tk.Frame(self.ingredients_frame)
        scroll_canvas_frame.pack(pady=10)

        canvas = tk.Canvas(scroll_canvas_frame, width=600, height=200)
        scrollbar = tk.Scrollbar(
            scroll_canvas_frame, orient="vertical", command=canvas.yview
        )

        # スクロール対象のフレーム
        scrollable_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # ------- 食材チェックボックス（4列でgrid配置） -------
        self.ingredients = load_ingredients()
        self.ingredient_vars = {}
        for i, ingredient in enumerate(self.ingredients):
            var = tk.BooleanVar(value=ingredient["checked"])
            self.ingredient_vars[ingredient["name"]] = var
            tk.Checkbutton(
                scrollable_frame,
                text=ingredient["name"],
                variable=var,
                command=lambda name=ingredient[
                    "name"
                ], var=var: self.update_ingredient_check(name, var.get()),
            ).grid(row=i // 6, column=i % 6, padx=20, pady=5)

        # ------- 入力＆削除ボタンエリアを中央揃えでまとめる -------
        control_frame = tk.Frame(self.ingredients_frame)
        control_frame.pack(pady=20)

        # 食材追加欄
        tk.Label(control_frame, text="新しい食材を追加:").pack()
        self.new_ingredient_entry = tk.Entry(control_frame)
        self.new_ingredient_entry.pack(pady=5)
        tk.Button(control_frame, text="追加", command=self.add_new_ingredient).pack(
            pady=5
        )

        # 食材削除
        tk.Label(control_frame, text="削除する食材を選択:").pack(pady=5)
        self.remove_ingredient_var = tk.StringVar()
        self.remove_ingredient_combobox = ttk.Combobox(
            control_frame,
            textvariable=self.remove_ingredient_var,
            values=[i["name"] for i in self.ingredients],
            state="readonly",
            font=("Arial", 12),
        )
        self.remove_ingredient_combobox.set("選択してください")
        self.remove_ingredient_combobox.pack(pady=5)

        tk.Button(
            control_frame,
            text="削除",
            command=self.delete_selected_ingredient,
            font=("Arial", 12),
            bg="red",
            fg="white",
            relief="raised",
        ).pack(pady=5)

        # 戻るボタン
        tk.Button(
            control_frame,
            text="戻る",
            command=lambda: self.switch_frame(self.main_menu_frame),
        ).pack(pady=10)

    def update_ingredient_check(self, name, checked):
        """チェックボックスの状態を更新"""
        update_ingredient_check(self.ingredients, name, checked)

    # 献立を選択
    def select_recipe(self, recipe):
        """選択されたレシピを表示"""
        self.selected_recipe_label.config(text=f"選択されたレシピ: {recipe['title']}")

        # 履歴保存用データを準備
        history_entry = {
            "title": recipe["title"],
            "link": recipe["link"],
            "ingredients": recipe["used_ingredients"],
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        # ディレクトリ作成（なければ）
        DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/history.json")

        # 履歴ファイルに追記
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        else:
            history = []

        history.append(history_entry)

        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)

        # 通知
        messagebox.showinfo("保存完了", f"「{recipe['title']}」を履歴に記録しました。")

    def add_new_ingredient(self):
        """新しい食材を追加"""
        new_ingredient = self.new_ingredient_entry.get().strip()
        if new_ingredient:
            if add_ingredient(self.ingredients, new_ingredient):
                messagebox.showinfo("成功", f"「{new_ingredient}」を追加しました！")
                self.manage_ingredients()  # 画面をリロード
            else:
                messagebox.showwarning(
                    "警告", f"「{new_ingredient}」は既に存在します。"
                )
        else:
            messagebox.showwarning("警告", "食材名を入力してください。")

    def delete_selected_ingredient(self):
        """選択した食材を削除"""
        selected_ingredient = self.remove_ingredient_var.get()
        if selected_ingredient:
            if remove_ingredient(self.ingredients, selected_ingredient):
                messagebox.showinfo(
                    "成功", f"「{selected_ingredient}」を削除しました！"
                )
                self.manage_ingredients()  # 画面をリロード
            else:
                messagebox.showwarning(
                    "警告", f"「{selected_ingredient}」が見つかりません。"
                )
        else:
            messagebox.showwarning("警告", "削除する食材を選択してください。")

    def update_ingredients(self):
        """チェックボックスの状態に基づいて食材リストを更新"""
        self.ingredients = [
            {"name": name, "checked": var.get()}
            for name, var in self.ingredient_vars.items()
        ]
        save_ingredients(self.ingredients)

    def suggest_recipes(self):
        """献立提案画面"""
        self.switch_frame(self.suggestion_frame)

        tk.Label(self.suggestion_frame, text="献立提案", font=("Arial", 16)).pack(
            pady=10
        )

        # レシピ提案
        recipes = search_youtube_videos(self.ingredients)
        recipes = [recipe for recipe in recipes if recipe not in self.seen_recipes]

        if not recipes:
            messagebox.showinfo("情報", "再検索できる献立がありませんでした。")
            self.switch_frame(self.main_menu_frame)
            return

        self.seen_recipes.extend(recipes)

        # 選択されたレシピを保持するラベル
        self.selected_recipe_label = tk.Label(
            self.suggestion_frame, text="", fg="green"
        )
        self.selected_recipe_label.pack(pady=10)

        for idx, recipe in enumerate(recipes, 1):
            tk.Label(self.suggestion_frame, text=f"{idx}. {recipe['title']}").pack()
            # URLリンク（クリックで開く）
            link_label = tk.Label(
                self.suggestion_frame,
                text=recipe["link"],
                fg="blue",
                cursor="hand2",
                font=("Arial", 10, "underline"),
            )
            link_label.pack()
            # イベントバインドでリンクをクリック可能にする
            link_label.bind(
                "<Button-1>", lambda e, url=recipe["link"]: webbrowser.open(url)
            )

            # 選択ボタン
            tk.Button(
                self.suggestion_frame,
                text="この献立にする",
                command=lambda r=recipe: self.select_recipe(r),
            ).pack(pady=5)

        # 戻るボタン
        tk.Button(
            self.suggestion_frame,
            text="戻る",
            command=lambda: self.switch_frame(self.main_menu_frame),
        ).pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = MenuSuggestionApp(root)
    root.mainloop()
