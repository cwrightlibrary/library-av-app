import csv, darkdetect, json, os, platform, pyglet
import pandas as pd
import tkinter as tk
from converters import Converter
from custom_windows import CustomWindow
from datetime import date
from mit_license import mit_license
from tkinter import filedialog, messagebox, PhotoImage


class AVApp(tk.Tk):
    def __init__(self, width: int = 1000, height: int = 625):
        super().__init__()

        self.width, self.height = width, height
        self.name = "AV Issues"
        self.title(self.name)
        self.geometry(f"{self.width}x{self.height}")

        if platform.system() == "Windows":
            self.iconbitmap(default="src/icons/icon_128.ico")
        else:
            self.app_icon = PhotoImage(file="src/icons/icon_128.png")
            self.iconphoto(True, self.app_icon)

        self.recent_files = self.load_recent_files()

        self.setup_menubar()

        self.current_file_path = None
        self.table = None
        self.df = None

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frame_issues = tk.Frame()
        self.frame_issues.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.frame_issues.grid_rowconfigure(0, weight=1)
        self.frame_issues.grid_columnconfigure(0, weight=1)
        
        self._cell_font = ("#000000", "#ffffff")
        self._cell_border = ("#d4d4d4", "#262626")
        self._cell_bg_inactive = ("#ffffff", "#000000")
        self._cell_bg_active = ("#e9e9e9", "#181818")
        
        self._library_darker = "#007492"
        self._library_dark = "#007e9e"
        self._library_light = "#0092b0"
        self._library_lighter = "#00afd0"
        
        cdir = os.path.dirname(os.path.abspath(__file__))
        inter_reg_path = os.path.join(cdir, "fonts", "Inter-Regular.ttf")
        inter_bold_path = os.path.join(cdir, "fonts", "Inter-Bold.ttf")
        pyglet.font.add_file(inter_reg_path)
        pyglet.font.add_file(inter_bold_path)
        
        self.fonts = {
            "INTER_REG": ("Inter Regular", 10),
            "INTER_BOLD": ("Inter Bold", 10, "bold")
        }

        if self.recent_files:
            self.open_csv_from_recent(self.recent_files[0])
        else:
            self.display_empty()

        self.mainloop()

    def setup_menubar(self):
        self.app_name = "AV Issues"
        self.app_author = "Chris Wright"
        self.app_organization = "Richland Library"
        self.app_sub_organization = "St. Andrews"
        self.app_current_year = date.today().year
        self.app_version = "0.0.1"
        self.app_license = (
            f"{self.app_name} v{self.app_version} is under the MIT license:"
        )
        self.app_mit_license = mit_license(
            self.app_current_year,
            self.app_author,
            self.app_organization,
            self.app_sub_organization,
        )

        self.MENUBAR = tk.Menu(self)

        self.FILE_MENU = tk.Menu(self.MENUBAR, tearoff=0)
        self.EDIT_MENU = tk.Menu(self.MENUBAR, tearoff=0)
        self.HELP_MENU = tk.Menu(self.MENUBAR, tearoff=0)
        self.MENUBAR.add_cascade(label="File", menu=self.FILE_MENU)
        self.MENUBAR.add_cascade(label="Edit", menu=self.EDIT_MENU)
        self.MENUBAR.add_cascade(label="Help", menu=self.HELP_MENU)

        self.FILE_MENU.add_command(label="new File", command=None)
        self.FILE_MENU.add_command(label="Open...", command=self.open_csv)
        self.FILE_MENU.add_command(label="Save", command=self.save_csv)
        self.FILE_MENU.add_command(label="Save As...", command=self.save_as_csv)
        self.FILE_MENU.add_separator()
        self.FILE_MENU.add_command(label="Convert...", command=self.convert_csv)

        self.RECENT_MENU = tk.Menu(self.FILE_MENU, tearoff=0)
        self.FILE_MENU.add_cascade(label="Recently Opened", menu=self.RECENT_MENU)
        self.update_recent_files_menu()

        self.FILE_MENU.add_separator()
        self.FILE_MENU.add_command(label="Exit", command=self.destroy)

        self.EDIT_MENU.add_command(label="Cut", command=None)
        self.EDIT_MENU.add_command(label="Copy", command=None)
        self.EDIT_MENU.add_command(label="Paste", command=None)
        self.EDIT_MENU.add_command(label="Select All", command=None)
        self.EDIT_MENU.add_separator()
        self.EDIT_MENU.add_command(label="Find...", command=None)
        self.EDIT_MENU.add_command(label="Replace...", command=None)

        self.HELP_MENU.add_command(label="AV Issues Help", command=None)
        self.HELP_MENU.add_command(label="Documentation", command=None)
        self.HELP_MENU.add_separator()
        self.HELP_MENU.add_command(
            label="About AV Issues", command=self.about_av_issues
        )

        self.config(menu=self.MENUBAR)

    def about_av_issues(self):
        about_string = f"{self.app_author}\n\n"
        about_string += f"{self.app_name} version {self.app_version}\n"
        about_string += f"© {self.app_author}, {self.app_organization} {self.app_sub_organization}. \n\n"
        about_string += f"This product is licensed under the MIT Permissive License:\n"
        about_string += self.app_mit_license

        about_window = CustomWindow()
        about_window.custom_showinfo(
            "About AV Issues", "src/icons/icon_128.png", about_string
        )

    def open_csv(self):
        file_path = filedialog.askopenfile(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            try:
                self.df = pd.read_csv(file_path)
                self.current_file_path = file_path
                self.display_csv()
            except Exception as e:
                messagebox.showerror("Error", f"Invalid file {file_path}. Error: {e}")

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def on_shift_mousewheel(self, event):
        self.canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

    def on_ctrl_mousewheel(self, event):
        self.canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

    def update_value(self, event, row, col):
        new_value = event.widget.get()
        self.df.iat[row, col] = new_value

    def save_csv(self):
        if self.df is not None and self.current_file_path:
            try:
                self.df.to_csv(self.current_file_path, index=False)
                messagebox.showinfo("Success", "CSV file saved")
            except Exception as e:
                messagebox.showerror(
                    "Error", f"Could not save file {self.current_file_path}. Error: {e}"
                )

    def save_as_csv(self):
        if self.df is not None:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv", filetypes=[("CSV Files", "*.csv")]
            )
            if file_path:
                try:
                    self.df.to_csv(file_path, index=False)
                    self.current_file_path = file_path
                    messagebox.showinfo("Success", "CSV file saved")
                except Exception as e:
                    messagebox.showerror("Error", f"Invalid {file_path}. Error: {e}")

    def convert_csv(self):
        file_path = filedialog.askopenfile(filetypes=[("Excel Files", "*.xlsx")])
        if file_path:
            try:
                csv_file_path = file_path.name.replace(".xlsx", ".csv")
                converter = Converter()
                converter.excel_to_csv(
                    excel_path=file_path.name,
                    sheet_name="av_issues",
                    csv_path=csv_file_path,
                )
                self.df = pd.read_csv(csv_file_path)
                self.current_file_path = csv_file_path
                self.display_csv()
            except Exception as e:
                messagebox.showerror(
                    "Error", f"Unable to convert {file_path.name}. Error: {e}"
                )

    def update_recent_files(self, file_path):
        if file_path in self.recent_files:
            self.recent_files.remove(file_path)
        self.recent_files.insert(0, file_path)
        if len(self.recent_files) > 5:
            self.recent_files = self.recent_files[:5]
        self.save_recent_files()
        self.update_recent_files_menu()

    def update_recent_files_menu(self):
        self.RECENT_MENU.delete(0, tk.END)
        for file_path in self.recent_files:
            self.RECENT_MENU.add_command(
                label=file_path,
                command=lambda path=file_path: self.open_csv_from_recent(path),
            )

    def open_csv_from_recent(self, file_path):
        try:
            self.df = pd.read_csv(file_path)
            self.current_file_path = file_path
            self.display_csv()
        except Exception as e:
            messagebox.showerror("Error", f"Invalid file {file_path}. Error: {e}")

    def save_recent_files(self):
        with open("src/recent_files.json", "w") as f:
            json.dump(self.recent_files, f)

    def load_recent_files(self):
        if os.path.exists("src/recent_files.json"):
            with open("src/recent_files.json", "r") as f:
                return json.load(f)
        return []

    def display_empty(self):
        if self.table:
            self.table.destroy()
        
        self.canvas = tk.Canvas(self.frame_issues)
        
        self.table = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.table, anchor="nw")
        
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.frame_issues.grid_rowconfigure(0, weight=1)
        self.frame_issues.grid_columnconfigure(0, weight=1)
        
        headers = ["Input Date", "Item Name", "Item Barcode", "Item Type", "Item Note", "Item To-Do", "Customer", "Customer Barcode", "Previous Customer", "Previous Customer Barcode", "Staff Logged", "Item Update", "Status", "Problem Upon Checkout"]
        
        for i in range(len(headers)):
            label = tk.Label(self.table, text=headers[i], borderwidth=0, bd=0, highlightthickness=0, width=14, height=2, font=self.fonts["INTER_BOLD"], bg=self._cell_bg_inactive[0], fg=self._cell_font[0])
            label.grid(row=0, column=i, padx=0, pady=0)
        
        for x in range(9):
            for y in range(20):
                entry = tk.Text(self.table, bd=0, highlightthickness=2, width=14, height=2, font=self.fonts["INTER_REG"], bg=self._cell_bg_inactive[0], fg=self._cell_font[0])
                entry.configure(highlightbackground=self._cell_border[0], highlightcolor=self._cell_border[0])
                
                entry.tag_configure("left", justify=tk.LEFT)
                entry.insert(tk.INSERT, f"test c: {x}, r: {y}")
                entry.tag_add("left", "1.0", "end")
                
                entry.grid(row=x + 1, column=y, padx=0, pady=0)
                
                entry.bind("<FocusIn>", lambda event, e=entry: e.configure(highlightbackground=self._library_darker, highlightcolor=self._library_darker, bg=self._cell_bg_active[0]))
                entry.bind("<FocusOut>", lambda event, e=entry: e.configure(highlightbackground=self._cell_border[0], highlightcolor=self._cell_border[0], bg=self._cell_bg_inactive[0]))
                
                if darkdetect.isDark():
                    entry.configure(bg=self._cell_bg_inactive[1], fg=self._cell_font[1], highlightbackground=self._cell_border[1], highlightcolor=self._cell_border[1])
                    entry.bind("<FocusIn>", lambda event, e=entry: e.configure(highlightbackground=self._library_darker, highlightcolor=self._library_darker, bg=self._cell_bg_active[1]))
                    entry.bind("<FocusOut>", lambda event, e=entry: e.configure(highlightbackground=self._cell_border[1], highlightcolor=self._cell_border[1], bg=self._cell_bg_inactive[1]))
                else:
                    entry.configure(bg=self._cell_bg_inactive[0], fg=self._cell_font[0], highlightbackground=self._cell_border[0], highlightcolor=self._cell_border[0])
                    entry.bind("<FocusOut>", lambda event, e=entry: e.configure(highlightbackground=self._cell_border, highlightcolor=self._cell_border, bg=self._cell_bg_inactive[0]))
                    entry.bind("<FocusIn>", lambda event, e=entry: e.configure(highlightbackground=self._library_darker, highlightcolor=self._library_darker, bg=self._cell_bg_active[0]))
                    entry.bind("<FocusOut>", lambda event, e=entry: e.configure(highlightbackground=self._cell_border[0], highlightcolor=self._cell_border[0], bg=self._cell_bg_inactive[0]))
        
        self.table.update_idletasks()
    
    def display_csv(self):
        if self.table:
            self.table.destroy()

        self.canvas = tk.Canvas(self.frame_issues)
        self.h_scrollbar = tk.Scrollbar(
            self.frame_issues, orient="horizontal", command=self.canvas.xview
        )
        self.v_scrollbar = tk.Scrollbar(
            self.frame_issues, orient="vertical", command=self.canvas.yview
        )

        self.canvas.configure(xscrollcommand=self.h_scrollbar.set)
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set)

        self.table = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.table, anchor="nw")

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.h_scrollbar.grid(row=1, column=0, sticky="ew")
        self.v_scrollbar.grid(row=0, column=1, sticky="ns")

        self.frame_issues.grid_rowconfigure(0, weight=1)
        self.frame_issues.grid_columnconfigure(0, weight=1)

        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind_all("<Shift-MouseWheel>", self.on_shift_mousewheel)
        self.canvas.bind_all("<Control-MouseWheel>", self.on_ctrl_mousewheel)

        for i, col in enumerate(self.df.columns):
            label = tk.Label(self.table, text=col, borderwidth=0, relief="solid")
            label.grid(row=0, column=i, padx=0, pady=0)

        for i, row in self.df.iterrows():
            for j, value in enumerate(row):
                entry = tk.Entry(self.table, borderwidth=1, relief="flat")
                entry.insert(0, value)
                if entry.get() == "NaN":
                    entry.delete(0, tk.END)
                    entry.insert(0, "")
                entry.grid(row=i + 1, column=j, padx=0, pady=0)
                entry.bind(
                    "<FocusOut>", lambda e, row=i, col=j: self.update_value(e, row, col)
                )
                if i % 2 != 0:
                    entry.configure(background="#d4d4d4")

        self.table.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))


if __name__ == "__main__":
    app = AVApp()
