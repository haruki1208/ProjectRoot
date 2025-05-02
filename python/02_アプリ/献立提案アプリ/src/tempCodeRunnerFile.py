       # # チェックボックスを表示
        # self.ingredient_vars = {}
        # for ingredient in self.ingredients:
        #     var = tk.BooleanVar(value=ingredient["checked"])  # JSONのチェック状態を反映
        #     self.ingredient_vars[ingredient["name"]] = var
        #     tk.Checkbutton(
        #         self.ingredients_frame,
        #         text=ingredient["name"],
        #         variable=var,
        #         command=lambda name=ingredient[
        #             "name"
        #         ], var=var: self.update_ingredient_check(name, var.get()),
        #     ).pack(anchor="w")