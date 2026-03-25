import tkinter as tk
from tkinter import messagebox
import random

# Unified Monster AC Data
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

monster_vars = {}
caster_vars = {}
range_vars = {}


def single_select_monster(selected_name):
    """Ensures only one monster is selected at a time."""
    for name, var in monster_vars.items():
        if name != selected_name:
            var.set(False)
    manual_ac_entry.delete(0, tk.END)


def single_select_caster(selected_type):
    """Ensures only one caster type is selected."""
    for c_type, var in caster_vars.items():
        if c_type != selected_type:
            var.set(False)


def single_select_range(selected_inc):
    """Ensures only one range increment is selected."""
    for inc, var in range_vars.items():
        if inc != selected_inc:
            var.set(False)


def get_proficiency_bonus(class_level):
    """Calculates proficiency based on caster type and level."""
    if caster_vars["Full"].get():
        if class_level < 5:
            return 2
        elif class_level < 9:
            return 3
        elif class_level < 13:
            return 4
        elif class_level < 17:
            return 5
        else:
            return 6
    elif caster_vars["Half"].get():
        if class_level < 6:
            return 2
        elif class_level < 10:
            return 3
        elif class_level < 14:
            return 4
        elif class_level < 18:
            return 5
        else:
            return 6
    elif caster_vars["Third"].get():
        if class_level < 7:
            return 2
        elif class_level < 13:
            return 3
        elif class_level < 19:
            return 4
        else:
            return 5
    return 0


def calculate_spell_attack():
    try:
        ability_score = int(ability_score_entry.get() or 10)
        class_level = int(class_level_entry.get() or 1)

        target_ac = get_selected_armor_class()

        prof_bonus = get_proficiency_bonus(class_level)
        ability_mod = (ability_score - 10) // 2

        # Determine range penalty
        penalty = 0
        if range_vars["Medium"].get():
            penalty = -2  # Example penalty logic
        if range_vars["Long"].get():
            penalty = -5

        d20_roll = random.randint(1, 20)
        total_attack = d20_roll + prof_bonus + ability_mod + penalty

        attack_roll_label.config(
            text=f"Total Spell Attack: {total_attack} (d20: {d20_roll})")

        if d20_roll == 20:
            result_label.config(text="CRITICAL HIT!", fg="green")
        elif d20_roll == 1:
            result_label.config(text="NATURAL 1 - MISS!", fg="red")
        elif total_attack >= target_ac:
            result_label.config(
                text=f"HIT! (Target AC: {target_ac})", fg="blue")
        else:
            result_label.config(
                text=f"MISS! (Target AC: {target_ac})", fg="black")

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers for stats.")


def get_selected_armor_class():
    for monster, var in monster_vars.items():
        if var.get():
            return MONSTER_ARMOR_CLASSES[monster]
    return int(manual_ac_entry.get() or 10)


def reset_all():
    ability_score_entry.delete(0, tk.END)
    ability_score_entry.insert(0, "10")
    class_level_entry.delete(0, tk.END)
    class_level_entry.insert(0, "1")
    manual_ac_entry.delete(0, tk.END)
    for v in monster_vars.values():
        v.set(False)
    for v in caster_vars.values():
        v.set(False)
    for v in range_vars.values():
        v.set(False)
    range_vars["Short"].set(True)
    caster_vars["Full"].set(True)
    attack_roll_label.config(text="Spell Attack Roll: --")
    result_label.config(text="Result: --", fg="black")


root = tk.Tk()
root.title("Spell Attack Calculator v4")

# Character Stats
stats_frame = tk.LabelFrame(root, text=" Caster Stats ", padx=10, pady=5)
stats_frame.pack(pady=5, fill="x", padx=10)

tk.Label(stats_frame, text="Ability Score:").grid(row=0, column=0)
ability_score_entry = tk.Entry(stats_frame, width=5)
ability_score_entry.insert(0, "10")
ability_score_entry.grid(row=0, column=1, padx=5)

tk.Label(stats_frame, text="Class Level:").grid(row=0, column=2)
class_level_entry = tk.Entry(stats_frame, width=5)
class_level_entry.insert(0, "1")
class_level_entry.grid(row=0, column=3, padx=5)

# Caster & Range Selection
selection_frame = tk.Frame(root)
selection_frame.pack(fill="x", padx=10)

caster_frame = tk.LabelFrame(
    selection_frame, text=" Caster Type ", padx=10, pady=5)
caster_frame.pack(side="left", expand=True, fill="both")

for c_text, c_key in [("Full (Wizard)", "Full"), ("Half (Paladin)", "Half"), ("Third (Warlock/Knight)", "Third")]:
    var = tk.BooleanVar()
    if c_key == "Full":
        var.set(True)
    caster_vars[c_key] = var
    tk.Checkbutton(caster_frame, text=c_text, variable=var,
                   command=lambda k=c_key: single_select_caster(k)).pack(anchor="w")

range_frame = tk.LabelFrame(
    selection_frame, text=" Spell Range ", padx=10, pady=5)
range_frame.pack(side="left", expand=True, fill="both")

for r_text, r_key in [("Short", "Short"), ("Medium", "Medium"), ("Long", "Long")]:
    var = tk.BooleanVar()
    if r_key == "Short":
        var.set(True)
    range_vars[r_key] = var
    tk.Checkbutton(range_frame, text=r_text, variable=var,
                   command=lambda k=r_key: single_select_range(k)).pack(anchor="w")

# 5-Column Monster Grid
monster_label_frame = tk.LabelFrame(
    root, text=" Select Target Monster ", padx=10, pady=5)
monster_label_frame.pack(padx=10, pady=5, fill="x")

MAX_COLS = 5
for i, (monster, ac) in enumerate(MONSTER_ARMOR_CLASSES.items()):
    var = tk.BooleanVar()
    monster_vars[monster] = var
    cb = tk.Checkbutton(monster_label_frame, text=f"{monster} ({ac})", variable=var,
                        command=lambda m=monster: single_select_monster(m))
    cb.grid(row=i//MAX_COLS, column=i % MAX_COLS, sticky="w")

# Footer
footer = tk.Frame(root)
footer.pack(pady=10)

tk.Label(footer, text="Manual AC:").grid(row=0, column=0)
manual_ac_entry = tk.Entry(footer, width=5)
manual_ac_entry.grid(row=0, column=1, padx=5)

tk.Button(footer, text="Execute Spell Attack", command=calculate_spell_attack,
          bg="#d1ffd1", font=("Calibri", 12, "bold")).grid(row=0, column=2, padx=10)
tk.Button(footer, text="Reset", command=reset_all,
          bg="#ffcccc").grid(row=0, column=3)

attack_roll_label = tk.Label(root, text="Spell Attack Roll: --")
attack_roll_label.pack()

result_label = tk.Label(root, text="Result: --", font=("Calibri", 13, "bold"))
result_label.pack(pady=5)

root.mainloop()
