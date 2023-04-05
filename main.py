import tkinter as tk
import tkinter.scrolledtext as tkst
import tkinter.messagebox
import tkinter.simpledialog
import random


class GameEditor:
    def __init__(self, master):
        self.master = master
        self.game_data = {}

        # 创建顶部菜单
        self.menu_bar = tk.Menu(master)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New", command=self.new_game)
        self.file_menu.add_command(label="Open...", command=self.open_game)
        self.file_menu.add_command(label="Save", command=self.save_game)
        self.file_menu.add_command(label="Save As...", command=self.save_game_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=master.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.run_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.run_menu.add_command(label="Run Scene", command=self.run_scene)
        self.menu_bar.add_cascade(label="Run", menu=self.run_menu)
        master.config(menu=self.menu_bar)

        # 创建编辑器界面
        self.text_box = tkst.ScrolledText(master, width=80, height=40)
        self.text_box.pack(expand=True, fill="both")

        # 创建编辑器工具栏
        self.tool_bar = tk.Frame(master)
        self.item_button = tk.Button(self.tool_bar, text="添加物品", command=self.add_item)
        self.item_button.pack(side="left", padx=2, pady=2)
        self.equipment_button = tk.Button(self.tool_bar, text="添加装备", command=self.add_equipment)
        self.equipment_button.pack(side="left", padx=2, pady=2)
        self.skill_button = tk.Button(self.tool_bar, text="添加技能", command=self.add_skill)
        self.skill_button.pack(side="left", padx=2, pady=2)
        self.character_button = tk.Button(self.tool_bar, text="添加角色", command=self.add_character)
        self.character_button.pack(side="left", padx=2, pady=2)
        self.scene_button = tk.Button(self.tool_bar, text="添加场景", command=self.add_scene)
        self.scene_button.pack(side="left", padx=2, pady=2)
        self.dialogue_button = tk.Button(self.tool_bar, text="添加对话", command=self.add_dialogue)
        self.dialogue_button.pack(side="left", padx=2, pady=2)
        self.battle_button = tk.Button(self.tool_bar, text="添加战斗", command=self.add_battle)
        self.battle_button.pack(side="left", padx=2, pady=2)
        self.end_button = tk.Button(self.tool_bar, text="添加结束", command=self.add_end)
        self.end_button.pack(side="left", padx=2, pady=2)
        self.tool_bar.pack(side="top", fill="x")

        # 创建战斗模式界面
        self.battle_frame = tk.Frame(master)
        self.attack_button = tk.Button(self.battle_frame, text="攻击", command=self.select_attack)
        self.attack_button.pack(side="left", padx=2, pady=2)
        self.skill_button = tk.Button(self.battle_frame, text="使用技能", command=self.select_skill)
        self.skill_button.pack(side="left", padx=2, pady=2)
        self.skip_button = tk.Button(self.battle_frame, text="跳过", command=self.skip_turn)
        self.skip_button.pack(side="left", padx=2, pady=2)
        self.battle_text = tkst.ScrolledText(self.battle_frame, width=40, height=20)
        self.battle_text.pack(side="left", padx=2, pady=2)
        self.battle_frame.pack(side="bottom", fill="x")

        # 解析游戏数据
        self.parse_game_data("")

    # 新建游戏
    def new_game(self):
        self.game_data = {}
        self.text_box.delete(1.0, tk.END)

    # 打开游戏
    def open_game(self):
        file_name = tk.filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_name:
            with open(file_name, "r") as file:
                data = file.read()
                self.text_box.delete(1.0, tk.END)
                self.text_box.insert(1.0, data)
                self.parse_game_data(data)

    # 保存游戏
    def save_game(self):
        if not self.game_data:
            tk.messagebox.showwarning("Warning", "No game data to save!")
            return

        if "file_name" not in self.game_data:
            self.save_game_as()
            return

        file_name = self.game_data["file_name"]
        with open(file_name, "w") as file:
            file.write(self.get_game_data())

    # 另存为
    def save_game_as(self):
        if not self.game_data:
            tk.messagebox.showwarning("Warning", "No game data to save!")
            return

        file_name = tk.filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_name:
            self.game_data["file_name"] = file_name
            with open(file_name, "w") as file:
                file.write(self.get_game_data())

    # 获取游戏数据的字符串表示
    def get_game_data(self):
        game_data = []
        for item in self.game_data.values():
            game_data.append(f"{item['type']}={item['name']}")
            for key, value in item.items():
                if key not in ["type", "name"]:
                    if key == "skills":
                        value = [skill["name"] for skill in value]
                        value = ", ".join(value)
                    elif key == "events":
                        event_lines = []
                        for event in value:
                            event_lines.append(event["type"])
                            for event_key, event_value in event.items():
                                if event_key != "type":
                                    event_lines.append(f"{event_key}={event_value}")
                            event_lines.append("")
                        value = "\n".join(event_lines)
                    game_data.append(f"{key}={value}")
            game_data.append("")
        return "\n".join(game_data)

     # 添加物品
    def add_item(self):
        name = tk.simpledialog.askstring("Item", "请输入物品名称：", parent=self.master)
        if name:
            if name in self.game_data:
                tk.messagebox.showwarning("Warning", "该名称已被使用！")
                return

            item_data = {"type": "ITEM", "name": name, "description": "", "value": 0}
            self.game_data[name] = item_data
            self.text_box.insert(tk.END, f"\n# 物品：{name}\n")
            self.edit_item(item_data)

    # 编辑物品
    def edit_item(self, item_data):
        window = tk.Toplevel(self.master)
        window.title(f"编辑物品：{item_data['name']}")
        name_label = tk.Label(window, text="名称：")
        name_label.grid(row=0, column=0)
        name_entry = tk.Entry(window, width=40)
        name_entry.grid(row=0, column=1)
        name_entry.insert(0, item_data["name"])
        description_label = tk.Label(window, text="描述：")
        description_label.grid(row=1, column=0)
        description_text = tk.Text(window, width=40, height=5)
        description_text.grid(row=1, column=1)
        description_text.insert(1.0, item_data["description"])
        value_label = tk.Label(window, text="价值：")
        value_label.grid(row=2, column=0)
        value_entry = tk.Entry(window, width=10)
        value_entry.grid(row=2, column=1)
        value_entry.insert(0, item_data["value"])
        button_frame = tk.Frame(window)
        button_frame.grid(row=3, column=0, columnspan=2)
        ok_button = tk.Button(button_frame, text="确定", command=lambda: self.save_item(item_data, name_entry.get(),
                                                                                          description_text.get(1.0, tk.END),
                                                                                          value_entry.get()))
        ok_button.pack(side="left", padx=2, pady=2)
        cancel_button = tk.Button(button_frame, text="取消", command=window.destroy)
        cancel_button.pack(side="left", padx=2, pady=2)

    # 保存物品
    def save_item(self, item_data, name, description, value):
        if name == "":
            tk.messagebox.showwarning("Warning", "名称不能为空！")
            return

        if name != item_data["name"] and name in self.game_data:
            tk.messagebox.showwarning("Warning", "该名称已被使用！")
            return

        item_data["name"] = name
        item_data["description"] = description
        item_data["value"] = int(value)
        self.text_box.insert(tk.END, f"名称={name}\n描述={description}\n价值={value}\n\n")

    # 添加装备
    def add_equipment(self):
        name = tk.simpledialog.askstring("Equipment", "请输入装备名称：", parent=self.master)
        if name:
            if name in self.game_data:
                tk.messagebox.showwarning("Warning", "该名称已被使用！")
                return

            equipment_data = {"type": "EQUIPMENT", "name": name, "description": "", "value": 0,
                              "strength": 0, "agility": 0, "intelligence": 0, "defense": 0}
            self.game_data[name] = equipment_data
            self.text_box.insert(tk.END, f"\n# 装备：{name}\n")
            self.edit_equipment(equipment_data)
    # 保存装备
    def save_equipment(self, equipment_data, name, description, value, strength, agility, intelligence, defense):
        if name == "":
            tk.messagebox.showwarning("Warning", "名称不能为空！")
            return

        if name != equipment_data["name"] and name in self.game_data:
            tk.messagebox.showwarning("Warning", "该名称已被使用！")
            return

        equipment_data["name"] = name
        equipment_data["description"] = description
        equipment_data["value"] = int(value)
        equipment_data["strength"] = int(strength)
        equipment_data["agility"] = int(agility)
        equipment_data["intelligence"] = int(intelligence)
        equipment_data["defense"] = int(defense)

        self.text_box.delete(f"{equipment_data['name']}.0", f"{equipment_data['name']}.end")
        self.text_box.insert(tk.END, f"\n# 装备：{name}\n")
        self.text_box.insert(tk.END, f"name = '{name}'\n")
        self.text_box.insert(tk.END, f"description = '''{description}'''\n")
        self.text_box.insert(tk.END, f"value = {value}\n")
        self.text_box.insert(tk.END, f"strength = {strength}\n")
        self.text_box.insert(tk.END, f"agility = {agility}\n")
        self.text_box.insert(tk.END, f"intelligence = {intelligence}\n")
        self.text_box.insert(tk.END, f"defense = {defense}\n")

    # 添加技能
    def add_skill(self):
        name = tk.simpledialog.askstring("Skill", "请输入技能名称：", parent=self.master)
        if name:
            if name in self.game_data:
                tk.messagebox.showwarning("Warning", "该名称已被使用！")
                return

            skill_data = {"type": "SKILL", "name": name, "description": "", "mp_cost": 0,
                          "damage": 0, "heal": 0, "target_type": "ENEMY"}
            self.game_data[name] = skill_data
            self.text_box.insert(tk.END, f"\n# 技能：{name}\n")
            self.edit_skill(skill_data)

    # 编辑技能
    def edit_skill(self, skill_data):
        window = tk.Toplevel(self.master)
        window.title(f"编辑技能：{skill_data['name']}")
        name_label = tk.Label(window, text="名称：")
        name_label.grid(row=0, column=0)
        name_entry = tk.Entry(window, width=40)
        name_entry.grid(row=0, column=1)
        name_entry.insert(0, skill_data["name"])
        description_label = tk.Label(window, text="描述：")
        description_label.grid(row=1, column=0)
        description_text = tk.Text(window, width=40, height=5)
        description_text.grid(row=1, column=1)
        description_text.insert(1.0, skill_data["description"])
        mp_cost_label = tk.Label(window, text="消耗法力：")
        mp_cost_label.grid(row=2, column=0)
        mp_cost_entry = tk.Entry(window, width=10)
        mp_cost_entry.grid(row=2, column=1)
        mp_cost_entry.insert(0, skill_data["mp_cost"])
        damage_label = tk.Label(window, text="伤害：")
        damage_label.grid(row=3, column=0)
        damage_entry = tk.Entry(window, width=10)
        damage_entry.grid(row=3, column=1)
        damage_entry.insert(0, skill_data["damage"])
        heal_label = tk.Label(window, text="恢复：")
        heal_label.grid(row=4, column=0)
        heal_entry = tk.Entry(window, width=10)
        heal_entry.grid(row=4, column=1)
        heal_entry.insert(0, skill_data["heal"])
        target_type_label = tk.Label(window, text="目标类型：")
        target_type_label.grid(row=5, column=0)
        target_type_combobox = ttk.Combobox(window, values=["ENEMY", "ALLY", "SELF"])
        target_type_combobox.grid(row=5, column=1)
        target_type_combobox.current(["ENEMY", "ALLY", "SELF"].index(skill_data["target_type"]))
        button_frame = tk.Frame(window)
        button_frame.grid(row=6, column=0, columnspan=2)
        ok_button = tk.Button(button_frame, text="确定", command=lambda: self.save_skill(skill_data,
                                                                                          name_entry.get(),
                                                                                          description_text.get(1.0, tk.END),
                                                                                          mp_cost_entry.get(),
                                                                                          damage_entry.get(),
                                                                                          heal_entry.get(),
                                                                                          target_type_combobox.get()))
        ok_button.pack(side="left", padx=2, pady=2)
        cancel_button = tk.Button(button_frame, text="取消", command=window.destroy)
        cancel_button.pack(side="left", padx=2, pady=2)

    # 保存技能
    def save_skill(self, skill_data, name, description, mp_cost, damage, heal, target_type):
        if name == "":
            tk.messagebox.showwarning("Warning", "名称不能为空！")
            return

        if name != skill_data["name"] and name in self.game_data:
            tk.messagebox.showwarning("Warning", "该名称已被使用！")
            return

        skill_data["name"] = name
        skill_data["description"] = description
        skill_data["mp_cost"] = int(mp_cost)
        skill_data["damage"] = int(damage)
        skill_data["heal"] = int(heal)
        skill_data["target_type"] = target_type

        self.text_box.delete(f"{skill_data['name']}.0", f"{skill_data['name']}.end")
        self.text_box.insert(tk.END, f"\n# 技能：{name}\n")
        self.text_box.insert(tk.END, f"name = '{name}'\n")
        self.text_box.insert(tk.END, f"description = '''{description}'''\n")
        self.text_box.insert(tk.END, f"mp_cost = {mp_cost}\n")
        self.text_box.insert(tk.END, f"damage = {damage}\n")
        self.text_box.insert(tk.END, f"heal = {heal}\n")
        self.text_box.insert(tk.END, f"target_type = '{target_type}'\n")

    # 创建角色
    def create_character(self):
        window = tk.Toplevel(self.master)
        window.title("创建角色")
        name_label = tk.Label(window, text="名称：")
        name_label.grid(row=0, column=0)
        name_entry = tk.Entry(window, width=40)
        name_entry.grid(row=0, column=1)
        description_label = tk.Label(window, text="描述：")
        description_label.grid(row=1, column=0)
        description_text = tk.Text(window, width=40, height=5)
        description_text.grid(row=1, column=1)
        hp_label = tk.Label(window, text="生命值：")
        hp_label.grid(row=2, column=0)
        hp_entry = tk.Entry(window, width=10)
        hp_entry.grid(row=2, column=1)
        mp_label = tk.Label(window, text="法力：")
        mp_label.grid(row=3, column=0)
        mp_entry = tk.Entry(window, width=10)
        mp_entry.grid(row=3, column=1)
        attack_label = tk.Label(window, text="攻击力：")
        attack_label.grid(row=4, column=0)
        attack_entry = tk.Entry(window, width=10)
        attack_entry.grid(row=4, column=1)
        defense_label = tk.Label(window, text="防御力：")
        defense_label.grid(row=5, column=0)
        defense_entry = tk.Entry(window, width=10)
        defense_entry.grid(row=5, column=1)
        realm_label = tk.Label(window, text="境界：")
        realm_label.grid(row=6, column=0)
        realm_entry = tk.Entry(window, width=40)
        realm_entry.grid(row=6, column=1)
        skills_label = tk.Label(window, text="技能：")
        skills_label.grid(row=7, column=0)
        skills_listbox = tk.Listbox(window, height=5, selectmode=tk.MULTIPLE)
        skills_listbox.grid(row=7, column=1)

        for skill_name in self.game_data:
            if self.game_data[skill_name]["type"] == "SKILL":
                skills_listbox.insert(tk.END, skill_name)

        button_frame = tk.Frame(window)
        button_frame.grid(row=8, column=0, columnspan=2)
        ok_button = tk.Button(button_frame, text="确定", command=lambda: self.save_character(name_entry.get(),
                                                                                             description_text.get(1.0, tk.END),
                                                                                             hp_entry.get(),
                                                                                             mp_entry.get(),
                                                                                             attack_entry.get(),
                                                                                             defense_entry.get(),
                                                                                             realm_entry.get(),
                                                                                             skills_listbox.curselection()))
        ok_button.pack(side="left", padx=2, pady=2)
        cancel_button = tk.Button(button_frame, text="取消", command=window.destroy)
        cancel_button.pack(side="left", padx=2, pady=2)

    # 保存角色
    def save_character(self, name, description, hp, mp, attack, defense, realm, selected_skills):
        if name == "":
            tk.messagebox.showwarning("Warning", "名称不能为空！")
            return

        if name in self.game_data:
            tk.messagebox.showwarning("Warning", "该名称已被使用！")
            return

        character_data = {"type": "CHARACTER", "name": name, "description": description,
                          "max_hp": int(hp), "max_mp": int(mp), "attack": int(attack),
                          "defense": int(defense), "realm": realm, "skills": []}

        for i in selected_skills:
            skill_name = self.game_data[skills_listbox.get(i)]["name"]
            character_data["skills"].append(skill_name)

        self.game_data[name] = character_data

        self.text_box.delete(f"{name}.0", f"{name}.end")
        self.text_box.insert(tk.END, f"\n# 角色：{name}\n")
        self.text_box.insert(tk.END, f"name = '{name}'\n")
        self.text_box.insert(tk.END, f"description = '''{description}'''\n")
        self.text_box.insert(tk.END, f"max_hp = {hp}\n")
        self.text_box.insert(tk.END, f"max_mp = {mp}\n")
        self.text_box.insert(tk.END, f"attack = {attack}\n")
        self.text_box.insert(tk.END, f"defense = {defense}\n")
        self.text_box.insert(tk.END, f"realm = '{realm}'\n")
        self.text_box.insert(tk.END, f"skills = [")
        for skill_name in character_data["skills"]:
            self.text_box.insert(tk.END, f"'{skill_name}', ")
        self.text_box.insert(tk.END, f"]\n")

        tk.messagebox.showinfo("Info", "角色已创建！")

    # 创建战斗模式界面
    def create_battle_mode(self):
        window = tk.Toplevel(self.master)
        window.title("创建战斗模式")
        name_label = tk.Label(window, text="名称：")
        name_label.grid(row=0, column=0)
        name_entry = tk.Entry(window, width=40)
        name_entry.grid(row=0, column=1)
        description_label = tk.Label(window, text="描述：")
        description_label.grid(row=1, column=0)
        description_text = tk.Text(window, width=40, height=5)
        description_text.grid(row=1, column=1)
        enemy_list_label = tk.Label(window, text="敌人列表：")
        enemy_list_label.grid(row=2, column=0)
        enemy_list_text = tk.Text(window, width=40, height=5)
        enemy_list_text.grid(row=2, column=1)
        battle_music_label = tk.Label(window, text="战斗音乐：")
        battle_music_label.grid(row=3, column=0)
        battle_music_entry = tk.Entry(window, width=40)
        battle_music_entry.grid(row=3, column=1)
        button_frame = tk.Frame(window)
        button_frame.grid(row=4, column=0, columnspan=2)
        ok_button = tk.Button(button_frame, text="确定", command=lambda: self.save_battle_mode(name_entry.get(),
                                                                                               description_text.get(1.0, tk.END),
                                                                                               enemy_list_text.get(1.0, tk.END),
                                                                                               battle_music_entry.get()))
        ok_button.pack(side="left", padx=2, pady=2)
        cancel_button = tk.Button(button_frame, text="取消", command=window.destroy)
        cancel_button.pack(side="left", padx=2, pady=2)
        
  # 保存战斗模式
    def save_battle_mode(self, name, description, enemy_list, battle_music):
        if name == "":
            tk.messagebox.showwarning("Warning", "名称不能为空！")
            return

        if name in self.game_data:
            tk.messagebox.showwarning("Warning", "该名称已被使用！")
            return
        battle_mode_data = {"type": "BATTLE_MODE", "name": name, "description": description,
                            "enemy_list": enemy_list, "battle_music": battle_music}

        self.game_data[name] = battle_mode_data
        self.text_box.delete(f"{name}.0", f"{name}.end")
        self.text_box.insert(tk.END, f"\n# 战斗模式：{name}\n")
        self.text_box.insert(tk.END, f"name = '{name}'\n")
        self.text_box.insert(tk.END, f"description = '''{description}'''\n")
        self.text_box.insert(tk.END, f"enemy_list = '''{enemy_list}'''\n")
        self.text_box.insert(tk.END, f"battle_music = '{battle_music}'\n")

        tk.messagebox.showinfo("Info", "战斗模式已创建！")

    # 创建事件
    def create_event(self):
        window = tk.Toplevel(self.master)
        window.title("创建事件")
        name_label = tk.Label(window, text="名称：")
        name_label.grid(row=0, column=0)
        name_entry = tk.Entry(window, width=40)
        name_entry.grid(row=0, column=1)
        description_label = tk.Label(window, text="描述：")
        description_label.grid(row=1, column=0)
        description_text = tk.Text(window, width=40, height=5)
        description_text.grid(row=1, column=1)
        event_type_label = tk.Label(window, text="事件类型：")
        event_type_label.grid(row=2, column=0)
        event_type_combobox = ttk.Combobox(window, values=["对话", "战斗"])
        event_type_combobox.grid(row=2, column=1)
        event_type_combobox.current(0)
        if self.selected_object_type == "CHARACTER":
            target_label = tk.Label(window, text="目标角色：")
            target_label.grid(row=3, column=0)
            target_combobox = ttk.Combobox(window, values=list(self.game_data.keys()))
            target_combobox.grid(row=3, column=1)
            target_combobox.current(0)
        else:
            target_label = tk.Label(window, text="目标场景：")
            target_label.grid(row=3, column=0)
            target_combobox = ttk.Combobox(window, values=list(self.game_data.keys()))
            target_combobox.grid(row=3, column=1)
            target_combobox.current(0)
        button_frame = tk.Frame(window)
        button_frame.grid(row=4, column=0, columnspan=2)
        ok_button = tk.Button(button_frame, text="确定", command=lambda: self.save_event(name_entry.get(),
                                                                                           description_text.get(1.0, tk.END),
                                                                                           event_type_combobox.get(),
                                                                                           target_combobox.get()))
        ok_button.pack(side="left", padx=2, pady=2)
        cancel_button = tk.Button(button_frame, text="取消", command=window.destroy)
        cancel_button.pack(side="left", padx=2, pady=2)

    # 保存事件
    def save_event(self, name, description, event_type, target):
        if name == "":
            tk.messagebox.showwarning("Warning", "名称不能为空！")
            return

        if name in self.game_data:
            tk.messagebox.showwarning("Warning", "该名称已被使用！")
            return

        event_data = {"type": "EVENT", "name": name, "description": description,
                      "event_type": event_type, "target": target}

        self.game_data[name] = event_data
        self.text_box.delete(f"{name}.0", f"{name}.end")
        self.text_box.insert(tk.END, f"\n# 事件：{name}\n")
        self.text_box.insert(tk.END, f"name = '{name}'\n")
        self.text_box.insert(tk.END, f"description = '''{description}'''\n")
        self.text_box.insert(tk.END, f"event_type = '{event_type}'\n")
        self.text_box.insert(tk.END, f"target = '{target}'\n")

        tk.messagebox.showinfo("Info", "事件已创建！")

    # 测试游戏
    def test_game(self):
        game_text = self.text_box.get(1.0, tk.END)
        exec(game_text)

    # 创建菜单
    def create_menu(self):
        menu_bar = tk.Menu(self.master)
        self.master.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="保存", command=self.save_game_data)
        file_menu.add_command(label="读取", command=self.load_game_data)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.master.quit)

        edit_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="编辑", menu=edit_menu)
        edit_menu.add_command(label="创建场景", command=self.create_scene)
        edit_menu.add_command(label="创建角色", command=self.create_character)
        edit_menu.add_command(label="创建物品", command=self.add_item)
        edit_menu.add_command(label="创建装备", command=self.add_equipment)
        edit_menu.add_command(label="创建技能", command=self.add_skill)
        edit_menu.add_command(label="创建战斗模式", command=self.create_battle_mode)
        edit_menu.add_command(label="创建事件", command=self.create_event)

        run_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="运行", menu=run_menu)
        run_menu.add_command(label="测试游戏", command=self.test_game)

    # 加载游戏数据
    def load_game_data(self):
        file_path = filedialog.askopenfilename()
        if file_path == "":
            return

        with open(file_path, "r") as f:
            self.game_data = json.load(f)

        self.text_box.delete("1.0", "end")
        for obj_name in self.game_data:
            obj_type = self.game_data[obj_name]["type"]
            if obj_type == "SCENE":
                self.text_box.insert(tk.END, f"\n# 场景：{obj_name}\n")
                self.text_box.insert(tk.END, f"name = '{obj_name}'\n")
                self.text_box.insert(tk.END, f"description = '''{self.game_data[obj_name]['description']}'''\n")
                self.text_box.insert(tk.END, f"background_music = '{self.game_data[obj_name]['background_music']}'\n")
                self.text_box.insert(tk.END, f"objects = []\n")
            elif obj_type == "CHARACTER":
                self.text_box.insert(tk.END, f"\n# 角色：{obj_name}\n")
                self.text_box.insert(tk.END, f"name = '{obj_name}'\n")
                self.text_box.insert(tk.END, f"hp = {self.game_data[obj_name]['hp']}\n")
                self.text_box.insert(tk.END, f"mp = {self.game_data[obj_name]['mp']}\n")
                self.text_box.insert(tk.END, f"attack = {self.game_data[obj_name]['attack']}\n")
                self.text_box.insert(tk.END, f"defense = {self.game_data[obj_name]['defense']}\n")
                self.text_box.insert(tk.END, f"realm = '{self.game_data[obj_name]['realm']}'\n")
                self.text_box.insert(tk.END, f"skills = []\n")
            elif obj_type == "ITEM":
                self.text_box.insert(tk.END, f"\n# 物品：{obj_name}\n")
                self.text_box.insert(tk.END, f"name = '{obj_name}'\n")
                self.text_box.insert(tk.END, f"description = '''{self.game_data[obj_name]['description']}'''\n")
            elif obj_type == "EQUIPMENT":
                self.text_box.insert(tk.END, f"\n# 装备：{obj_name}\n")
                self.text_box.insert(tk.END, f"name = '{obj_name}'\n")
                self.text_box.insert(tk.END, f"description = '''{self.game_data[obj_name]['description']}'''\n")
                self.text_box.insert(tk.END, f"equip_type = '{self.game_data[obj_name]['equip_type']}'\n")
                self.text_box.insert(tk.END, f"attack_bonus = {self.game_data[obj_name]['attack_bonus']}\n")
                self.text_box.insert(tk.END, f"defense_bonus = {self.game_data[obj_name]['defense_bonus']}\n")
            elif obj_type == "SKILL":
                self.text_box.insert(tk.END, f"\n# 技能：{obj_name}\n")
                self.text_box.insert(tk.END, f"name = '{obj_name}'\n")
                self.text_box.insert(tk.END, f"description = '''{self.game_data[obj_name]['description']}'''\n")
                self.text_box.insert(tk.END, f"mp_cost = {self.game_data[obj_name]['mp_cost']}\n")
                self.text_box.insert(tk.END, f"power = {self.game_data[obj_name]['power']}\n")
                self.text_box.insert(tk.END, f"type = '{self.game_data[obj_name]['type']}'\n")
            elif obj_type == "BATTLE_MODE":
                self.text_box.insert(tk.END, f"\n# 战斗模式：{obj_name}\n")
                self.text_box.insert(tk.END, f"name = '{obj_name}'\n")
                self.text_box.insert(tk.END, f"description = '''{self.game_data[obj_name]['description']}'''\n")
                self.text_box.insert(tk.END, f"enemy_list = '''{self.game_data[obj_name]['enemy_list']}'''\n")
                self.text_box.insert(tk.END, f"battle_music = '{self.game_data[obj_name]['battle_music']}'\n")
        tk.messagebox.showinfo("Info", "游戏数据已加载！")

    # 保存游戏数据
    def save_game_data(self):
        file_path = filedialog.asksaveasfilename()
        if file_path == "":
            return

        with open(file_path, "w") as f:
            json.dump(self.game_data, f, indent=4)

        tk.messagebox.showinfo("Info", "游戏数据已保存！")
     
    def run_scene(self):
        pass
    def add_character(self):
        pass
if __name__ == "__main__":
    root = tk.Tk()
    editor = GameEditor(root)
    root.mainloop()
