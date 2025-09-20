import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
import threading
import subprocess
import webbrowser
import importlib
import time

class AutoInstaller:
    @staticmethod
    def install_dependencies():
        """Automatically install all required dependencies"""
        dependencies = ["pyinstaller"]
        
        for package in dependencies:
            try:
                # Check if package is already installed
                importlib.import_module(package.split("[")[0] if "[" in package else package)
                print(f"✅ {package} already installed")
            except ImportError:
                print(f"⏳ Installing {package}...")
                try:
                    # Install package using pip
                    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                    print(f"✅ {package} installed successfully")
                except subprocess.CalledProcessError:
                    print(f"❌ Failed to install {package}")
                    return False
                except Exception as e:
                    print(f"❌ Error installing {package}: {str(e)}")
                    return False
        
        # Special case: Additional check for PyInstaller
        try:
            result = subprocess.run([sys.executable, "-m", "PyInstaller", "--version"], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                raise Exception("PyInstaller not working properly")
            print("✅ All dependencies installed and working correctly")
            return True
        except Exception as e:
            print(f"❌ PyInstaller verification failed: {str(e)}")
            return False

class AdvancedPythonToExeConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("DarkBoss1BD - Advanced Python to EXE Converter")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Hacker theme colors
        self.bg_color = "#000000"
        self.text_color = "#00ff00"
        self.accent_color = "#ff00ff"
        self.highlight_color = "#00ffff"
        
        self.root.configure(bg=self.bg_color)
        
        # Branding information
        self.branding_info = {
            "Telegram ID": "https://t.me/darkvaiadmin",
            "Website": "https://serialkey.top/",
            "Telegram Channel": "https://t.me/windowspremiumkey"
        }
        
        # Selected files and folders
        self.selected_files = []
        self.selected_folders = []
        
        # PyInstaller availability
        self.pyinstaller_available = False
        
        # Start automatic installation
        self.setup_ui()
        self.display_hacker_banner()
        self.start_auto_installation()
        
    def start_auto_installation(self):
        """Start automatic dependency installation"""
        self.status.config(text="Checking dependencies...")
        self.progress.start(10)
        
        def install_thread():
            try:
                success = AutoInstaller.install_dependencies()
                if success:
                    self.pyinstaller_available = True
                    self.status.config(text="All dependencies installed successfully!")
                    # Enable convert button
                    self.root.after(0, lambda: self.convert_btn.config(state=tk.NORMAL, bg="#003300"))
                    self.log_to_console("✅ All dependencies are ready!")
                else:
                    self.status.config(text="Failed to install dependencies")
                    self.log_to_console("❌ Failed to install some dependencies")
                    messagebox.showerror("Error", "Failed to install required dependencies. Please check your internet connection and try again.")
            except Exception as e:
                self.status.config(text=f"Installation error: {str(e)}")
                self.log_to_console(f"❌ Installation error: {str(e)}")
            finally:
                self.progress.stop()
        
        threading.Thread(target=install_thread, daemon=True).start()
    
    def setup_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header with hacker style
        header = tk.Label(main_frame, text="⚡ DARKBOSS1BD PYTHON TO EXE CONVERTER ⚡", 
                         font=("Courier New", 16, "bold"), 
                         fg=self.highlight_color, bg=self.bg_color)
        header.pack(pady=10)
        
        # Installation status
        self.install_status = tk.Label(main_frame, text="Checking dependencies...", 
                                      font=("Courier New", 10), 
                                      fg=self.text_color, bg=self.bg_color)
        self.install_status.pack(pady=5)
        
        # Hacker style subtitle
        subtitle = tk.Label(main_frame, text="Advanced Multi-Folder Support Tool", 
                           font=("Courier New", 12), 
                           fg=self.accent_color, bg=self.bg_color)
        subtitle.pack(pady=5)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Main tab
        main_tab = tk.Frame(notebook, bg=self.bg_color)
        notebook.add(main_tab, text="Main Settings")
        
        # File selection frame
        file_frame = tk.LabelFrame(main_tab, text=" Python File Selection ", 
                                  font=("Courier New", 10, "bold"),
                                  fg=self.text_color, bg=self.bg_color)
        file_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(file_frame, text="Main Python File:", 
                fg=self.text_color, bg=self.bg_color).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.file_path = tk.Entry(file_frame, width=50, bg="#111111", fg=self.text_color, insertbackground=self.text_color)
        self.file_path.grid(row=0, column=1, padx=5)
        tk.Button(file_frame, text="Browse", command=self.browse_file, 
                 bg="#222222", fg=self.text_color).grid(row=0, column=2)
        
        # Output settings frame
        output_frame = tk.LabelFrame(main_tab, text=" Output Settings ", 
                                    font=("Courier New", 10, "bold"),
                                    fg=self.text_color, bg=self.bg_color)
        output_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(output_frame, text="Output Name:", 
                fg=self.text_color, bg=self.bg_color).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.output_name = tk.Entry(output_frame, width=50, bg="#111111", fg=self.text_color, insertbackground=self.text_color)
        self.output_name.grid(row=0, column=1, padx=5)
        
        tk.Label(output_frame, text="Output Directory:", 
                fg=self.text_color, bg=self.bg_color).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.output_dir = tk.Entry(output_frame, width=50, bg="#111111", fg=self.text_color, insertbackground=self.text_color)
        self.output_dir.grid(row=1, column=1, padx=5)
        tk.Button(output_frame, text="Browse", command=self.browse_output_dir, 
                 bg="#222222", fg=self.text_color).grid(row=1, column=2)
        
        # Options frame
        options_frame = tk.LabelFrame(main_tab, text=" Build Options ", 
                                     font=("Courier New", 10, "bold"),
                                     fg=self.text_color, bg=self.bg_color)
        options_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.onefile = tk.BooleanVar(value=True)
        tk.Checkbutton(options_frame, text="Create single executable file", 
                      variable=self.onefile, fg=self.text_color, bg=self.bg_color, 
                      selectcolor="#222222").grid(row=0, column=0, sticky=tk.W, padx=5)
        
        self.console = tk.BooleanVar(value=True)
        tk.Checkbutton(options_frame, text="Show console window", 
                      variable=self.console, fg=self.text_color, bg=self.bg_color, 
                      selectcolor="#222222").grid(row=0, column=1, sticky=tk.W, padx=5)
        
        self.upx = tk.BooleanVar(value=False)
        tk.Checkbutton(options_frame, text="Use UPX compression (if available)", 
                      variable=self.upx, fg=self.text_color, bg=self.bg_color, 
                      selectcolor="#222222").grid(row=1, column=0, sticky=tk.W, padx=5)
        
        # Icon file selection
        icon_frame = tk.Frame(options_frame, bg=self.bg_color)
        icon_frame.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        tk.Label(icon_frame, text="Icon File (optional):", 
                fg=self.text_color, bg=self.bg_color).grid(row=0, column=0, sticky=tk.W)
        self.icon_path = tk.Entry(icon_frame, width=40, bg="#111111", fg=self.text_color, insertbackground=self.text_color)
        self.icon_path.grid(row=0, column=1, padx=5)
        tk.Button(icon_frame, text="Browse", command=self.browse_icon, 
                 bg="#222222", fg=self.text_color).grid(row=0, column=2)
        
        # Additional Files tab
        files_tab = tk.Frame(notebook, bg=self.bg_color)
        notebook.add(files_tab, text="Additional Files & Folders")
        
        # Additional files frame
        add_files_frame = tk.LabelFrame(files_tab, text=" Additional Files ", 
                                       font=("Courier New", 10, "bold"),
                                       fg=self.text_color, bg=self.bg_color)
        add_files_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Listbox for additional files
        self.files_listbox = tk.Listbox(add_files_frame, width=50, height=8, 
                                       bg="#111111", fg=self.text_color)
        self.files_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollbar for listbox
        scrollbar = tk.Scrollbar(add_files_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.files_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.files_listbox.yview)
        
        # Buttons for files
        files_btn_frame = tk.Frame(add_files_frame, bg=self.bg_color)
        files_btn_frame.pack(side=tk.RIGHT, padx=5)
        
        tk.Button(files_btn_frame, text="Add Files", command=self.add_files, 
                 bg="#222222", fg=self.text_color).pack(pady=5)
        tk.Button(files_btn_frame, text="Remove Selected", command=self.remove_selected_file, 
                 bg="#222222", fg=self.text_color).pack(pady=5)
        
        # Additional folders frame
        add_folders_frame = tk.LabelFrame(files_tab, text=" Additional Folders ", 
                                         font=("Courier New", 10, "bold"),
                                         fg=self.text_color, bg=self.bg_color)
        add_folders_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Listbox for additional folders
        self.folders_listbox = tk.Listbox(add_folders_frame, width=50, height=8, 
                                         bg="#111111", fg=self.text_color)
        self.folders_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollbar for folders listbox
        scrollbar2 = tk.Scrollbar(add_folders_frame)
        scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
        self.folders_listbox.config(yscrollcommand=scrollbar2.set)
        scrollbar2.config(command=self.folders_listbox.yview)
        
        # Buttons for folders
        folders_btn_frame = tk.Frame(add_folders_frame, bg=self.bg_color)
        folders_btn_frame.pack(side=tk.RIGHT, padx=5)
        
        tk.Button(folders_btn_frame, text="Add Folder", command=self.add_folder, 
                 bg="#222222", fg=self.text_color).pack(pady=5)
        tk.Button(folders_btn_frame, text="Remove Selected", command=self.remove_selected_folder, 
                 bg="#222222", fg=self.text_color).pack(pady=5)
        
        # Console output tab
        console_tab = tk.Frame(notebook, bg=self.bg_color)
        notebook.add(console_tab, text="Console Output")
        
        self.console_output = scrolledtext.ScrolledText(console_tab, width=80, height=15, 
                                                       bg="#111111", fg=self.text_color)
        self.console_output.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.console_output.config(state=tk.DISABLED)
        
        # Convert button
        self.convert_btn = tk.Button(main_tab, text="🚀 CONVERT TO EXE 🚀", 
                               command=self.start_conversion, 
                               bg="#555555", fg=self.highlight_color,
                               font=("Courier New", 14, "bold"), state=tk.DISABLED)
        self.convert_btn.pack(pady=20)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_tab, orient=tk.HORIZONTAL, length=800, mode='indeterminate')
        self.progress.pack(pady=10)
        
        # Status label
        self.status = tk.Label(main_tab, text="Preparing...", font=("Courier New", 10), 
                              fg=self.text_color, bg=self.bg_color)
        self.status.pack(pady=5)
        
        # Branding information
        self.create_branding_frame(main_tab)
        
    def create_branding_frame(self, parent):
        branding_frame = tk.Frame(parent, relief=tk.GROOVE, bd=1, bg="#222222")
        branding_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(branding_frame, text="DarkBoss1BD - Contact Information:", 
                font=("Courier New", 10, "bold"), fg=self.accent_color, bg="#222222").pack(pady=5)
        
        for key, value in self.branding_info.items():
            info_frame = tk.Frame(branding_frame, bg="#222222")
            info_frame.pack(fill=tk.X, padx=10, pady=2)
            tk.Label(info_frame, text=f"{key}:", width=20, anchor=tk.W, 
                    fg=self.text_color, bg="#222222").pack(side=tk.LEFT)
            link = tk.Label(info_frame, text=value, fg=self.highlight_color, 
                           bg="#222222", cursor="hand2")
            link.pack(side=tk.LEFT)
            link.bind("<Button-1>", lambda e, url=value: self.open_url(url))
    
    def display_hacker_banner(self):
        banner_text = """
        ╔═══════════════════════════════════════════════════════════╗
        ║                                                           ║
        ║    ██████╗  █████╗ ██████╗ ██╗  ██╗██████╗  ██████╗ ███████╗║
        ║    ██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝██╔══██╗██╔════╝ ██╔════╝║
        ║    ██║  ██║███████║██████╔╝█████╔╝ ██████╔╝██║  ███╗███████╗║
        ║    ██║  ██║██╔══██║██╔══██╗██╔═██╗ ██╔══██╗██║   ██║╚════██║║
        ║    ██████╔╝██║  ██║██║  ██║██║  ██╗██████╔╝╚██████╔╝███████║║
        ║    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚══════╝║
        ║                                                           ║
        ║                 ADVANCED EXE CONVERTER                    ║
        ║                 WITH MULTI-FOLDER SUPPORT                 ║
        ║                                                           ║
        ╚═══════════════════════════════════════════════════════════╝
        """
        
        banner_label = tk.Label(self.root, text=banner_text, font=("Courier New", 8), 
                               fg=self.highlight_color, bg=self.bg_color, justify=tk.LEFT)
        banner_label.pack(pady=10)
    
    def open_url(self, url):
        webbrowser.open(url)
    
    def browse_file(self):
        filename = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if filename:
            self.file_path.delete(0, tk.END)
            self.file_path.insert(0, filename)
            
            # Set default output name
            if not self.output_name.get():
                base_name = os.path.basename(filename).replace('.py', '')
                self.output_name.insert(0, base_name)
    
    def browse_output_dir(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_dir.delete(0, tk.END)
            self.output_dir.insert(0, directory)
    
    def browse_icon(self):
        filename = filedialog.askopenfilename(filetypes=[("Icon Files", "*.ico")])
        if filename:
            self.icon_path.delete(0, tk.END)
            self.icon_path.insert(0, filename)
    
    def add_files(self):
        filenames = filedialog.askopenfilenames()
        for filename in filenames:
            if filename not in self.selected_files:
                self.selected_files.append(filename)
                self.files_listbox.insert(tk.END, filename)
    
    def remove_selected_file(self):
        selected = self.files_listbox.curselection()
        if selected:
            index = selected[0]
            self.selected_files.pop(index)
            self.files_listbox.delete(index)
    
    def add_folder(self):
        directory = filedialog.askdirectory()
        if directory and directory not in self.selected_folders:
            self.selected_folders.append(directory)
            self.folders_listbox.insert(tk.END, directory)
    
    def remove_selected_folder(self):
        selected = self.folders_listbox.curselection()
        if selected:
            index = selected[0]
            self.selected_folders.pop(index)
            self.folders_listbox.delete(index)
    
    def log_to_console(self, message):
        self.console_output.config(state=tk.NORMAL)
        self.console_output.insert(tk.END, message + "\n")
        self.console_output.see(tk.END)
        self.console_output.config(state=tk.DISABLED)
    
    def start_conversion(self):
        if not self.pyinstaller_available:
            messagebox.showerror("Error", "PyInstaller is not available. Please wait for installation to complete.")
            return
            
        thread = threading.Thread(target=self.convert)
        thread.daemon = True
        thread.start()
    
    def convert(self):
        python_file = self.file_path.get()
        if not python_file:
            messagebox.showerror("Error", "Please select a Python file")
            return
        
        if not os.path.exists(python_file):
            messagebox.showerror("Error", "The selected Python file does not exist")
            return
        
        # Build PyInstaller command
        cmd = [sys.executable, "-m", "PyInstaller", '--clean']
        
        if self.onefile.get():
            cmd.append('--onefile')
        
        if not self.console.get():
            cmd.append('--windowed')
        
        if self.upx.get():
            cmd.append('--upx-dir=')
        
        if self.icon_path.get():
            cmd.extend(['--icon', self.icon_path.get()])
        
        # Add additional files
        for file_path in self.selected_files:
            cmd.extend(['--add-data', f'{file_path};.'])
        
        # Add additional folders
        for folder_path in self.selected_folders:
            folder_name = os.path.basename(folder_path)
            cmd.extend(['--add-data', f'{folder_path};{folder_name}'])
        
        output_name = self.output_name.get()
        if output_name:
            cmd.extend(['--name', output_name])
        
        output_dir = self.output_dir.get()
        if output_dir:
            cmd.extend(['--distpath', output_dir])
        
        cmd.append(python_file)
        
        # Show progress
        self.progress.start(10)
        self.status.config(text="Converting... Please wait")
        self.log_to_console("Starting conversion process...")
        self.log_to_console(f"Command: {' '.join(cmd)}")
        self.root.update()
        
        try:
            # Run PyInstaller
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                      text=True, cwd=os.path.dirname(python_file))
            
            # Read output in real-time
            for line in process.stdout:
                self.log_to_console(line.strip())
            
            process.wait()
            
            if process.returncode == 0:
                self.status.config(text="Conversion completed successfully!")
                self.log_to_console("✅ EXE file created successfully!")
                messagebox.showinfo("Success", "EXE file created successfully!")
            else:
                self.status.config(text="Conversion failed")
                self.log_to_console("❌ Conversion failed!")
                messagebox.showerror("Error", "Conversion failed. Check console for details.")
        
        except Exception as e:
            self.status.config(text="Conversion failed")
            self.log_to_console(f"❌ An error occurred: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        
        finally:
            self.progress.stop()

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedPythonToExeConverter(root)
    root.mainloop()
