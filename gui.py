import tkinter as tk
from tkinter import ttk, messagebox
from sorter import get_drive_service, search_files

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

        self.result_tree = ttk.Treeview(master, columns=('Name', 'ID'), show='headings')
        self.result_tree.heading('Name', text='File Name')
        self.result_tree.heading('ID', text='File ID')
        self.result_tree.pack(pady=10, expand=True, fill='both')

    def search_files(self):
        keyword = self.keyword_entry.get().strip()
        if not keyword:
            messagebox.showwarning("Warning", "Please enter a keyword.")
            return

        try:
            service = get_drive_service()
            searched_items = search_files(service, keyword)
            
            # Clear previous results
            for i in self.result_tree.get_children():
                self.result_tree.delete(i)
            
            # Insert new results
            for item in searched_items:
                self.result_tree.insert('', 'end', values=(item['name'], item['id']))
            
            messagebox.showinfo("Success", f"Files searched by keyword '{keyword}' successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def main():
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()