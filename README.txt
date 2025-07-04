===========================
  Yonky v0.9.2 - Launcher
===========================

Yonky is a lightweight, local-first PowerShell script launcher with a simple GUI.
It helps IT technicians, AV pros, and small teams run their predefined PowerShell scripts
through an easy, safe interface — no consoles, no typing, no nonsense.

This is the official EXE release.
🖤 Inspired by a very good black cat, Yoko.

------------------------------
📦 What’s in the ZIP
------------------------------
- Yonky.exe             --> The launcher (compiled EXE)
- config.json           --> Optional script metadata
- /scripts/             --> Place your PowerShell (.ps1) scripts here
- README.txt            --> This file

------------------------------
🚀 Getting Started
------------------------------
1. **Extract** the ZIP to a local folder (e.g. `C:\Yonky\`)
2. **Double-click `Yonky.exe`** to launch the GUI
3. Add your scripts to the `/scripts/` folder
4. Edit `config.json` to set friendly names and descriptions

The launcher will auto-detect available `.ps1` files and display them with names, descriptions, and a “Run” button for each.

------------------------------
🧠 Example config.json
------------------------------
{
  "Cleanup.ps1": {
    "name": "Clean Temp Folders",
    "description": "Deletes temp files older than 7 days."
  }
}

This file is optional. If it's missing, Yonky will simply list scripts by filename.

------------------------------

🛠 Using the Launcher
=======
🛠 Features (v0.9.1.1)


------------------------------
- **Add Script**: `File > Add Script...` copies an existing file into the `scripts` folder.
- **New Script**: `File > New Script...` creates a blank `.ps1` ready for editing.
- **Edit/Delete**: Select a script and use the `Edit Script` or `Delete Selected` buttons.
- **Preferences**: Open `Edit > Preferences` to see the upcoming settings dialog (edit `config.json` to change options).
- **Tools**: Open the scripts folder or launch PowerShell from the `Tools` menu.

------------------------------
🔧 Features (v0.9.2)
------------------------------
✔️ Simple GUI to run PowerShell or batch scripts
✔️ Real-time output with optional timestamps
✔️ Add, create, edit, and delete scripts from the launcher
✔️ config.json for names, descriptions, and settings
✔️ Tools menu to open the scripts folder or a PowerShell console
✔️ Portable EXE — no install required

------------------------------
🆕 What's New in 0.9.2
------------------------------
- Preferences dialog accessible from **Edit > Preferences** (placeholder for upcoming options)
- Config expanded with `recent_scripts`, `auto_scroll`, `show_timestamps` and `execution_policy`
- Create, edit and delete scripts directly from the launcher
- Tools menu added to open the scripts folder or launch PowerShell
- Support for `.bat` and `.cmd` scripts

------------------------------
📌 Notes
------------------------------
- Scripts run using PowerShell silently under the hood.
- You can update scripts/config without restarting the app (click “Refresh”).
- This is an early release — more features coming!

------------------------------
📫 Feedback & Source Code
------------------------------
GitHub: https://github.com/viik2k/yonky  
Latest Release: https://github.com/viik2k/yonky/releases  

Please report bugs, request features, or contribute via GitHub Issues.

Built with love, PowerShell, and a black cat named Yoko.
