import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

try:
    import customtkinter as ctk
    from PIL import Image, ImageTk
except ImportError:
    import sys
    import tkinter.messagebox as messagebox
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Premium Design (CustomTkinter)", 
        "To enable the premium design, please install the required libraries.\n\n"
        "Open your terminal and type:\n"
        "pip install customtkinter pillow\n\nThen run main.py again!")
    sys.exit(1)

from config import *
from organizer import get_files, generate_preview, execute_organization

ctk.set_appearance_mode("dark")

class PhotoOrganizerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Photo Organizer - Made by.leandr0")
        self.geometry("1250x700")
        
        self.configure(fg_color=BG_COLOR)
        
        self.original_files = []
        self.preview_data = []
        self.img_reference = None
        
        self.setup_ui()
        
    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1, minsize=320)
        self.grid_columnconfigure(1, weight=2, minsize=450)
        self.grid_columnconfigure(2, weight=1, minsize=350)
        self.grid_rowconfigure(0, weight=1)
        

        self.frame_left = ctk.CTkFrame(self, fg_color=PANEL_COLOR, corner_radius=15)
        self.frame_left.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        ctk.CTkLabel(self.frame_left, text="📸 Organizer", font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold"), text_color=ACCENT_COLOR).pack(pady=(35, 40), anchor="center")
        
        ctk.CTkLabel(self.frame_left, text="1. Target Folder", font=ctk.CTkFont(size=14, weight="bold"), text_color=TEXT_COLOR).pack(anchor="w", padx=25)
        self.entry_folder = ctk.CTkEntry(self.frame_left, placeholder_text="Folder path...", height=42, corner_radius=8, border_width=1, fg_color="#22222B")
        self.entry_folder.pack(fill="x", padx=25, pady=(5, 10))
        self.btn_folder = ctk.CTkButton(self.frame_left, text="Browse Folder", fg_color=ACCENT_COLOR, text_color="#1E1E24", hover_color="#E6CCB2", font=ctk.CTkFont(weight="bold"), height=35, corner_radius=8, command=self.choose_folder)
        self.btn_folder.pack(fill="x", padx=25, pady=(0, 30))
        
        ctk.CTkLabel(self.frame_left, text="2. Project Name", font=ctk.CTkFont(size=14, weight="bold"), text_color=TEXT_COLOR).pack(anchor="w", padx=25)
        self.entry_project = ctk.CTkEntry(self.frame_left, placeholder_text="Ex: John_Wedding", height=42, corner_radius=8, border_width=1, fg_color="#22222B")
        self.entry_project.pack(fill="x", padx=25, pady=(5, 30))
        
        ctk.CTkLabel(self.frame_left, text="3. Prefix (Auto-numbered)", font=ctk.CTkFont(size=14, weight="bold"), text_color=TEXT_COLOR).pack(anchor="w", padx=25)
        self.entry_prefix = ctk.CTkEntry(self.frame_left, placeholder_text="Ex: Client_", height=42, corner_radius=8, border_width=1, fg_color="#22222B")
        self.entry_prefix.pack(fill="x", padx=25, pady=(5, 45))
        
        self.btn_preview = ctk.CTkButton(self.frame_left, text="👀 PREVIEW ALL", fg_color="#F4A261", hover_color="#E76F51", text_color="white", font=ctk.CTkFont(size=14, weight="bold"), height=45, corner_radius=8, command=self.do_preview)
        self.btn_preview.pack(fill="x", padx=25, pady=10)
        
        self.btn_organize = ctk.CTkButton(self.frame_left, text="🚀 ORGANIZE NOW", fg_color=ACTION_COLOR, hover_color="#52796F", text_color="white", font=ctk.CTkFont(size=15, weight="bold"), height=50, corner_radius=8, state="disabled", command=self.start_organization)
        self.btn_organize.pack(fill="x", padx=25, pady=10)
        
        
        self.frame_center = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_center.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="nsew")
        
        ctk.CTkLabel(self.frame_center, text="File List", font=ctk.CTkFont(size=18, weight="bold"), text_color=TEXT_COLOR).pack(anchor="w", pady=(0, 15))
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=PANEL_COLOR, foreground=TEXT_COLOR, fieldbackground=PANEL_COLOR, rowheight=40, borderwidth=0, font=("Segoe UI", 11))
        style.configure("Treeview.Heading", background="#22222B", foreground=ACCENT_COLOR, font=("Segoe UI", 12, "bold"), borderwidth=0, padding=8)
        style.map("Treeview", background=[("selected", ACCENT_COLOR)], foreground=[("selected", "#1E1E24")])
        
        table_frame = ctk.CTkFrame(self.frame_center, corner_radius=10, fg_color=PANEL_COLOR)
        table_frame.pack(fill="both", expand=True)
        
        columns = ("original", "new_name", "status")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        
        self.table.heading("original", text=" Current File")
        self.table.heading("new_name", text=" New Name")
        self.table.heading("status", text=" Status")
        
        self.table.column("original", width=120, anchor="w")
        self.table.column("new_name", width=120, anchor="w")
        self.table.column("status", width=120, anchor="w")
        
        self.table.tag_configure('conflict', foreground=WARNING_COLOR)
        self.table.tag_configure('success', foreground=ACTION_COLOR)
        self.table.tag_configure('error', foreground=WARNING_COLOR)
        
        self.table.bind("<<TreeviewSelect>>", self.on_photo_select)
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.table.yview)
        self.table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y", pady=10, padx=(0,10))
        self.table.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        

        self.frame_right = ctk.CTkFrame(self, fg_color=PANEL_COLOR, corner_radius=15)
        self.frame_right.grid(row=0, column=2, padx=(0, 20), pady=20, sticky="nsew")
        
        ctk.CTkLabel(self.frame_right, text="Visual Details", font=ctk.CTkFont(size=18, weight="bold"), text_color=TEXT_COLOR).pack(anchor="center", pady=(35, 25))
        
        self.frame_image = ctk.CTkFrame(self.frame_right, fg_color="#1A1A20", corner_radius=15, width=280, height=280)
        self.frame_image.pack(pady=(0, 30), padx=25)
        self.frame_image.pack_propagate(False)
        
        self.lbl_image = ctk.CTkLabel(self.frame_image, text="🖼️\nSelect a photo\nin the list", text_color="#6c757d", font=ctk.CTkFont(size=15))
        self.lbl_image.place(relx=0.5, rely=0.5, anchor="center")
        
        self.lbl_detail_orig = ctk.CTkLabel(self.frame_right, text="Original: ---", font=ctk.CTkFont(size=13), text_color=TEXT_COLOR, justify="left", wraplength=250)
        self.lbl_detail_orig.pack(anchor="w", padx=30, pady=8)
        
        self.lbl_detail_new = ctk.CTkLabel(self.frame_right, text="New: ---", font=ctk.CTkFont(size=15, weight="bold"), text_color=ACCENT_COLOR, justify="left", wraplength=250)
        self.lbl_detail_new.pack(anchor="w", padx=30, pady=8)
        
        self.lbl_detail_status = ctk.CTkLabel(self.frame_right, text="Status: ---", font=ctk.CTkFont(size=13), text_color="#E9C46A", justify="left", wraplength=250)
        self.lbl_detail_status.pack(anchor="w", padx=30, pady=8)

    def on_photo_select(self, event):
        selection = self.table.selection()
        if not selection: return
        
        values = self.table.item(selection[0], 'values')
        original, new_name, status = values
        
        self.lbl_detail_orig.configure(text=f"Original: {original}")
        self.lbl_detail_new.configure(text=f"New: {new_name}")
        self.lbl_detail_status.configure(text=f"Status: {status}")
        
        folder = self.entry_folder.get()
        if not folder: return
        
        img_path = os.path.join(folder, original)
        try:
            img_pil = Image.open(img_path)
            img_pil.thumbnail((260, 260))
            self.img_reference = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=img_pil.size)
            self.lbl_image.configure(image=self.img_reference, text="")
        except Exception:
            self.lbl_image.configure(image="", text="🚫\nFormat not\nsupported")
            
    def choose_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.entry_folder.delete(0, "end")
            self.entry_folder.insert(0, folder)
            self.load_files(folder)
            
    def load_files(self, folder):
        for item in self.table.get_children(): self.table.delete(item)
        self.original_files.clear()
        self.preview_data.clear()
        self.btn_organize.configure(state="disabled")
        
        try:
            files = get_files(folder)
            self.original_files = files
            for f, ext in files:
                self.table.insert("", "end", values=(f, "---", "Ready for preview"))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def do_preview(self):
        folder = self.entry_folder.get()
        project = self.entry_project.get()
        prefix = self.entry_prefix.get()
        
        if not folder or not project or not prefix:
            messagebox.showwarning("Warning", "Please fill in all fields on the left!")
            return
            
        if not self.original_files: return

        self.preview_data = generate_preview(folder, project, prefix, self.original_files)
        
        for item in self.table.get_children(): self.table.delete(item)
            
        conflicts = 0
        for item in self.preview_data:
            tag = 'conflict' if item['conflict'] else ''
            if item['conflict']: conflicts += 1
            self.table.insert("", "end", values=(item['original'], item['new_name'], item['status']), tags=(tag,))
            
        if conflicts > 0:
            messagebox.showwarning("Conflicts Detected", f"Warning! {conflicts} files with the new names already exist in the target folder.\nIf you organize now, they will be overwritten.")
            
        self.btn_organize.configure(state="normal")

    def start_organization(self):
        if not self.preview_data: return
            
        conflicts = sum(1 for p in self.preview_data if p['conflict'])
        msg = f"You are about to organize {len(self.preview_data)} photos.\n"
        if conflicts > 0: msg += f"⚠️ {conflicts} conflicts will be overwritten!\n"
        msg += "\nDo you wish to continue?"
        
        if messagebox.askyesno("Final Confirmation", msg):
            successes, errors = execute_organization(self.preview_data)
            
            for item_id, data in zip(self.table.get_children(), self.preview_data):
                tag = 'success' if '✅' in data['status'] else 'error'
                self.table.item(item_id, values=(data['original'], data['new_name'], data['status']), tags=(tag,))
                
            messagebox.showinfo("Success", f"Process Complete!\n✅ Successes: {successes}\n❌ Errors: {errors}")
            self.original_files.clear()
            self.preview_data.clear()
            self.btn_organize.configure(state="disabled")
