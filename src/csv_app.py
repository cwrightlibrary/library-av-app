import customtkinter
import os
import pandas as pd
from tkinter import filedialog

# lst = 
# [['date-inputted', []],
#  ['date-resolved', []],
#  ['item-name', []],
#  ['item-barcode', []],
#  ['item-final-update', []],
#  ['item-issue', []],
#  ['item-note', []],
#  ['customer-name', []],
#  ['customer-barcode', []],
#  ['customer-phone', []],
#  ['customer-email', []],
#  ['customer-note', []],
#  ['customer-contacted', []],
#  ['last-customer-name', []],
#  ['last-customer-barcode', []]]


# Preview CSV pop-up window
class PreviewCSV(customtkinter.CTkToplevel):
    def __init__(self, master, parent):
        # Set inheritences
        super().__init__(master)
        self.parent = parent

        self.title("Preview CSV")
        self.geometry("600x400")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        # Make the new window always float on top
        self.attributes("-topmost", 1)
        self.lift()

        # Get the AV issues from the CSV
        self.av_issues_rows = []

        # Create a list for each issue
        # issue = ['title', [csv_info]]
        for d in self.parent.csv_dict:
            title_values = [list(d.values())]
            for k, v in d.items():
                if k == "item-name":
                    title_values.insert(0, v)
            self.av_issues_rows.append(title_values)

        # Create a list of all of the titles
        self.av_issues_titles = [item[0] for item in self.av_issues_rows]
        # Segmented button with the titles for the names of each button segment
        self.av_issues_segmented_button = customtkinter.CTkSegmentedButton(
            self,
            values=self.av_issues_titles,
            command=self.update_av_issues_segmented_button,
        )
        self.av_issues_segmented_button.set(self.av_issues_titles[0])
        self.av_issues_segmented_button.grid(
            row=0, column=0, padx=10, pady=10, sticky="new"
        )

        # Show the CSV in a textbox
        self.textbox = customtkinter.CTkTextbox(
            self, font=customtkinter.CTkFont(family="Consolas"), corner_radius=4
        )
        self.textbox.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.textbox.insert("0.0", "\n".join(map(str, self.av_issues_rows[0][1])))

    def update_av_issues_segmented_button(self, value):
        for c in self.av_issues_rows:
            if c[0] == value:
                print(c)
                textbox_text = "\n".join(map(str, c[1]))
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", textbox_text)


class NewCSV(customtkinter.CTkToplevel):
    def __init__(self, master, parent):
        super().__init__(master)
        self.parent = parent

        self.title("New CSV")
        self.geometry("400x800")

        self.attributes("-topmost", 1)
        self.lift()
        
        self.input_keys = parent.csv_df.columns.tolist()
        print(self.input_keys)
        self.input_keys_rows = tuple(index for index, _ in enumerate(self.input_keys))
        self.input_keys_rows += (self.input_keys_rows[-1] + 1,)
        
        self.input_values = []
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(self.input_keys_rows, weight=1)
        
        self.new_csv_label = customtkinter.CTkLabel(self, text="New AV Issues CSV")
        self.new_csv_label.grid(row=0, column=0, padx=10, pady=10, sticky="new")
        
        for k in range(len(self.input_keys)):
            input_value_entry = customtkinter.CTkEntry(self, placeholder_text=self.input_keys[k])
            input_value_entry.grid(row=k+1, column=0, padx=10, pady=10, sticky="ew")


# Buttons for the App
class OpenShowNewCSVFrame(customtkinter.CTkFrame):
    def __init__(self, master, parent):
        # Inherit the master CTkFrame properties
        super().__init__(master)
        self.parent = parent

        # CSV preview window
        self.preview_window = None
        self.preview_window_textbox = None

        # Use grid system
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Load CSV button
        self.button_open_csv = customtkinter.CTkButton(
            self, text="Open CSV", command=self.load_csv
        )
        # Place Load CSV button
        self.button_open_csv.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

        # New CSV button
        self.button_new_csv = customtkinter.CTkButton(
            self, text="New CSV", command=self.new_csv
        )
        # Place New CSV button
        self.button_new_csv.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # Preview CSV button
        self.button_preview_csv = customtkinter.CTkButton(
            self, text="Preview CSV", command=self.preview_csv
        )
        # Place Preview CSV Button
        self.button_preview_csv.grid(
            row=2, column=0, padx=10, pady=(10, 0), sticky="ew"
        )

        # If CSV file valid, disable the load button, enable the preview button
        if hasattr(self.parent, "csv_path") and self.parent.csv_path != "":
            self.button_open_csv.configure(state="disabled")
            self.button_preview_csv.configure(state="enabled")

    # Load the CSV
    def load_csv(self):
        # Get the location of this script '/src' where the 'updated_av_issues.csv' file is located
        current_dir = os.path.join(os.getcwd(), "src")
        # Open an OS file dialog window to select a CSV file
        self.parent.csv_path = filedialog.askopenfile(
            title="Select a CSV file",
            filetypes=[("CSV Files", "*.csv")],
            initialdir=current_dir,
        )
        # Disable the open CSV button and enable the preview CSV button
        # TODO: Remove this in the future
        self.parent.open_csv()

    # Preview the CSV
    def preview_csv(self):
        if self.parent.csv_df is not None:
            print(f'Success previewing "{self.parent.csv_path}".')
            print(self.parent.csv_df)
            self.preview_csv_window()
        else:
            print(
                f'Error! Incorrent path "{self.parent.csv_path}". Try loading a CSV or creating a new one.'
            )

    # Preview CSV window
    def preview_csv_window(self):
        print("Success opening CSV preview window.")
        self.preview_window = PreviewCSV(self, self.parent)

    def new_csv(self):
        self.new_csv_window = NewCSV(self, self.parent)


# CSV Reader App
class AVApp(customtkinter.CTk):
    def __init__(self, csv_path: str = ""):
        # Inherit CTk properties
        super().__init__()
        # Set the window's title
        self.title("AV Issues 0.1.0")
        # Set the window's width & height
        self.geometry("400x400")
        # Set the appearance
        self._set_appearance_mode("System")

        # Get the CSV file path
        self.csv_path = csv_path
        # Create empty dataframe and dict
        self.csv_df = None
        self.csv_dict = None

        # Use a grid system
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create a frame for the OpenShowCSVFrame
        self.open_show_csv_frame = OpenShowNewCSVFrame(self, self)
        self.open_show_csv_frame.grid(
            row=0, column=0, padx=10, pady=(10, 0), sticky="nsew"
        )

        # Valid CSV file check
        self.open_csv()

    # Open the CSV, create a dict from its contents
    def open_csv(self):
        # Try to open the file
        try:
            # Read the CSV file
            self.csv_df = pd.read_csv(self.csv_path)
            print(f'Success! Loaded "{self.csv_path}".')

            # Create dict
            self.csv_dict = self.csv_df.to_dict(orient="records")
            print("Created dictionary from CSV data")
        # If the file path is invalid
        except FileNotFoundError:
            print(f'Error! File path "{self.csv_path}" does not exist.')
            print("Try running create_new_csv() or fix the file path.")


# Set the CSV file path
csv_file_path = "src/updated_av_issues.csv"

# Create the app
app = AVApp(csv_file_path)
# Run it
app.mainloop()
