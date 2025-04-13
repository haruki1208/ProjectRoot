from tkinter import Tk, Label, Button, Entry, Listbox, StringVar, END, messagebox

class GUIView:
    def __init__(self, master):
        self.master = master
        master.title("献立提案アプリ")

        self.label = Label(master, text="食材を追加:")
        self.label.pack()

        self.ingredient_entry = Entry(master)
        self.ingredient_entry.pack()

        self.add_button = Button(master, text="追加", command=self.add_ingredient)
        self.add_button.pack()

        self.ingredient_listbox = Listbox(master)
        self.ingredient_listbox.pack()

        self.suggest_button = Button(master, text="メニュー提案", command=self.suggest_menu)
        self.suggest_button.pack()

        self.suggestion_label = Label(master, text="")
        self.suggestion_label.pack()

        self.ingredients = []

    def add_ingredient(self):
        ingredient = self.ingredient_entry.get()
        if ingredient:
            self.ingredients.append(ingredient)
            self.ingredient_listbox.insert(END, ingredient)
            self.ingredient_entry.delete(0, END)
        else:
            messagebox.showwarning("警告", "食材を入力してください。")

    def suggest_menu(self):
        if not self.ingredients:
            messagebox.showwarning("警告", "食材がありません。")
            return
        
        # ここでメニュー提案のロジックを実装する
        suggested_menu = "オススメメニュー: " + ", ".join(self.ingredients)  # 仮の提案
        self.suggestion_label.config(text=suggested_menu)

def main():
    root = Tk()
    gui_view = GUIView(root)
    root.mainloop()

if __name__ == "__main__":
    main()