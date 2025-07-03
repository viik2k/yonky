===========================
  Yonky v0.9.1 - Launcher
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
🔧 Features (v0.9.1)
------------------------------
✔️ Simple GUI to run scripts  
✔️ Real-time script output display  
✔️ config.json for custom labels  
✔️ Auto-detect scripts from `scripts/` folder  
✔️ Portable EXE — no install required  

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
