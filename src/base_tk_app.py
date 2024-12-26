import tkinter as tk
from tkinter import filedialog, messagebox
import csv


class CSVEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('CSV Editor')
        self.geometry('800x600')
        
        self.filename = None
        self.data = []
        
        self.menu = tk.Menu(self)
        self.config(menu=self.menu)
        
        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label='File', menu=self.file_menu)
        self.file_menu.add_command(label='Open', command=self.open_file)
        self.file_menu.add_command(label='Save', command=self.save_file)
        self.file_menu.add_command(label='Exit', command=self.quit)
        
        self.grid_frame = tk.Frame(self)
        self.grid_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    
    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])
        if file_path:
            self.filename = file_path
            
            try:
                with open(file_path, newline='', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    self.data = list(reader)
                self.display_grid()
            except Exception as e:
                messagebox.showerror('Error', f'Failed to open file: {e}')
    
    def save_file(self):
        if not self.filename:
            self.filename = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV Files', '*.csv')])
            if not self.filename:
                return
        try:
            with open(self.filename, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(self.data)
            messagebox.showinfo('Success', 'File saved successfully')
        except Exception as e:
            messagebox.showerror('Error', f'Failed to save file: {e}')
    
    def display_grid(self):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        
        self.cells = []
        for i, row in enumerate(self.data):
            row_cells = []
            for j, value in enumerate(row):
                entry = tk.Entry(self.grid_frame, width=20)
                entry.grid(row=i, column=j, padx=2, pady=2)
                entry.insert(tk.END, value)
                row_cells.append(entry)
            self.cells.append(row_cells)
        
        for i in range(len(self.data)):
            self.grid_frame.grid_rowconfigure(i, weight=1)
        if self.data:
            for j in range(len(self.data[0])):
                self.grid_frame.grid_columnconfigure(j, weight=1)
    
    def get_data_from_grid(self):
        for i, row_cells in enumerate(self.cells):
            for j, entry in enumerate(row_cells):
                self.data[i][j] = entry.get()


if __name__ == '__main__':
    app = CSVEditor()
    app.mainloop()