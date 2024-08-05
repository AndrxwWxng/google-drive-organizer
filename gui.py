import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.simpledialog import askstring
from sorter import get_drive_service, search_files, create_folder, move_files_to_folder

class GUI:
    def __init__(self, master):
        self.master = master
        master.title("Google Drive File Sorter")
        
        self.label = tk.Label(master, text="Enter a keyword to search your Google Drive for files")
        self.label.pack(pady=10)

        self.keyword_entry = tk.Entry(master, width=30)
        self.keyword_entry.pack(pady=10)

        self.search_button = tk.Button(master, text="Search Files", command=self.search_files)
        self.search_button.pack(pady=10)

        self.create_folder_button = tk.Button(master, text="Create Folder and Move Files", command=self.create_folder_and_move_files)
        self.create_folder_button.pack(pady=10)

        self.result_tree = ttk.Treeview(master, columns=('Name', 'ID'), show='headings', selectmode='extended')
        self.result_tree.heading('Name', text='File Name')
        self.result_tree.heading('ID', text='File ID')
        self.result_tree.pack(pady=10, expand=True, fill='both')

    def search_files(self):
        keyword = self.keyword_entry.get().strip()
        if not keyword:
            messagebox.showwarning("Warning", "Please enter a keyword.")
            return

        self.search_button.config(state=tk.DISABLED)
        self.create_folder_button.config(state=tk.DISABLED)
        
        try:
            service = get_drive_service()
            self.searched_items = search_files(service, keyword) 
            
            for i in self.result_tree.get_children():
                self.result_tree.delete(i)
            
            for item in self.searched_items:
                self.result_tree.insert('', 'end', values=(item['name'], item['id']))
            
            messagebox.showinfo("Success", f"Files searched by keyword '{keyword}' successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            self.search_button.config(state=tk.NORMAL)
            self.create_folder_button.config(state=tk.NORMAL)

    def create_folder_and_move_files(self):
        selected_items = self.result_tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "Please select at least one file.")
            return

        folder_name = askstring("Folder Name", "Enter the name for the new folder:")
        if not folder_name:
            messagebox.showwarning("Warning", "Please enter a folder name.")
            return

        try:
            service = get_drive_service()
            folder_id = create_folder(service, folder_name)
            file_ids = [self.result_tree.item(item, 'values')[1] for item in selected_items]
            move_files_to_folder(service, file_ids, folder_id)
            messagebox.showinfo("Success", "Folder created and files moved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def main():
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
