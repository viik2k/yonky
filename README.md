
  Yonky v0.9.2 - Launcher


Yonky is a lightweight, local-first PowerShell script launcher with a simple GUI.
It helps IT technicians, AV pros, and small teams run their predefined PowerShell scripts
through an easy, safe interface — no consoles, no typing, no nonsense.

This is the official EXE release.
🖤 Inspired by a very good black cat, Yoko.

------------------------------
📦 What’s in the ZIP
------------------------------
- Yonky.exe             --> The launcher (compiled EXE)
 codex/update-readme.md-and-readme.txt
- config.json           --> Automatically created settings file

 - config.json           --> Optional launcher settings & script metadata
main
- /scripts/             --> Place your PowerShell (.ps1) scripts here
- README.txt            --> This file

------------------------------
🚀 Getting Started
------------------------------
1. **Extract** the ZIP to a local folder (e.g. `C:\Yonky\`)
2. **Double-click `Yonky.exe`** to launch the GUI
 codex/update-readme.md-and-readme.txt
3. Place your PowerShell or batch scripts in the `/scripts/` folder
4. `config.json` will be created or updated automatically when Yonky starts

3. Add your scripts to the `/scripts/` folder
4. Edit `config.json` to set friendly names and descriptions under the `scripts` section
 main

Scripts in the `scripts` folder are detected automatically when you start Yonky or press **Refresh**.

------------------------------
🧠 Example `config.json`
------------------------------
{
 codex/update-readme.md-and-readme.txt
  "recent_scripts": [],
  "auto_scroll": true,
  "show_timestamps": true,
  "execution_policy": "Bypass"
}

Yonky updates this file to remember your preferences between runs.

------------------------------
📃 Working with Scripts
------------------------------
* **Automatic detection** – Any `.ps1`, `.bat` or `.cmd` file placed in the `scripts` folder shows up when you start Yonky or click **Refresh**.
* **Manual addition** – Use `File > Add Script...` to copy an existing script into the folder.
* **Persistence** – Scripts stay listed as long as their files remain in `scripts/`; Yonky also records recent runs in `config.json`.


  "scripts": {
    "Cleanup.ps1": {
      "name": "Clean Temp Folders",
      "description": "Deletes temp files older than 7 days."
    }
  }
}

This file is optional. If it's missing, Yonky scans the `scripts` folder and
generates entries automatically using each filename.
 main

------------------------------

🛠 Using the Launcher
=======
🛠 Features (v0.9.2)


------------------------------
- **Add Script**: `File > Add Script...` copies an existing file into the `scripts` folder.
- **New Script**: `File > New Script...` creates a blank `.ps1` ready for editing.
- **Edit/Delete**: Select a script and use the `Edit Script` or `Delete Selected` buttons.
- **Preferences**: Open `Edit > Preferences` to change options saved in `config.json`.
- **Tools**: Open the scripts folder or launch PowerShell from the `Tools` menu.


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

-------------------------------------
![image](https://github.com/user-attachments/assets/125dba38-2675-4bc1-89dc-f9ed5f1a70b9)
