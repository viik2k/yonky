# yonky

  Yonky - Script Launcher


Yonky is a lightweight, local-first PowerShell script launcher with a simple GUI.
It's designed to help IT technicians, AV pros, and small teams run predefined scripts easily.

🐾 Named after a beloved black cat, Yoko (Yonky,Bonk,Bonky) is as "quiet" and efficient as she is.

-------------------------------------
📦 What’s Included
-------------------------------------
- Yonky_2.0.py        --> The main launcher application (Python script)
- config.json         --> Script metadata (names, descriptions, etc.)
- /scripts/           --> Place your .ps1 PowerShell scripts here
- icon.ico            --> Icon for the Batch file (Temporary until its packed into a exe)

-------------------------------------
🧠 How to Use
-------------------------------------
1. Make sure you have Python 3.9+ installed.

2. Run Yonky using:
   > pythonw Yonky_2.0.py,
   > Placing the batch file on your desktop


3. Add your scripts into the /scripts/ folder.

4. Edit config.json to give each script a friendly name and description.

5. Launch scripts from the GUI with a click. Output will appear in the launcher window.

-------------------------------------
⚙️ Example config.json entry
-------------------------------------
{
  "Cleanup.ps1": {
    "name": "Clean Temp Folders",
    "description": "Deletes temp files older than 7 days."
  }
}

-------------------------------------
🛠 Tips
-------------------------------------
- Use "pythonw" instead of "python" to suppress the black console window.
- Scripts will run in separate threads to keep the GUI responsive.
- Log output and error handling improvements are in development!

-------------------------------------
📌 Notes
-------------------------------------
Yonky is in active development. Expect features like favorites, history, and remote config in future versions. Please feel free to contribute to this!

Built with love, PowerShell, and a little cat magic.
