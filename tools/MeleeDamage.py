"""
Portable Calculator Suite - Main Hub
Copyright (C) 2026 [Your Name]

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

import tkinter as tk
from tkinter import messagebox
import random

# Data from RangedHitx.py
MONSTER_ARMOR_CLASSES = {
    "Aarakocra": 12, "Acolyte": 10, "Axe Beak": 11, "Blink Dog": 13, "Boar": 11,
    "Bullywug": 11, "Constrictor Snake": 12, "Draft Horse": 10, "Dretch": 11,
    "Drow": 15, "Duodrone": 14, "Elk": 10, "Flying Sword": 17, "Giant Badger": 10,
    "Giant Bat": 13, "Giant Centipede": 13, "Giant Frog": 11, "Giant Lizard": 12,
    "Giant Owl": 12, "Giant Poisonous Snake": 14, "Giant Wolf Spider": 13,
    "Goblin": 15, "Grimlock": 11, "Kenku": 13, "Kuo-toa": 13, "Mud Mephit": 11,
    "Needle Blight": 12, "Panther": 12, "Pixie": 15, "Pseudodragon": 13,
    "Pteranodon": 13, "Riding Horse": 10, "Skeleton": 13, "Smoke Mephit": 12,
    "Sprite": 15, "Steam Mephit": 10, "Swarm of Bats": 12, "Swarm of Rats": 10,
    "Swarm of Ravens": 12, "Troglodyte": 11, "Violet Fungus": 5, "Winged Kobold": 12,
    "Wolf": 13, "Zombie": 8
}

WEAPONS = {
    "Club (1d4)": (1, 4), "Dagger (1d4)": (1, 4), "Greatclub (1d8)": (1, 8),
    "Handaxe (1d6)": (1, 6), "Javelin (1d6)": (1, 6), "Light hammer (1d4)": (1, 4),
    "Mace (1d6)": (1, 6), "Quarterstaff (1d6)": (1, 6), "Sickle (1d4)": (1, 4),
    "Spear (1d6)": (1, 6), "Battleaxe (1d8)": (1, 8), "Flail (1d8)": (1, 8),
    "Glaive (1d10)": (1, 10), "Greataxe (1d12)": (1, 12), "Greatsword (2d6)": (2, 12),
    "Halberd (1d10)": (1, 10), "Lance (1d12)": (1, 12), "Longsword (1d8)": (1, 8),
    "Maul (2d6)": (2, 12), "Morningstar (1d8)": (1, 8), "Pike (1d10)": (1, 10),
    "Rapier (1d8)": (1, 8), "Scimitar (1d6)": (1, 6), "Shortsword (1d6)": (1, 6),
    "Trident (1d6)": (1, 6), "War pick (1d8)": (1, 8), "Warhammer (1d8)": (1, 8),
    "Whip (1d4)": (1, 4)
}

WEAPON_COLORS = {
    "Dagger (1d4)": "#e1f5fe", "Rapier (1d8)": "#e1f5fe", "Scimitar (1d6)": "#e1f5fe",
    "Shortsword (1d6)": "#e1f5fe", "Whip (1d4)": "#e1f5fe",
    "Quarterstaff (1d6)": "#e8f5e9", "Spear (1d6)": "#e8f5e9", "Battleaxe (1d8)": "#e8f5e9",
    "Longsword (1d8)": "#e8f5e9", "Trident (1d6)": "#e8f5e9", "Warhammer (1d8)": "#e8f5e9",
    "Glaive (1d10)": "#fff3e0", "Greataxe (1d12)": "#fff3e0", "Greatsword (2d6)": "#fff3e0",
    "Halberd (1d10)": "#fff3e0", "Maul (2d6)": "#fff3e0", "Pike (1d10)": "#fff3e0"
}

monster_vars = {}
weapon_vars = {}
range_vars = {}


def single_select_weapon(selected_name):
    for name, var in weapon_vars.items():
        if name != selected_name:
            var.set(False)


def single_select_monster(selected_name):
    for name, var in monster_vars.items():
        if name != selected_name:
            var.set(False)
    manual_ac_entry.delete(0, tk.END)


def single_select_range(selected_increment):
    for increment, var in range_vars.items():
        if increment != selected_increment:
            var.set(False)


def reset_all():
    for var in weapon_vars.values():
        var.set(False)
    for var in monster_vars.values():
        var.set(False)
    for var in range_vars.values():
        var.set(False)
    thrown_var.set(False)
    range_vars["Short"].set(True)
    ability_score_entry.delete(0, tk.END)
    ability_score_entry.insert(0, "10")
    proficiency_bonus_entry.delete(0, tk.END)
    proficiency_bonus_entry.insert(0, "2")
    manual_ac_entry.delete(0, tk.END)
    attack_roll_label.config(text="Attack Roll: --")
    result_label.config(text="Result: --", fg="black")


def calculate_attack_and_damage():
    try:
        ability_score = int(ability_score_entry.get() or 10)
        proficiency = int(proficiency_bonus_entry.get() or 0)
        ability_mod = (ability_score - 10) // 2

        range_penalty = 0
        # Only calculate range if Thrown is checked
        if thrown_var.get():
            if range_vars["Medium"].get():
                range_penalty = -2
            if range_vars["Long"].get():
                range_penalty = -4

        target_ac = get_selected_armor_class()
        weapon_name = get_selected_weapon()

        if not weapon_name:
            messagebox.showerror("Error", "Please select a weapon.")
            return

        d20_roll = random.randint(1, 20)
        attack_total = d20_roll + ability_mod + proficiency + range_penalty

        if d20_roll == 20:
            low, high = WEAPONS[weapon_name]
            dmg = random.randint(low, high) + ability_mod
            result = f"CRIT! Hit for {dmg} damage!"
            color = "green"
        elif d20_roll == 1:
            result = f"NAT 1! Complete miss."
            color = "red"
        elif attack_total >= target_ac:
            low, high = WEAPONS[weapon_name]
            dmg = random.randint(low, high) + ability_mod
            result = f"HIT! ({attack_total} vs AC {target_ac}) for {dmg} damage."
            color = "blue"
        else:
            result = f"MISS! ({attack_total} vs AC {target_ac})"
            color = "black"

        result_label.config(text=result, fg=color)
        penalty_text = f" (Penalty: {range_penalty})" if thrown_var.get(
        ) else ""
        attack_roll_label.config(
            text=f"Total Attack Roll: {attack_total}{penalty_text}")

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers.")


def get_selected_armor_class():
    for monster, var in monster_vars.items():
        if var.get():
            return MONSTER_ARMOR_CLASSES[monster]
    return int(manual_ac_entry.get() or 10)


def get_selected_weapon():
    for weapon, var in weapon_vars.items():
        if var.get():
            return weapon
    return None


root = tk.Tk()
root.title("Melee & Thrown Attack Calculator")

# Stats Frame
stats_frame = tk.LabelFrame(root, text=" Character Stats ", padx=10, pady=5)
stats_frame.pack(pady=5, fill="x", padx=10)

tk.Label(stats_frame, text="Ability Score:").grid(row=0, column=0, padx=5)
ability_score_entry = tk.Entry(stats_frame, width=5)
ability_score_entry.insert(0, "10")
ability_score_entry.grid(row=0, column=1, padx=5)

tk.Label(stats_frame, text="Proficiency:").grid(row=0, column=2, padx=5)
proficiency_bonus_entry = tk.Entry(stats_frame, width=5)
proficiency_bonus_entry.insert(0, "2")
proficiency_bonus_entry.grid(row=0, column=3, padx=5)

# Range Frame with Thrown Toggle
range_frame = tk.LabelFrame(
    root, text=" Combat Mode & Range ", padx=10, pady=5)
range_frame.pack(pady=5, fill="x", padx=10)

thrown_var = tk.BooleanVar()
tk.Checkbutton(range_frame, text="Is Thrown Attack?", variable=thrown_var, font=(
    "Calibri", 9, "bold")).grid(row=0, column=0, padx=10)

increments = ["Short", "Medium", "Long"]
for i, inc in enumerate(increments):
    var = tk.BooleanVar()
    if inc == "Short":
        var.set(True)
    range_vars[inc] = var
    cb = tk.Checkbutton(range_frame, text=f"{inc}", variable=var,
                        command=lambda r=inc: single_select_range(r))
    cb.grid(row=0, column=i+1, padx=10)

# 5-Column Weapon Grid
MAX_COLS = 5
weapon_frame = tk.LabelFrame(root, text=" Select Weapon ", padx=10, pady=5)
weapon_frame.pack(padx=10, pady=5, fill="x")

for i, weapon in enumerate(WEAPONS):
    var = tk.BooleanVar()
    weapon_vars[weapon] = var
    bg_color = WEAPON_COLORS.get(weapon, "#f5f5f5")
    cb = tk.Checkbutton(weapon_frame, text=weapon, variable=var, bg=bg_color,
                        command=lambda w=weapon: single_select_weapon(w))
    cb.grid(row=i//MAX_COLS, column=i % MAX_COLS, sticky="w", padx=2, pady=2)

# Legend Section to explain color-coding
legend_frame = tk.Frame(weapon_frame)
legend_frame.grid(row=(len(WEAPONS)//MAX_COLS)+1, column=0,
                  columnspan=MAX_COLS, pady=5, sticky="w")

tk.Label(legend_frame, text="Legend:", font=(
    "Arial", 8, "bold")).pack(side="left", padx=5)
tk.Label(legend_frame, text=" Finesse ", bg="#e1f5fe",
         relief="ridge", font=("Arial", 8)).pack(side="left", padx=2)
tk.Label(legend_frame, text=" Versatile ", bg="#e8f5e9",
         relief="ridge", font=("Arial", 8)).pack(side="left", padx=2)
tk.Label(legend_frame, text=" Heavy ", bg="#fff3e0", relief="ridge",
         font=("Arial", 8)).pack(side="left", padx=2)

# 5-Column Monster Grid
monster_frame = tk.LabelFrame(
    root, text=" Select Target Monster ", padx=10, pady=5)
monster_frame.pack(padx=10, pady=5, fill="x")

for i, (monster, ac) in enumerate(MONSTER_ARMOR_CLASSES.items()):
    var = tk.BooleanVar()
    monster_vars[monster] = var
    cb = tk.Checkbutton(monster_frame, text=f"{monster} ({ac})", variable=var,
                        command=lambda m=monster: single_select_monster(m))
    cb.grid(row=i//MAX_COLS, column=i % MAX_COLS, sticky="w")

# Footer Controls
action_frame = tk.Frame(root)
action_frame.pack(pady=5)

tk.Label(action_frame, text="Or Manual AC:").grid(row=0, column=0, padx=5)
manual_ac_entry = tk.Entry(action_frame, width=5)
manual_ac_entry.grid(row=0, column=1, padx=5)

calculate_button = tk.Button(action_frame, text="Execute Attack",
                             command=calculate_attack_and_damage, bg="#d1ffd1", font=("Calibri", 10, "bold"))
calculate_button.grid(row=0, column=2, padx=10)

reset_button = tk.Button(action_frame, text="Reset All",
                         command=reset_all, bg="#ffcccc")
reset_button.grid(row=0, column=3, padx=10)

attack_roll_label = tk.Label(root, text="Attack Roll: --")
attack_roll_label.pack()

result_label = tk.Label(root, text="Result: --", font=("Calibri", 13, "bold"))
result_label.pack(pady=5)

root.mainloop()
