import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox


def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def launch_app(app_name):
    path = get_resource_path(f"tools/{app_name}")
    try:
        subprocess.Popen([path], shell=True)
    except Exception as e:
        messagebox.showerror("Error", f"Could not launch {app_name}: {e}")


root = tk.Tk()
root.title("Quick Calc Hub")
root.geometry("300x400")

# Label for the hub
tk.Label(root, text="Portable Calculator Suite",
         font=("Arial", 12, "bold")).pack(pady=10)

# Folder where your calculators are stored before bundling
tools_dir = get_resource_path("tools")
if os.path.exists(tools_dir):
    for filename in os.listdir(tools_dir):
        if filename.endswith(".exe") or filename.endswith(".py"):
            btn = tk.Button(root, text=filename, width=25,
                            command=lambda f=filename: launch_app(f))
            btn.pack(pady=5)
else:
    tk.Label(root, text="No tools found in /tools directory").pack()

root.mainloop()
