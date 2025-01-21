import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

class FileRenamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Renamer")
        self.root.geometry("700x500")
        
        # ปรับขนาด font ให้เหมาะสมกับ macOS
        self.default_font = ('SF Pro Text', 13)
        self.root.option_add('*Font', self.default_font)
        
        # สร้าง GUI
        self.create_widgets()
        
    def create_widgets(self):
        # กรอบหลัก
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # ทำให้ frame ขยายตามหน้าต่าง
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # เลือกโฟลเดอร์
        ttk.Label(main_frame, text="Folder:").grid(row=0, column=0, sticky=tk.W)
        self.folder_path = tk.StringVar()
        folder_entry = ttk.Entry(main_frame, textvariable=self.folder_path, width=50)
        folder_entry.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))
        ttk.Button(main_frame, text="Choose Folder", 
                  command=self.browse_folder).grid(row=0, column=2, padx=(5,0))
        
        # ข้อความที่ต้องการค้นหา
        ttk.Label(main_frame, text="Find:").grid(row=1, column=0, sticky=tk.W, pady=10)
        self.old_text = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.old_text).grid(row=1, column=1, 
                                                              sticky=(tk.W, tk.E), padx=5)
        
        # ข้อความที่ต้องการแทนที่
        ttk.Label(main_frame, text="Replace:").grid(row=2, column=0, sticky=tk.W)
        self.new_text = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.new_text).grid(row=2, column=1, 
                                                              sticky=(tk.W, tk.E), padx=5)
        
        # ปุ่มแสดงตัวอย่างและเริ่มเปลี่ยนชื่อ
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=1, pady=20)
        ttk.Button(button_frame, text="Preview", 
                  command=self.preview_changes).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Rename", 
                  command=self.start_rename).pack(side=tk.LEFT, padx=5)
        
        # พื้นที่แสดงผล
        log_frame = ttk.Frame(main_frame)
        log_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = tk.Text(log_frame, height=15, width=60, wrap=tk.WORD)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.log_text.configure(yscrollcommand=scrollbar.set)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        self.folder_path.set(folder_selected)
        
    def preview_changes(self):
        folder = self.folder_path.get()
        old_text = self.old_text.get()
        new_text = self.new_text.get()
        
        if not self.validate_inputs(folder, old_text, new_text):
            return
            
        self.log_text.delete(1.0, tk.END)
        self.log_message("Preview of changes:")
        
        count = 0
        for filename in os.listdir(folder):
            if old_text in filename:
                new_filename = filename.replace(old_text, new_text)
                self.log_message(f"{filename} → {new_filename}")
                count += 1
        
        self.log_message(f"\nTotal files to be renamed: {count}")
    
    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update()
        
    def validate_inputs(self, folder, old_text, new_text):
        if not folder or not old_text or not new_text:
            messagebox.showerror("Error", "Please fill in all fields")
            return False
            
        if not os.path.exists(folder):
            messagebox.showerror("Error", f"Folder not found: {folder}")
            return False
            
        return True
        
    def start_rename(self):
        folder = self.folder_path.get()
        old_text = self.old_text.get()
        new_text = self.new_text.get()
        
        if not self.validate_inputs(folder, old_text, new_text):
            return
            
        # ถามยืนยันก่อนเปลี่ยนชื่อ
        if not messagebox.askyesno("Confirm", "Are you sure you want to rename these files?"):
            return
            
        self.log_text.delete(1.0, tk.END)
        self.log_message("Starting rename process...")
        
        count = 0
        for filename in os.listdir(folder):
            if old_text in filename:
                new_filename = filename.replace(old_text, new_text)
                old_file = os.path.join(folder, filename)
                new_file = os.path.join(folder, new_filename)
                
                try:
                    os.rename(old_file, new_file)
                    count += 1
                    self.log_message(f"Renamed: {filename} → {new_filename}")
                except Exception as e:
                    self.log_message(f"Error renaming {filename}: {str(e)}")
        
        self.log_message(f"\nComplete! Renamed {count} files")
        messagebox.showinfo("Success", f"Successfully renamed {count} files")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileRenamerApp(root)
    root.mainloop()