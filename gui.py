import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.simpledialog import askstring
from sorter import get_drive_service, search_files, search_folders, create_folder, move_files_to_folder
import sv_ttk

class GUI:
    def __init__(self, master):
        self.master = master
        master.title("Google Drive File Sorter")
        master.geometry("800x600")
        master.configure(bg="#f0f0f0")
        
        # self.style = ttk.Style()
        # self.style.theme_use("clam")
        # self.style.configure("TButton", padding=6, relief="flat", background="#4CAF50", foreground="white")
        # self.style.map("TButton", background=[('active', '#45a049')])
        self.sv_ttk = sv_ttk
        self.sv_ttk.set_theme("dark")
        
        self.main_frame = ttk.Frame(master, padding="10")
        self.main_frame.pack(expand=True, fill="both")
        
        self.label = ttk.Label(self.main_frame, text="Enter a keyword to search your Google Drive", font=("Arial", 14))
        self.label.grid(row=0, column=0, columnspan=3, pady=10)

        self.keyword_entry = ttk.Entry(self.main_frame, width=40, font=("Arial", 12))
        self.keyword_entry.grid(row=1, column=0, columnspan=3, pady=10)

        self.search_files_button = ttk.Button(self.main_frame, text="Search Files", command=lambda: self.search_items('files'))
        self.search_files_button.grid(row=2, column=0, pady=5, padx=5, sticky="ew")

        self.search_folders_button = ttk.Button(self.main_frame, text="Search Folders", command=lambda: self.search_items('folders'))
        self.search_folders_button.grid(row=2, column=1, pady=5, padx=5, sticky="ew")

        self.select_all_button = ttk.Button(self.main_frame, text="Select All", command=self.select_all)
        self.select_all_button.grid(row=2, column=2, pady=5, padx=5, sticky="ew")

        self.result_tree = ttk.Treeview(self.main_frame, columns=('Name', 'ID'), show='headings', selectmode='extended')
        self.result_tree.heading('Name', text='Name')
        self.result_tree.heading('ID', text='ID')
        self.result_tree.column('Name', width=300)
        self.result_tree.column('ID', width=300)
        self.result_tree.grid(row=3, column=0, columnspan=3, pady=10, sticky="nsew")

        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.result_tree.yview)
        self.scrollbar.grid(row=3, column=3, sticky="ns")
        self.result_tree.configure(yscrollcommand=self.scrollbar.set)

        self.create_folder_button = ttk.Button(self.main_frame, text="Create New Folder and Move Files", command=self.create_folder_and_move_files)
        self.create_folder_button.grid(row=4, column=0, pady=5, padx=5, sticky="ew")

        self.move_to_existing_folder_button = ttk.Button(self.main_frame, text="Move to Existing Folder", command=self.move_to_existing_folder)
        self.move_to_existing_folder_button.grid(row=4, column=1, columnspan=2, pady=5, padx=5, sticky="ew")

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(2, weight=1)
        self.main_frame.grid_rowconfigure(3, weight=1)

        self.searched_items = []
        self.last_search_type = None

    def search_items(self, item_type):
        keyword = self.keyword_entry.get().strip()
        if not keyword:
            messagebox.showwarning("Warning", "Please enter a keyword.")
            return

        self.search_files_button.config(state=tk.DISABLED)
        self.search_folders_button.config(state=tk.DISABLED)
        
        try:
            service = get_drive_service()
            if item_type == 'files':
                self.searched_items = search_files(service, keyword)
            else:
                self.searched_items = search_folders(service, keyword)
            
            self.last_search_type = item_type
            
            for i in self.result_tree.get_children():
                self.result_tree.delete(i)
            
            for item in self.searched_items:
                self.result_tree.insert('', 'end', values=(item['name'], item['id']))
            
            messagebox.showinfo("Success", f"{item_type.capitalize()} searched by keyword '{keyword}' successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            self.search_files_button.config(state=tk.NORMAL)
            self.search_folders_button.config(state=tk.NORMAL)

    def select_all(self):
        self.result_tree.selection_set(self.result_tree.get_children())

    def create_folder_and_move_files(self):
        if self.last_search_type != 'files':
            messagebox.showwarning("Warning", "Please search for files first.")
            return
        self._move_files(create_new=True)

    def move_to_existing_folder(self):
        if self.last_search_type != 'files':
            messagebox.showwarning("Warning", "Please search for files first.")
            return
        self._move_files(create_new=False)

    def _move_files(self, create_new):
        selected_files = self.result_tree.selection()
        if not selected_files:
            messagebox.showwarning("Warning", "Please select at least one file.")
            return

        if create_new:
            folder_name = askstring("Folder Name", "Enter the name for the new folder:")
            if not folder_name:
                messagebox.showwarning("Warning", "Please enter a folder name.")
                return
        else:
            folder_selection = FolderSelectionDialog(self.master)
            if folder_selection.result is None:
                return
            folder_id = folder_selection.result

        try:
            service = get_drive_service()
            if create_new:
                folder_id = create_folder(service, folder_name)
            file_ids = [self.result_tree.item(item, 'values')[1] for item in selected_files]
            move_files_to_folder(service, file_ids, folder_id)
            messagebox.showinfo("Success", "Files moved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

class FolderSelectionDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Select Folder")
        self.geometry("400x300")
        self.result = None

        self.label = ttk.Label(self, text="Select a folder to move files to:", font=("Arial", 12))
        self.label.pack(pady=10)

        self.folder_tree = ttk.Treeview(self, columns=('Name', 'ID'), show='headings', selectmode='browse')
        self.folder_tree.heading('Name', text='Folder Name')
        self.folder_tree.heading('ID', text='Folder ID')
        self.folder_tree.column('Name', width=200)
        self.folder_tree.column('ID', width=200)
        self.folder_tree.pack(expand=True, fill="both", padx=10, pady=10)

        self.select_button = ttk.Button(self, text="Select", command=self.on_select)
        self.select_button.pack(pady=10)

        self.populate_folders()

    def populate_folders(self):
        try:
            service = get_drive_service()
            folders = search_folders(service, "")  # Empty string to get all folders
            for folder in folders:
                self.folder_tree.insert('', 'end', values=(folder['name'], folder['id']))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while fetching folders: {str(e)}")

    def on_select(self):
        selected_item = self.folder_tree.selection()
        if selected_item:
            self.result = self.folder_tree.item(selected_item[0], 'values')[1]
            self.destroy()
        else:
            messagebox.showwarning("Warning", "Please select a folder.")

def main():
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()