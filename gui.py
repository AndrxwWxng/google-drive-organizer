import tkinter as tk
from tkinter import ttk, messagebox
from sorter import get_drive_service, sort_files

class DriveGUI:
    def __init__(self, master):
        self.master = master
        master.title("Google Drive File Sorter")
        
        self.label = tk.Label(master, text="Click the button to sort your Google Drive files")
        self.label.pack(pady=10)

        self.sort_button = tk.Button(master, text="Sort Files", command=self.sort_files)
        self.sort_button.pack(pady=10)

        self.result_tree = ttk.Treeview(master, columns=('Name', 'ID'), show='headings')
        self.result_tree.heading('Name', text='File Name')
        self.result_tree.heading('ID', text='File ID')
        self.result_tree.pack(pady=10, expand=True, fill='both')

    def sort_files(self):
        try:
            service = get_drive_service()
            sorted_items = sort_files(service)
            
            # Clear previous results
            for i in self.result_tree.get_children():
                self.result_tree.delete(i)
            
            # Insert new results
            for item in sorted_items:
                self.result_tree.insert('', 'end', values=(item['name'], item['id']))
            
            messagebox.showinfo("Success", "Files sorted successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def main():
    root = tk.Tk()
    gui = DriveGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()