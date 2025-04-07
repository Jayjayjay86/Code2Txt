import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime

class Code2Txt:
    def __init__(self, root):
        self.root = root
        self.root.title("Code 2 Txt")
        self.paths = []
        
        # Configure styles
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Helvetica', 10))
        self.style.configure('TButton', font=('Helvetica', 9))
        self.style.configure('Red.TButton', foreground='red')
        self.style.configure('Green.TButton', foreground='green')
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Select Files/Folders to Convert", 
                               font=('Helvetica', 14, 'bold'))
        title_label.grid(row=0, column=0, columnspan=4, pady=(0, 10))
        
        # Path selection
        self.path_entry = ttk.Entry(main_frame, width=50)
        self.path_entry.grid(row=1, column=0, padx=5, pady=5)
        
        ttk.Button(main_frame, text="Add Files", command=self.add_files).grid(row=1, column=1, padx=5)
        ttk.Button(main_frame, text="Add Folder", command=self.add_folder).grid(row=1, column=2, padx=5)
        
        # File list
        self.file_listbox = tk.Listbox(main_frame, width=70, height=10, 
                                      selectmode=tk.EXTENDED)
        self.file_listbox.grid(row=2, column=0, columnspan=3, pady=5)
        
        # List controls
        ttk.Button(main_frame, text="Remove Selected", command=self.remove_selected, 
                  style='Red.TButton').grid(row=3, column=0, pady=5)
        ttk.Button(main_frame, text="Clear All", command=self.clear_all, 
                  style='Red.TButton').grid(row=3, column=1, pady=5)
        
        # Separator
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).grid(
            row=4, column=0, columnspan=3, sticky="ew", pady=10)
        
        # Output options
        ttk.Label(main_frame, text="Output Folder:").grid(row=5, column=0, sticky=tk.W)
        
        self.output_entry = ttk.Entry(main_frame, width=50)
        self.output_entry.grid(row=6, column=0, padx=5, pady=5)
        self.output_entry.insert(0, os.getcwd())
        
        ttk.Button(main_frame, text="Browse", command=self.browse_output).grid(
            row=6, column=1, padx=5)
        
        self.timestamp_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(main_frame, text="Add timestamp to filename", 
                       variable=self.timestamp_var).grid(
                       row=7, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Progress
        self.progress_label = ttk.Label(main_frame, text="")
        self.progress_label.grid(row=8, column=0, columnspan=3, pady=(10, 0))
        
        self.progress = ttk.Progressbar(main_frame, orient=tk.HORIZONTAL, 
                                      length=400, mode='determinate')
        self.progress.grid(row=9, column=0, columnspan=3, pady=5)
        
        # Action buttons
        ttk.Button(main_frame, text="Convert", command=self.convert_files, 
                  style='Green.TButton').grid(row=10, column=1, pady=10)
        ttk.Button(main_frame, text="Exit", command=self.root.quit).grid(
            row=10, column=2, pady=10)
    
    def add_files(self):
        files = filedialog.askopenfilenames()
        if files:
            self.paths.extend(files)
            self.update_listbox()
            self.path_entry.delete(0, tk.END)
    
    def add_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.paths.append(folder)
            self.update_listbox()
            self.path_entry.delete(0, tk.END)
    
    def browse_output(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, folder)
    
    def remove_selected(self):
        selected = self.file_listbox.curselection()
        for i in reversed(selected):
            del self.paths[i]
        self.update_listbox()
    
    def clear_all(self):
        self.paths = []
        self.update_listbox()
    
    def update_listbox(self):
        self.file_listbox.delete(0, tk.END)
        for path in self.paths:
            self.file_listbox.insert(tk.END, path)
    
    def write_file_structure(self, path, output_file, base_path):
        """Write the directory structure to the output file"""
        relative_path = os.path.relpath(path, base_path)
        indent = '    ' * (len(relative_path.split(os.sep)) - 1)
        
        if os.path.isdir(path):
            with open(output_file, 'a', encoding='utf-8') as out:
                out.write(f"{indent}📁 {os.path.basename(path)}/\n")
        else:
            with open(output_file, 'a', encoding='utf-8') as out:
                out.write(f"{indent}📄 {os.path.basename(path)}\n")
    
    def process_file(self, file_path, output_file, base_path):
        try:
            relative_path = os.path.relpath(file_path, base_path)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            with open(output_file, 'a', encoding='utf-8') as out:
                out.write(f"\n\n# File: {relative_path}\n")
                out.write("#" * 50 + "\n")
                out.write(content)
                out.write("\n")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process {file_path}\nError: {str(e)}")
            return False
    
    def process_directory(self, directory, output_file, base_path):
        ignored_dirs = {'node_modules', '__pycache__', '.git'}
        ignored_files = ('package-lock.json', '.DS_Store')
        extensions = ('.py', '.js', '.jsx', '.json', '.txt', '.html', '.css')
        
        # First pass: count files and write structure
        total_files = 0
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in ignored_dirs]
            for file in files:
                if file.endswith(ignored_files):
                    continue
                if file.endswith(extensions):
                    file_path = os.path.join(root, file)
                    self.write_file_structure(file_path, output_file, base_path)
                    total_files += 1
        
        # Second pass: process file contents
        processed = 0
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in ignored_dirs]
            for file in files:
                if file.endswith(ignored_files):
                    continue
                if file.endswith(extensions):
                    file_path = os.path.join(root, file)
                    if self.process_file(file_path, output_file, base_path):
                        processed += 1
                        progress = (processed / total_files) * 100
                        self.progress['value'] = progress
                        self.progress_label.config(
                            text=f"Processing: {processed}/{total_files} files")
                        self.root.update_idletasks()
        return processed
    
    def convert_files(self):
        if not self.paths:
            messagebox.showwarning("Warning", "No files or folders selected")
            return
        
        out_folder = self.output_entry.get() or os.path.dirname(self.paths[0])
        base_name = "combined_output"
        
        if self.timestamp_var.get():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_name += f"_{timestamp}"
        
        output_file = os.path.join(out_folder, f"{base_name}.txt")
        
        try:
            # Initialize output file
            with open(output_file, 'w', encoding='utf-8') as out:
                out.write("=== FILE STRUCTURE ===\n\n")
                # Write base paths first
                for path in self.paths:
                    if os.path.isdir(path):
                        out.write(f"📁 {os.path.basename(path)}/\n")
                    else:
                        out.write(f"📄 {os.path.basename(path)}\n")
                out.write("\n\n=== FILE CONTENTS ===\n\n")
            
            total_processed = 0
            for path in self.paths:
                base_path = os.path.dirname(path) if os.path.isfile(path) else path
                if os.path.isfile(path):
                    if path.endswith(('.py', '.js', '.jsx', '.json', '.txt', '.html', '.css')):
                        if self.process_file(path, output_file, base_path):
                            total_processed += 1
                elif os.path.isdir(path):
                    total_processed += self.process_directory(path, output_file, path)
            
            messagebox.showinfo(
                "Conversion Complete",
                f"Processed {total_processed} files\n"
                f"Output saved to:\n{output_file}"
            )
            
            # Reset progress
            self.progress['value'] = 0
            self.progress_label.config(text="")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create output file:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Code2Txt(root)
    root.mainloop()