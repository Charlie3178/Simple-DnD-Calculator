import tkinter as tk
from tkinter import ttk
import random

# Define races, subraces, classes, and subclasses
races = ["Aasimar", "Aarokocra", "Dragonborn", "Dwarf",
         "Elf", "Halfling", "Human", "Tiefling", "Warforged"]
subraces = {
    "Aasimar": ["Fallen", "Protector", "Scourge"],
    "Dragonborn": ["Black", "Blue", "Brass", "Bronze", "Copper", "Gold", "Green", "Silver", "White"],
    "Dwarf": ["Hill", "Mountain"],
    "Elf": ["High", "Wood", "Dark"],
    "Halfling": ["Lightfoot", "Stout"]
}
classes = ["Artificer", "Barbarian", "Bard", "Cleric", "Druid", "Fighter",
           "Monk", "Paladin", "Ranger", "Rogue", "Sorcerer", "Warlock", "Wizard"]
subclasses = {
    "Artificer": ["Alchemist", "Armorer", "Artillerist"],
    "Barbarian": ["Berserker", "Totem Warrior"],
    "Bard": ["Lore", "Valor"],
    "Cleric": ["Knowledge", "Life", "Light", "Nature", "Tempest", "Trickery", "War"],
    "Druid": ["Land", "Moon"],
    "Fighter": ["Champion", "Battle Master", "Eldritch Knight"],
    "Monk": ["Open Hand", "Shadow", "Four Elements"],
    "Paladin": ["Devotion", "Ancients", "Vengeance"],
    "Ranger": ["Hunter", "Beast Master"],
    "Rogue": ["Thief", "Assassin", "Arcane Trickster"],
    "Sorcerer": ["Draconic Bloodline", "Wild Magic"],
    "Warlock": ["Fiend", "Archfey", "Great Old One"],
    "Wizard": ["Abjuration", "Conjuration", "Divination", "Enchantment", "Evocation", "Illusion", "Necromancy", "Transmutation"]
}


def update_subraces(event):
    subrace_combobox['values'] = subraces[race_combobox.get()]
    if subrace_combobox['values']:
        subrace_combobox.current(0)

    else:
        subrace_combobox.set("")  # Clear it if no subraces exist


def update_subclasses(event):
    subclass_combobox['values'] = subclasses[class_combobox.get()]
    if subclass_combobox['values']:
        subclass_combobox.current(0)

    else:
        subclass_combobox.set("")  # Clear it if no subclasses exist


def generate_ability_scores():
    return [random.randint(12, 18) for _ in range(6)]


root = tk.Tk()
root.title("D&D Character Creator")

# Create a frame for the race selection
race_frame = ttk.Frame(root)
race_frame.pack()

race_label = ttk.Label(race_frame, text="Race:")
race_label.grid(row=0, column=0)

race_combobox = ttk.Combobox(race_frame, values=races)
race_combobox.grid(row=0, column=1)
race_combobox.current(0)
race_combobox.bind("<<ComboboxSelected>>", update_subraces)

# Create a frame for the subrace selection
subrace_frame = ttk.Frame(root)
subrace_frame.pack()

subrace_label = ttk.Label(subrace_frame, text="Subrace:")
subrace_label.grid(row=0, column=0)

subrace_combobox = ttk.Combobox(subrace_frame)
subrace_combobox.grid(row=0, column=1)
if subrace_combobox['values']:
    subrace_combobox.current(0)

else:
    subrace_combobox.set("")  # Clear it if no subraces exist

# Create a frame for the class selection
class_frame = ttk.Frame(root)
class_frame.pack()

class_label = ttk.Label(class_frame, text="Class:")
class_label.grid(row=0, column=0)

class_combobox = ttk.Combobox(class_frame, values=classes)
class_combobox.grid(row=0, column=1)
class_combobox.current(0)
class_combobox.bind("<<ComboboxSelected>>", update_subclasses)

# Create a frame for the subclass selection
subclass_frame = ttk.Frame(root)
subclass_frame.pack()

subclass_label = ttk.Label(subclass_frame, text="Subclass:")
subclass_label.grid(row=0, column=0)

subclass_combobox = ttk.Combobox(subclass_frame)
subclass_combobox.grid(row=0, column=1)
if subclass_combobox['values']:
    subclass_combobox.current(0)

else:
    subclass_combobox.set("")  # Clear it if no subclasses exist

# Create a frame for ability scores
ability_frame = ttk.LabelFrame(root, text="Ability Scores")
ability_frame.pack()

abilities = ["Strength", "Dexterity", "Constitution",
             "Intelligence", "Wisdom", "Charisma"]
ability_scores = generate_ability_scores()
for i in range(6):
    label = ttk.Label(ability_frame, text=f"{abilities[i]}:")
    label.grid(row=i, column=0, sticky="w")
    score_label = ttk.Label(ability_frame, text=ability_scores[i])
    score_label.grid(row=i, column=1, sticky="w")

root.mainloop()
