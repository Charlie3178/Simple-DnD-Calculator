import tkinter as tk
from tkinter import messagebox
import random

# Monster AC Data
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

# Proper Ranged Weapon Data
WEAPONS = {
    "Blowgun (1)": (1, 1), "Dart (1d4)": (1, 4), "Hand Xbow (1d6)": (1, 6),
    "Heavy Xbow (1d10)": (1, 10), "Light Xbow (1d8)": (1, 8), "Longbow (1d8)": (1, 8),
    "Net (-)": (0, 0), "Shortbow (1d6)": (1, 6), "Sling (1d4)": (1, 4),
    "Dagger (1d4)*": (1, 4), "Handaxe (1d6)*": (1, 6), "Javelin (1d6)*": (1, 6),
    "Light Hammer (1d4)*": (1, 4), "Spear (1d6)*": (1, 6), "Trident (1d6)*": (1, 6)
}

# Blue = Ammunition, Green = Thrown, Grey = Standard
WEAPON_COLORS = {
    "Blowgun (1)": "#e3f2fd", "Hand Xbow (1d6)": "#e3f2fd", "Heavy Xbow (1d10)": "#e3f2fd",
    "Light Xbow (1d8)": "#e3f2fd", "Longbow (1d8)": "#e3f2fd", "Shortbow (1d6)": "#e3f2fd",
    "Sling (1d4)": "#e3f2fd", "Dart (1d4)": "#f1f8e9", "Dagger (1d4)*": "#f1f8e9",
    "Handaxe (1d6)*": "#f1f8e9", "Javelin (1d6)*": "#f1f8e9", "Light Hammer (1d4)*": "#f1f8e9",
    "Spear (1d6)*": "#f1f8e9", "Trident (1d6)*": "#f1f8e9"
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


def calculate_attack_and_damage():
    try:
        ability_score = int(ability_score_entry.get() or 10)
        proficiency = int(proficiency_bonus_entry.get() or 0)
        ability_mod = (ability_score - 10) // 2

        range_penalty = 0
        if range_vars["Medium"].get():
            range_penalty = -2
        if range_vars["Long"].get():
            range_penalty = -5

        target_ac = get_selected_armor_class()
        weapon_name = get_selected_weapon()

        if not weapon_name:
            messagebox.showerror("Error", "Please select a weapon.")
            return

        d20_roll = random.randint(1, 20)
        attack_total = d20_roll + ability_mod + proficiency + range_penalty

        if d20_roll == 20:
            low, high = WEAPONS[weapon_name]
            dmg = random.randint(low, high) + ability_mod if high > 0 else 0
            result = f"CRIT! {dmg} damage!" if high > 0 else "CRIT! (Special Effect)"
            color = "green"
        elif d20_roll == 1:
            result = "NAT 1! Miss."
            color = "red"
        elif attack_total >= target_ac:
            low, high = WEAPONS[weapon_name]
            dmg = random.randint(low, high) + ability_mod if high > 0 else 0
            result = f"HIT! ({attack_total}) for {dmg} damage."
            color = "blue"
        else:
            result = f"MISS! ({attack_total} vs AC {target_ac})"
            color = "black"

        result_label.config(text=result, fg=color)
        attack_roll_label.config(
            text=f"Attack: {attack_total} (d20: {d20_roll}, Penalty: {range_penalty})")
    except ValueError:
        messagebox.showerror("Error", "Check your stat inputs.")


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


def reset_all():
    for var in weapon_vars.values():
        var.set(False)
    for var in monster_vars.values():
        var.set(False)
    for var in range_vars.values():
        var.set(False)
    range_vars["Short"].set(True)
    ability_score_entry.delete(0, tk.END)
    ability_score_entry.insert(0, "10")
    proficiency_bonus_entry.delete(0, tk.END)
    proficiency_bonus_entry.insert(0, "2")
    manual_ac_entry.delete(0, tk.END)
    attack_roll_label.config(text="Attack Roll: --")
    result_label.config(text="Result: --", fg="black")


root = tk.Tk()
root.title("Ranged & Thrown Attack Calculator")

# Stats
stats_frame = tk.LabelFrame(root, text=" Character Stats ", padx=10, pady=5)
stats_frame.pack(pady=5, fill="x", padx=10)
tk.Label(stats_frame, text="Ability Score:").grid(row=0, column=0)
ability_score_entry = tk.Entry(stats_frame, width=5)
ability_score_entry.insert(0, "10")
ability_score_entry.grid(row=0, column=1, padx=5)
tk.Label(stats_frame, text="Proficiency:").grid(row=0, column=2)
proficiency_bonus_entry = tk.Entry(stats_frame, width=5)
proficiency_bonus_entry.insert(0, "2")
proficiency_bonus_entry.grid(row=0, column=3, padx=5)

# Range
range_frame = tk.LabelFrame(root, text=" Range Increment ", padx=10, pady=5)
range_frame.pack(pady=5, fill="x", padx=10)
for i, inc in enumerate(["Short", "Medium", "Long"]):
    var = tk.BooleanVar(value=(inc == "Short"))
    range_vars[inc] = var
    tk.Checkbutton(range_frame, text=f"{inc} Range", variable=var, command=lambda r=inc: single_select_range(
        r)).grid(row=0, column=i, padx=20)

# Weapons (5 Columns)
weapon_frame = tk.LabelFrame(
    root, text=" Select Ranged/Thrown Weapon ", padx=10, pady=5)
weapon_frame.pack(padx=10, pady=5, fill="x")

for i, weapon in enumerate(WEAPONS):
    var = tk.BooleanVar()
    weapon_vars[weapon] = var
    bg = WEAPON_COLORS.get(weapon, "#f5f5f5")
    tk.Checkbutton(weapon_frame, text=weapon, variable=var, bg=bg,
                   command=lambda w=weapon: single_select_weapon(w)).grid(row=i//5, column=i % 5, sticky="w")

# New Legend Section for RangedDamage.py
legend_frame = tk.Frame(weapon_frame)
legend_frame.grid(row=(len(WEAPONS)//5)+1, column=0,
                  columnspan=5, pady=5, sticky="w")

tk.Label(legend_frame, text="Legend:", font=(
    "Calibri", 12, "bold")).pack(side="left", padx=5)
tk.Label(legend_frame, text=" Ammunition ", bg="#e3f2fd",
         relief="ridge", font=("Calibri", 12)).pack(side="left", padx=2)
tk.Label(legend_frame, text=" Thrown (*) ", bg="#f1f8e9",
         relief="ridge", font=("Calibri", 12)).pack(side="left", padx=2)
tk.Label(legend_frame, text=" Standard ", bg="#f5f5f5",
         relief="ridge", font=("Calibri", 12)).pack(side="left", padx=2)

# Monsters (5 Columns)
monster_frame = tk.LabelFrame(
    root, text=" Select Target Monster ", padx=10, pady=5)
monster_frame.pack(padx=10, pady=5, fill="x")
for i, (monster, ac) in enumerate(MONSTER_ARMOR_CLASSES.items()):
    var = tk.BooleanVar()
    monster_vars[monster] = var
    tk.Checkbutton(monster_frame, text=f"{monster} ({ac})", variable=var, command=lambda m=monster: single_select_monster(
        m)).grid(row=i//5, column=i % 5, sticky="w")

# Controls
ctrl_frame = tk.Frame(root)
ctrl_frame.pack(pady=5)
tk.Label(ctrl_frame, text="Manual AC:").grid(row=0, column=0)
manual_ac_entry = tk.Entry(ctrl_frame, width=5)
manual_ac_entry.grid(row=0, column=1, padx=5)
tk.Button(ctrl_frame, text="Attack", command=calculate_attack_and_damage,
          bg="#d1ffd1", font=("Calibri", 12, "bold")).grid(row=0, column=2, padx=10)
tk.Button(ctrl_frame, text="Reset All", command=reset_all,
          bg="#ffcccc").grid(row=0, column=3)

attack_roll_label = tk.Label(root, text="Attack Roll: --")
attack_roll_label.pack()
result_label = tk.Label(root, text="Result: --", font=("Calibri", 13, "bold"))
result_label.pack(pady=5)

root.mainloop()
