import pandas as pd
import tkinter as tk
from datetime import date
from tkinter import filedialog, messagebox


class App(tk.Tk):
    def __init__(self, width: int = 800, height: int = 600):
        super().__init__()
        # Window properties
        self.width, self.height = width, height
        self.name = "AV Issues"
        self.title(self.name)
        self.geometry(f"{self.width}x{self.height}")
        
        # Run the function to set up the menu bar
        self.setup_menubar()
        
        # Empty variables for later use
        self.current_file_path = None
        self.table = None
        self.df = None
        
        # Initialize the grid system
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Frame for table
        self.table_frame = tk.Frame()
        self.table_frame.grid(row=0, column=0, padx=0, pady=0, sticky='nsew')
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)
    
    def setup_menubar(self):
        # App properties
        self._author = "Chris Wright"
        self._organization = "Richland Library"
        self._sub_organization = "St. Andrews Branch"
        self._current_year = date.today().year
        self._version = "0.0.1"
        self._license = f"{self.name} v{self._version} is under the MIT license:"
        self._mit_license = f"""Copyright {self._current_year} {self._author}, {self._organization} {self._sub_organization}

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""

        # Set up the menu bar
        self.menubar = tk.Menu(self)

        # Set up the menu bar buttons
        self._file = tk.Menu(self.menubar, tearoff=0)
        self._edit = tk.Menu(self.menubar, tearoff=0)
        self._help = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self._file)
        self.menubar.add_cascade(label="Edit", menu=self._edit)
        self.menubar.add_cascade(label="Help", menu=self._help)

        # Set up the File menu's options
        self._file.add_command(label="New File", command=None)
        self._file.add_command(label="Open...", command=self.open_csv)
        self._file.add_command(label="Save", command=self.save_csv)
        self._file.add_command(label="Save As...", command=self.save_as_csv)
        self._file.add_separator()
        self._file.add_command(label="Exit", command=self.destroy)

        # Set up the Edit menu
        self._edit.add_command(label="Cut", command=None)
        self._edit.add_command(label="Copy", command=None)
        self._edit.add_command(label="Paste", command=None)
        self._edit.add_command(label="Select All", command=None)
        self._edit.add_separator()
        self._edit.add_command(label="Find...", command=None)
        self._edit.add_command(label="Find again", command=None)

        # Set up the Help menu
        self._help.add_command(label="AV Issues Help", command=None)
        self._help.add_command(label="Guide", command=None)
        self._help.add_separator()
        self._help.add_command(label="About AV Issues", command=self._about_av_issues)

        # Add the menubar to the app
        self.config(menu=self.menubar)

    def _about_av_issues(self):
        about_av_issues_string = f'{self._author}\n'
        about_av_issues_string += f'Version {self._version}\n'
        about_av_issues_string += f'© {self._author}, {self._organization} {self._sub_organization}.\n'
        about_av_issues_string += f'This product is licensed under the MIT Permissive License:\n'
        about_av_issues_string += self._mit_license
        messagebox.showinfo('About AV Issues', about_av_issues_string)
    
    def open_csv(self):
        # Ask the user for the path to the csv
        file_path = filedialog.askopenfilename(filetypes=[('CSV files', '*.csv')])
        if file_path:
            # If the file is valid, show it in the main window
            try:
                self.df = pd.read_csv(file_path)
                self.current_file_path = file_path
                self.display_csv()
                # messagebox.showinfo('Success', 'Opened CSV file')
            except Exception as e:
                messagebox.showerror('Error', f'Invalid file {file_path}. Error: {e}')
    
    def display_csv(self):
        if self.table:
            self.table.destroy()
        
        self.canvas = tk.Canvas(self.table_frame)
        self.horizontal_scrollbar = tk.Scrollbar(self.table_frame, orient='horizontal', command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=self.horizontal_scrollbar.set)
        
        self.table = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.table, anchor='nw')
        
        self.canvas.grid(row=0, column=0, sticky='nsew')
        self.horizontal_scrollbar.grid(row=1, column=0, sticky='ew')
        
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)
        
        for i, col in enumerate(self.df.columns):
            label = tk.Label(self.table, text=col, borderwidth=1, relief='solid')
            label.grid(row=0, column=i, padx=5, pady=5)
        
        for i, row in self.df.iterrows():
            for j, value in enumerate(row):
                entry = tk.Entry(self.table, borderwidth=1, relief='solid')
                entry.insert(0, value)
                entry.grid(row=i+1, column=j, padx=5, pady=5)
                entry.bind('<FocusOut>', lambda e, row=i, col=j: self.update_value(e, row, col))
        
        self.table.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox('all'))
    
    def update_value(self, event, row, col):
        new_value = event.widget.get()
        self.df.iat[row, col] = new_value
    
    def save_csv(self):
        if self.df is not None and self.current_file_path:
            try:
                self.df.to_csv(self.current_file_path, index=False)
                messagebox.showinfo('Success', 'CSV file saved')
            except Exception as e:
                messagebox.showerror('Error', f'Could not save file {self.current_file_path}. Error: {e}')
    
    def save_as_csv(self):
        if self.df is not None:
            file_path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV files', '*.csv')])
            if file_path:
                try:
                    self.df.to_csv(file_path, index=False)
                    self.current_file_path = file_path
                    messagebox.showinfo('Success', 'CSV file saved')
                except Exception as e:
                    messagebox.showerror('Error', f'Invalid {file_path}. Error: {e}')


if __name__ == "__main__":
    app = App()
    app.mainloop()
