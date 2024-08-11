from tkinter import font, messagebox, ttk
import tkinter as tk
from sorter import get_drive_service, search_folders


class FolderSelectionDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Select Folder")
        self.geometry("800x500")
        self.result = None
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.content_font = font.Font(family="Helvetica", size=12)

        self.label = ttk.Label(self, text="Select a folder to move files to:", font=self.content_font)
        self.label.pack(pady=10)

        self.search_frame = ttk.Frame(self)
        self.search_frame.pack(fill="x", padx=10, pady=5)

        self.search_container = ttk.Frame(self.search_frame)
        self.search_container.pack(expand=True)

        self.search_entry = ttk.Entry(self.search_container, width=40, font=self.content_font)
        self.search_entry.pack(side="left", padx=(0, 5))

        self.search_button = ttk.Button(self.search_container, text="Search", command=self.search_folders)
        self.search_button.pack(side="left")

        self.folder_tree = ttk.Treeview(self, columns=('Name', 'ID'), show='headings', selectmode='browse')
        self.folder_tree.heading('Name', text='Folder Name')
        self.folder_tree.heading('ID', text='Folder ID')
        self.folder_tree.column('Name', width=300)
        self.folder_tree.column('ID', width=300)
        self.folder_tree.pack(expand=True, fill="both", padx=10, pady=10)

        self.select_button = ttk.Button(self, text="Select", command=self.on_select)
        self.select_button.pack(pady=10)

        self.populate_folders()

    def populate_folders(self, keyword=""):
        try:
            service = get_drive_service()
            folders = search_folders(service, keyword)
            self.folder_tree.delete(*self.folder_tree.get_children())
            for folder in folders:
                self.folder_tree.insert('', 'end', values=(folder['name'], folder['id']))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while fetching folders: {str(e)}")

    def search_folders(self):
        keyword = self.search_entry.get().strip()
        self.populate_folders(keyword)

    def on_select(self):
        selected_item = self.folder_tree.selection()
        if selected_item:
            self.result = self.folder_tree.item(selected_item[0], 'values')[1]
            self.destroy()
        else:
            messagebox.showwarning("Warning", "Please select a folder.")
    def on_close(self):
        self.result = None
        self.destroy()

