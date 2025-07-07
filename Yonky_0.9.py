import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext, simpledialog
import threading
import json
import time
from datetime import datetime

if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")


class PreferencesDialog(tk.Toplevel):
    """Dialog for editing user preferences"""

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Preferences")
        self.resizable(False, False)

        # Variables bound to configuration options
        self.auto_scroll_var = tk.BooleanVar(value=parent.config_data.get("auto_scroll", True))
        self.timestamps_var = tk.BooleanVar(value=parent.config_data.get("show_timestamps", True))
        self.exec_policy_var = tk.StringVar(value=parent.config_data.get("execution_policy", "Bypass"))

        # Build UI
        ttk.Checkbutton(self, text="Auto-scroll output", variable=self.auto_scroll_var).pack(anchor="w", padx=10, pady=5)
        ttk.Checkbutton(self, text="Show timestamps", variable=self.timestamps_var).pack(anchor="w", padx=10, pady=5)

        exec_frame = ttk.Frame(self)
        exec_frame.pack(fill="x", padx=10, pady=5)
        ttk.Label(exec_frame, text="Execution Policy:").pack(side="left")
        ttk.Entry(exec_frame, textvariable=self.exec_policy_var, width=20).pack(side="left", padx=(5, 0))

        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", pady=10)
        ttk.Button(button_frame, text="OK", command=self.on_ok).pack(side="right", padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.destroy).pack(side="right")

        self.protocol("WM_DELETE_WINDOW", self.on_ok)

    def on_ok(self):
        """Save settings and close"""
        self.parent.config_data["auto_scroll"] = self.auto_scroll_var.get()
        self.parent.config_data["show_timestamps"] = self.timestamps_var.get()
        self.parent.config_data["execution_policy"] = self.exec_policy_var.get()
        self.parent.save_config()
        self.destroy()

class ScriptLauncherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Yonky – PowerShell Script Launcher")
        self.geometry("800x600")
        self.minsize(600, 400)
        
        # Load configuration
        self.config_data = self.load_config()
        
        # Apply theme
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.setup_menu()
        self.setup_ui()
        self.load_scripts()
        
        # Bind close event
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_config(self):
        """Load application configuration"""
        default_config = {
            "recent_scripts": [],
            "auto_scroll": True,
            "show_timestamps": True,
            "execution_policy": "Bypass"
        }
        
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    return {**default_config, **json.load(f)}
            except:
                return default_config
        return default_config

    def save_config(self):
        """Save application configuration"""
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.config_data, f, indent=2)
        except Exception as e:
            print(f"Could not save config: {e}")

    def setup_ui(self):
        """Setup the user interface"""
        # Header
        header_frame = ttk.Frame(self)
        header_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(header_frame, text="Yonky - Built with Powershell, and a little cat magic", 
                 font=("Segoe UI", 16, "bold")).pack(side=tk.LEFT)
        
        # Status label
        self.status_label = ttk.Label(header_frame, text="Ready", 
                                     font=("Segoe UI", 9))
        self.status_label.pack(side=tk.RIGHT)

        # Main container with paned window
        main_paned = ttk.PanedWindow(self, orient=tk.VERTICAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Scripts frame
        scripts_container = ttk.LabelFrame(main_paned, text="Available Scripts", padding=5)
        main_paned.add(scripts_container, weight=1)
        
        # Create treeview for scripts
        columns = ('Name', 'Modified', 'Size')
        self.script_tree = ttk.Treeview(scripts_container, columns=columns, show='headings', height=6)
        
        # Configure columns
        self.script_tree.heading('Name', text='Script Name')
        self.script_tree.heading('Modified', text='Last Modified')
        self.script_tree.heading('Size', text='Size (KB)')
        
        self.script_tree.column('Name', width=300)
        self.script_tree.column('Modified', width=150)
        self.script_tree.column('Size', width=80)
        
        # Scrollbar for treeview
        tree_scroll = ttk.Scrollbar(scripts_container, orient=tk.VERTICAL, command=self.script_tree.yview)
        self.script_tree.configure(yscrollcommand=tree_scroll.set)
        
        # Pack treeview and scrollbar
        self.script_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Buttons frame
        button_frame = ttk.Frame(scripts_container)
        button_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Button(button_frame, text="Run Selected", 
                  command=self.run_selected_script).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Edit Script", 
                  command=self.edit_selected_script).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Delete Selected", 
                  command=self.delete_selected_script).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Refresh", 
                  command=self.load_scripts).pack(side=tk.RIGHT)

        # Output frame
        output_container = ttk.LabelFrame(main_paned, text="Output", padding=5)
        main_paned.add(output_container, weight=2)

        # Output text widget with better formatting
        self.output_box = scrolledtext.ScrolledText(
            output_container, 
            height=15, 
            wrap=tk.WORD, 
            font=("Consolas", 10),
            bg='#1e1e1e',
            fg='#ffffff',
            insertbackground='white'
        )
        self.output_box.pack(fill=tk.BOTH, expand=True)

        # Configure text tags for colored output
        self.output_box.tag_configure("error", foreground="#ff6b6b")
        self.output_box.tag_configure("success", foreground="#51cf66")
        self.output_box.tag_configure("info", foreground="#74c0fc")
        self.output_box.tag_configure("timestamp", foreground="#868e96")

        # Progress and status frame
        status_frame = ttk.Frame(self)
        status_frame.pack(fill=tk.X, padx=10, pady=(0, 5))

        self.progress = ttk.Progressbar(status_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(0, 5))

        # Bottom status
        self.bottom_status = ttk.Label(status_frame, text="Ready to run scripts")
        self.bottom_status.pack(side=tk.LEFT)

    def setup_menu(self):
        """Setup application menu"""
        menu = tk.Menu(self)

        # File Menu
        file_menu = tk.Menu(menu, tearoff=0)
        file_menu.add_command(label="Add Script...", command=self.add_script, accelerator="Ctrl+O")
        file_menu.add_command(label="New Script...", command=self.create_new_script, accelerator="Ctrl+N")
        file_menu.add_separator()
        file_menu.add_command(label="Refresh Scripts", command=self.load_scripts, accelerator="F5")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing, accelerator="Ctrl+Q")
        menu.add_cascade(label="File", menu=file_menu)

        # Edit Menu
        edit_menu = tk.Menu(menu, tearoff=0)
        edit_menu.add_command(label="Clear Output", command=self.clear_output, accelerator="Ctrl+L")
        edit_menu.add_command(label="Copy Output", command=self.copy_output, accelerator="Ctrl+C")
        edit_menu.add_separator()
        edit_menu.add_command(label="Preferences...", command=self.show_preferences)
        menu.add_cascade(label="Edit", menu=edit_menu)

        # Tools Menu
        tools_menu = tk.Menu(menu, tearoff=0)
        tools_menu.add_command(label="Open Scripts Folder", command=self.open_scripts_folder)
        tools_menu.add_command(label="PowerShell Console", command=self.open_powershell)
        menu.add_cascade(label="Tools", menu=tools_menu)

        # Help Menu
        help_menu = tk.Menu(menu, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menu.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menu)

        # Bind keyboard shortcuts
        self.bind('<Control-o>', lambda e: self.add_script())
        self.bind('<Control-n>', lambda e: self.create_new_script())
        self.bind('<F5>', lambda e: self.load_scripts())
        self.bind('<Control-l>', lambda e: self.clear_output())
        self.bind('<Control-q>', lambda e: self.on_closing())

    def log_output(self, message, tag=""):
        """Add message to output with optional formatting"""
        if self.config_data.get("show_timestamps", True):
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.output_box.insert(tk.END, f"[{timestamp}] ", "timestamp")
        
        self.output_box.insert(tk.END, message + "\n", tag)
        
        if self.config_data.get("auto_scroll", True):
            self.output_box.see(tk.END)

    def add_script(self):
        """Add a new script from file system"""
        file_path = filedialog.askopenfilename(
            title="Select PowerShell Script",
            filetypes=[
                ("PowerShell Scripts", "*.ps1"),
                ("Batch Files", "*.bat *.cmd"),
                ("All Files", "*.*")
            ]
        )
        if file_path:
            dest_path = os.path.join(SCRIPTS_DIR, os.path.basename(file_path))
            try:
                with open(file_path, 'rb') as src, open(dest_path, 'wb') as dst:
                    dst.write(src.read())
                self.log_output(f"Added script: {os.path.basename(file_path)}", "success")
                self.load_scripts()
            except Exception as e:
                messagebox.showerror("Error", f"Could not add script: {e}")

    def create_new_script(self):
        """Create a new empty script"""
        script_name = tk.simpledialog.askstring("New Script", "Enter script name (without .ps1):")
        if script_name:
            if not script_name.endswith('.ps1'):
                script_name += '.ps1'
            
            script_path = os.path.join(SCRIPTS_DIR, script_name)
            try:
                with open(script_path, 'w') as f:
                    f.write("# New PowerShell Script\n# Created: {}\n\nWrite-Host 'Hello from {}'\n".format(
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        script_name
                    ))
                self.log_output(f"Created new script: {script_name}", "success")
                self.load_scripts()
                self.edit_script(script_name)
            except Exception as e:
                messagebox.showerror("Error", f"Could not create script: {e}")

    def edit_script(self, script_name):
        """Open script in default editor"""
        script_path = os.path.join(SCRIPTS_DIR, script_name)
        try:
            os.startfile(script_path)
        except Exception as e:
            self.log_output(f"Could not open editor: {e}", "error")

    def edit_selected_script(self):
        """Edit the currently selected script"""
        selection = self.script_tree.selection()
        if selection:
            script_name = self.script_tree.item(selection[0])['values'][0]
            self.edit_script(script_name)

    def clear_output(self):
        """Clear the output window"""
        self.output_box.delete(1.0, tk.END)
        self.log_output("Output cleared", "info")

    def copy_output(self):
        """Copy output to clipboard"""
        try:
            output_text = self.output_box.get(1.0, tk.END)
            self.clipboard_clear()
            self.clipboard_append(output_text)
            self.log_output("Output copied to clipboard", "info")
        except Exception as e:
            self.log_output(f"Could not copy output: {e}", "error")

    def load_scripts(self):
        """Load and display available scripts"""
        # Clear existing items
        for item in self.script_tree.get_children():
            self.script_tree.delete(item)
        
        if not os.path.exists(SCRIPTS_DIR):
            return
            
        try:
            scripts = [f for f in os.listdir(SCRIPTS_DIR) 
                      if f.endswith(('.ps1', '.bat', '.cmd'))]
            
            for script in sorted(scripts):
                script_path = os.path.join(SCRIPTS_DIR, script)
                try:
                    stat = os.stat(script_path)
                    modified = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
                    size = f"{stat.st_size / 1024:.1f}"
                    
                    self.script_tree.insert('', tk.END, values=(script, modified, size))
                except Exception as e:
                    self.script_tree.insert('', tk.END, values=(script, "Error", "0"))
            
            self.status_label.config(text=f"{len(scripts)} scripts loaded")
            
        except Exception as e:
            self.log_output(f"Error loading scripts: {e}", "error")

    def run_selected_script(self):
        """Run the currently selected script"""
        selection = self.script_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a script to run")
            return
        
        script_name = self.script_tree.item(selection[0])['values'][0]
        self.run_script_thread(script_name)

    def delete_selected_script(self):
        """Delete the currently selected script"""
        selection = self.script_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a script to delete")
            return
        
        script_name = self.script_tree.item(selection[0])['values'][0]
        self.delete_script(script_name)

    def run_script_thread(self, script_name):
        """Run script in a separate thread"""
        thread = threading.Thread(target=self.run_script, args=(script_name,), daemon=True)
        thread.start()

    def run_script(self, script_name):
        """Execute a PowerShell script"""
        script_path = os.path.join(SCRIPTS_DIR, script_name)
        self.set_ui_state("running", script_name)

        try:
            # Determine execution command based on file extension
            if script_name.endswith('.ps1'):
                cmd = ["powershell", "-ExecutionPolicy", self.config_data.get("execution_policy", "Bypass"), 
                       "-File", script_path]
            elif script_name.endswith(('.bat', '.cmd')):
                cmd = [script_path]
            else:
                raise ValueError(f"Unsupported script type: {script_name}")


            start_time = time.time()
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            def stream_reader(stream, tag, prefix):
                first = True
                for line in iter(stream.readline, ""):
                    if not line:
                        break
                    if first:
                        self.log_output(prefix, "info" if tag == "" else "error")
                        first = False
                    self.log_output(line.rstrip(), tag)

            stdout_thread = threading.Thread(
                target=stream_reader,
                args=(process.stdout, "", "STDOUT:"),
                daemon=True,
            )
            stderr_thread = threading.Thread(
                target=stream_reader,
                args=(process.stderr, "error", "STDERR:"),
                daemon=True,
            )

            stdout_thread.start()
            stderr_thread.start()

            timed_out = False
            try:
                process.wait(timeout=300)
            except subprocess.TimeoutExpired:
                process.kill()
                timed_out = True

            end_time = time.time()
            stdout_thread.join()
            stderr_thread.join()

            self.log_output(f"=== Executed: {script_name} ===", "info")
            self.log_output(
                f"Duration: {end_time - start_time:.2f} seconds",
                "info",
            )

            if timed_out:
                self.log_output(
                    f"Script '{script_name}' timed out after 5 minutes",
                    "error",
                )
            else:
                if process.returncode != 0:
                    self.log_output(
                        f"Exit code: {process.returncode}",
                        "error",
                    )
                else:
                    self.log_output(
                        "Script completed successfully",
                        "success",
                    )
        except Exception as e:
            self.log_output(f"Exception running '{script_name}': {e}", "error")

        self.set_ui_state("done", script_name)

    def delete_script(self, script_name):
        """Delete a script file"""
        confirm = messagebox.askyesno("Confirm Delete", 
                                     f"Are you sure you want to delete '{script_name}'?")
        if confirm:
            try:
                os.remove(os.path.join(SCRIPTS_DIR, script_name))
                self.load_scripts()
                self.log_output(f"Deleted script: {script_name}", "success")
            except Exception as e:
                messagebox.showerror("Error", f"Could not delete script: {e}")

    def set_ui_state(self, state, script_name=""):
        """Update UI state during script execution"""
        if state == "running":
            self.progress.start()
            self.bottom_status.config(text=f"Running: {script_name}")
            self.log_output(f"Starting execution: {script_name}", "info")
        elif state == "done":
            self.progress.stop()
            self.bottom_status.config(text="Ready")

    def open_scripts_folder(self):
        """Open the scripts directory in file explorer"""
        try:
            os.startfile(SCRIPTS_DIR)
        except Exception as e:
            self.log_output(f"Could not open scripts folder: {e}", "error")

    def open_powershell(self):
        """Open PowerShell console"""
        try:
            subprocess.Popen(["powershell"], creationflags=subprocess.CREATE_NEW_CONSOLE)
        except Exception as e:
            self.log_output(f"Could not open PowerShell: {e}", "error")

    def show_preferences(self):
        """Show preferences dialog"""
        PreferencesDialog(self)

    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo("About", 
                           "Yonky - PowerShell Script Launcher\n"
                           "Version 0.9.2\n"
                           "Enhanced script management and execution\n"
                           "Created By Finn Henderson\n"
                           "Current Version. 07/2025")

    def on_closing(self):
        """Handle application closing"""
        self.save_config()
        self.destroy()

if __name__ == "__main__":
    # Ensure required directories exist
    if not os.path.exists(SCRIPTS_DIR):
        os.makedirs(SCRIPTS_DIR)
    
    app = ScriptLauncherApp()
    app.mainloop()
