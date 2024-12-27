import json
import os
import pandas as pd
import platform
import pyglet
import tkinter as tk
from converters import Converter
from custom_windows import CustomWindow
from datetime import date
from mit_license import mit_license
from tkinter import filedialog, messagebox, PhotoImage

class App(tk.Tk):
	def __init__(self, width: int = 800, height: int = 600):
		super().__init__()

		# Set up window properties
		self.width, self.height = width, height
		self.name = "AV Issues"
		self.title(self.name)
		self.geometry(f"{self.width}x{self.height}")

		# Set window icon based on the operating system
		if platform.system() == "Windows":
			self.iconbitmap(default="src/icon.ico")
		else:
			self._icon = PhotoImage(file="src/icon.png")
			self.iconphoto(True, self._icon)

		# Load recent files from JSON file
		self.recent_files = self.load_recent_files()

		# Set up the menu bar
		self.setup_menubar()

		self.current_file_path = None  # Path of the currently opened file
		self.table = None  # Table widget to display CSV data
		self.df = None  # DataFrame to hold CSV data

		# Configure grid layout for the main window
		self.grid_rowconfigure(0, weight=1)
		self.grid_columnconfigure(0, weight=1)

		# Set up frame to hold the table
		self.table_frame = tk.Frame()
		self.table_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
		self.table_frame.grid_rowconfigure(0, weight=1)
		self.table_frame.grid_columnconfigure(0, weight=1)

		# Open the most recent file if available
		if self.recent_files:
			self.open_csv_from_recent(self.recent_files[0])
		self.mainloop()

	def setup_menubar(self):
		# Application metadata
		self._app_name = "AV Issues"
		self._author = "Chris Wright"
		self._organization = "Richland Library"
		self._sub_organization = "St. Andrews Branch"
		self._current_year = date.today().year
		self._version = "0.0.1"
		self._license = f"{self.name} v{self._version} is under the MIT license:"
		self._mit_license = mit_license(
			self._current_year, self._author, self._organization, self._sub_organization
		)

		# Create the menu bar
		self.menubar = tk.Menu(self)

		# Create File, Edit, and Help menus
		self._file = tk.Menu(self.menubar, tearoff=0)
		self._edit = tk.Menu(self.menubar, tearoff=0)
		self._help = tk.Menu(self.menubar, tearoff=0)
		self.menubar.add_cascade(label="File", menu=self._file)
		self.menubar.add_cascade(label="Edit", menu=self._edit)
		self.menubar.add_cascade(label="Help", menu=self._help)

		# Add commands to File menu
		self._file.add_command(label="New File", command=None)
		self._file.add_command(label="Open...", command=self.open_csv)
		self._file.add_command(label="Save", command=self.save_csv)
		self._file.add_command(label="Save As...", command=self.save_as_csv)
		self._file.add_separator()
		self._file.add_command(label="Convert...", command=self.convert_csv)

		# Add Recently Opened submenu
		self.recent_menu = tk.Menu(self._file, tearoff=0)
		self._file.add_cascade(label="Recently Opened", menu=self.recent_menu)
		self.update_recent_files_menu()

		self._file.add_separator()
		self._file.add_command(label="Exit", command=self.destroy)

		# Add commands to Edit menu
		self._edit.add_command(label="Cut", command=None)
		self._edit.add_command(label="Copy", command=None)
		self._edit.add_command(label="Paste", command=None)
		self._edit.add_command(label="Select All", command=None)
		self._edit.add_separator()
		self._edit.add_command(label="Find...", command=None)
		self._edit.add_command(label="Find again", command=None)

		# Add commands to Help menu
		self._help.add_command(label="AV Issues Help", command=None)
		self._help.add_command(label="Guide", command=None)
		self._help.add_separator()
		self._help.add_command(label="About AV Issues", command=self._about_av_issues)

		# Configure the menu bar
		self.config(menu=self.menubar)

	def _about_av_issues(self):
		# Display information about the application
		about_av_issues_string = f"{self._author}\n\n"
		about_av_issues_string += f"{self._app_name} version {self._version}\n"
		about_av_issues_string += (
			f"© {self._author}, {self._organization} {self._sub_organization}.\n\n"
		)
		about_av_issues_string += (
			f"This product is licensed under the MIT Permissive License:\n"
		)
		about_av_issues_string += self._mit_license
		# Display custom info window with application details
		cw = CustomWindow()
		cw.custom_showinfo(
			"About AV Issues", "src/icon_128.png", about_av_issues_string
		)

	def open_csv(self):
		# Open a CSV file and display its contents
		file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
		if file_path:
			try:
				self.df = pd.read_csv(file_path)
				self.current_file_path = file_path
				self.update_recent_files(file_path)
				self.display_csv()
			except Exception as e:
				messagebox.showerror("Error", f"Invalid file {file_path}. Error: {e}")

	def display_csv(self):
		# Display the contents of the CSV file in a table
		if self.table:
			self.table.destroy()

		# Create canvas and scrollbars
		self.canvas = tk.Canvas(self.table_frame)
		self.horizontal_scrollbar = tk.Scrollbar(
			self.table_frame, orient="horizontal", command=self.canvas.xview
		)
		self.vertical_scrollbar = tk.Scrollbar(
			self.table_frame, orient="vertical", command=self.canvas.yview
		)
		self.canvas.configure(xscrollcommand=self.horizontal_scrollbar.set)
		self.canvas.configure(yscrollcommand=self.vertical_scrollbar.set)

		# Create table frame inside canvas
		self.table = tk.Frame(self.canvas)
		self.canvas.create_window((0, 0), window=self.table, anchor="nw")

		self.canvas.grid(row=0, column=0, sticky="nsew")
		self.horizontal_scrollbar.grid(row=1, column=0, sticky="ew")
		self.vertical_scrollbar.grid(row=0, column=1, sticky="ns")

		self.table_frame.grid_rowconfigure(0, weight=1)
		self.table_frame.grid_columnconfigure(0, weight=1)

		# Bind scroll events
		self.canvas.bind_all('<MouseWheel>', self._on_mousewheel)
		self.canvas.bind_all('<Shift-MouseWheel>', self._on_shift_mousewheel)
		self.canvas.bind_all('<Control-MouseWheel>', self._on_ctrl_mousewheel)

		# Populate table with data
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

	def _on_mousewheel(self, event):
		self.canvas.yview_scroll(int(-1*(event.delta/120)), 'units')
	
	def _on_shift_mousewheel(self, event):
		self.canvas.xview_scroll(int(-1*(event.delta/120)), 'units')

	def _on_ctrl_mousewheel(self, event):
		self.canvas.xview_scroll(int(-1*(event.delta/120)), 'units')

	def update_value(self, event, row, col):
		# Update the value in the DataFrame when the user edits a cell
		new_value = event.widget.get()
		self.df.iat[row, col] = new_value

	def save_csv(self):
		# Save the current DataFrame to the current file path
		if self.df is not None and self.current_file_path:
			try:
				self.df.to_csv(self.current_file_path, index=False)
				messagebox.showinfo("Success", "CSV file saved")
			except Exception as e:
				messagebox.showerror(
					"Error", f"Could not save file {self.current_file_path}. Error: {e}"
				)

	def save_as_csv(self):
		# Save the current DataFrame to a new file path
		if self.df is not None:
			file_path = filedialog.asksaveasfilename(
				defaultextension=".csv", filetypes=[("CSV files", "*.csv")]
			)
			if file_path:
				try:
					self.df.to_csv(file_path, index=False)
					self.current_file_path = file_path
					messagebox.showinfo("Success", "CSV file saved")
				except Exception as e:
					messagebox.showerror("Error", f"Invalid {file_path}. Error: {e}")

	def convert_csv(self):
		# Convert an Excel file to CSV and display its contents
		file_path = filedialog.askopenfile(filetypes=[("Excel files", "*.xlsx")])
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
		# Update the list of recent files
		if file_path in self.recent_files:
			self.recent_files.remove(file_path)
		self.recent_files.insert(0, file_path)
		if len(self.recent_files) > 5:
			self.recent_files = self.recent_files[:5]
		self.save_recent_files()
		self.update_recent_files_menu()

	def update_recent_files_menu(self):
		# Update the Recently Opened menu with the list of recent files
		self.recent_menu.delete(0, tk.END)
		for file_path in self.recent_files:
			self.recent_menu.add_command(
				label=file_path,
				command=lambda path=file_path: self.open_csv_from_recent(path),
			)

	def open_csv_from_recent(self, file_path):
		# Open a CSV file from the list of recent files
		try:
			self.df = pd.read_csv(file_path)
			self.current_file_path = file_path
			self.display_csv()
		except Exception as e:
			messagebox.showerror("Error", f"Invalid file {file_path}. Error {e}")

	def save_recent_files(self):
		# Save the list of recent files to a JSON file
		with open("src/recent_files.json", "w") as f:
			json.dump(self.recent_files, f)

	def load_recent_files(self):
		# Load the list of recent files from a JSON file
		if os.path.exists("src/recent_files.json"):
			with open("src/recent_files.json", "r") as f:
				return json.load(f)
		return []

if __name__ == "__main__":
	app = App()
