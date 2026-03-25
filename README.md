# Portable D&D Calculator Suite

[![Download Latest Release](https://img.shields.io/github/v/release/Charlie3178/Simple-DnD-Calculator?label=Download%20Latest%20v1.0.0&color=green)](https://github.com/Charlie3178/Simple-DnD-Calculator/releases/latest)

A collection of lightweight, specialized combat calculators for tabletop gaming...

# Portable D&D Calculator Suite

A collection of lightweight, specialized combat calculators for tabletop gaming, bundled into a single portable Windows executable. This suite features a central "Hub" that dynamically loads tools from a local directory, allowing for easy updates and modularity.

## Features

- **Dynamic Hub:** The main launcher (`calculators.py`) automatically scans the `/tools` directory and generates launch buttons for any `.py` or `.exe` files it finds.
- **Specialized Combat Tools:**
  - **MeleeDamage:** Melee attack and damage calculator with color-coded legends for Finesse, Versatile, and Heavy weapon properties.
  - **RangedDamage:** Supports ammunition and thrown weapons with built-in range increment penalties.
  - **SpellHit:** A dedicated spell attack utility featuring monster AC lookup and caster-type proficiency scaling.
- **Optimized UI:** All tools utilize a 5-column grid layout to maximize information density while minimizing window height.
- **Portable:** Packaged using PyInstaller to run on Windows without requiring a local Python installation.

## Project Structure

```text
/
├── calculators.py          # Main launcher/hub script
├── LICENSE                 # GNU GPL v3.0 Full Text
├── README.md               # Project documentation
├── .gitignore              # Excludes Deprecated/ and build files
├── tools/                  # Active calculator modules
│   ├── MeleeDamage.py
│   ├── RangedDamage.py
│   ├── SpellHit.py
│   └── tkCharGen.py
└── Deprecated/             # Archived versions (Ignored by Git)
Build Instructions
To package the suite into a single executable, run the following from the root directory:

Bash
pyinstaller --onefile --noconsole --add-data "tools;tools" calculators.py
License
This project is licensed under the GNU General Public License v3.0. See the LICENSE file for the full text.
```
