import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.simpledialog import askstring
from sorter import get_drive_service, search_files, search_folders, create_folder, move_files_to_folder

class GUI:
    def __init__(self, master):
        self.master = master
        master.title("Google Drive File Sorter")
        
        self.label = tk.Label(master, text="Enter a keyword to search your Google Drive")
        self.label.pack(pady=10)

        self.keyword_entry = tk.Entry(master, width=30)
        self.keyword_entry.pack(pady=10)

        self.search_files_button = tk.Button(master, text="Search Files", command=lambda: self.search_items('files'))
        self.search_files_button.pack(pady=5)

        self.search_folders_button = tk.Button(master, text="Search Folders", command=lambda: self.search_items('folders'))
        self.search_folders_button.pack(pady=5)

        self.create_folder_button = tk.Button(master, text="Create New Folder and Move Files", command=self.create_folder_and_move_files)
        self.create_folder_button.pack(pady=5)

        self.move_to_existing_folder_button = tk.Button(master, text="Move to Existing Folder", command=self.move_to_existing_folder)
        self.move_to_existing_folder_button.pack(pady=5)

        self.result_tree = ttk.Treeview(master, columns=('Name', 'ID'), show='headings', selectmode='extended')
        self.result_tree.heading('Name', text='Name')
        self.result_tree.heading('ID', text='ID')
        self.result_tree.pack(pady=10, expand=True, fill='both')

        self.searched_items = []
        self.last_search_type = None

    def search_items(self, item_type):
        keyword = self.keyword_entry.get().strip()
        if not keyword:
            messagebox.showwarning("Warning", "Please enter a keyword.")
            return

        self.search_files_button.config(state=tk.DISABLED)
        self.search_folders_button.config(state=tk.DISABLED)
        self.create_folder_button.config(state=tk.DISABLED)
        self.move_to_existing_folder_button.config(state=tk.DISABLED)
        
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
            self.create_folder_button.config(state=tk.NORMAL)
            self.move_to_existing_folder_button.config(state=tk.NORMAL)

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
        selected_items = self.result_tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "Please select at least one file.")
            return

        if create_new:
            folder_name = askstring("Folder Name", "Enter the name for the new folder:")
            if not folder_name:
                messagebox.showwarning("Warning", "Please enter a folder name.")
                return
        else:
            folder_id = askstring("Folder ID", "Enter the ID of the existing folder:")
            if not folder_id:
                messagebox.showwarning("Warning", "Please enter a folder ID.")
                return

        try:
            service = get_drive_service()
            if create_new:
                folder_id = create_folder(service, folder_name)
            file_ids = [self.result_tree.item(item, 'values')[1] for item in selected_items]
            move_files_to_folder(service, file_ids, folder_id)
            messagebox.showinfo("Success", "Files moved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def main():
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()