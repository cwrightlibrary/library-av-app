import customtkinter
import os
import pandas as pd
from tkinter import filedialog


# Buttons for the App
class OpenShowCSVFrame(customtkinter.CTkFrame):
    def __init__(self, master, parent):
        # Inherit the master CTkFrame properties
        super().__init__(master)
        self.parent = parent
        
        # CSV preview window
        self.preview_window = None
        self.preview_window_textbox = None
        
        # Use grid system
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        # Load CSV button
        self.button_open_csv = customtkinter.CTkButton(
            self, text='Open CSV', command=self.load_csv
        )
        # Place Load CSV button
        self.button_open_csv.grid(row=0, column=0, padx=10, pady=(10, 0), sticky='ew')

        # Preview CSV button
        self.button_preview_csv = customtkinter.CTkButton(
            self, text='Preview CSV', command=self.preview_csv
        )
        # Place Preview CSV Button
        self.button_preview_csv.grid(
            row=1, column=0, padx=10, pady=(10, 0), sticky='ew'
        )

        # If CSV file valid, disable the load button, enable the preview button
        if hasattr(self.parent, 'csv_path') and self.parent.csv_path != '':
            self.button_open_csv.configure(state='disabled')
            self.button_preview_csv.configure(state='enabled')

    # Load the CSV
    def load_csv(self):
        # Get the location of this script '/src' where the 'updated_av_issues.csv' file is located
        current_dir = os.path.join(os.getcwd(), 'src')
        # Open an OS file dialog window to select a CSV file
        self.parent.csv_path = filedialog.askopenfile(
            title='Select a CSV file',
            filetypes=[('CSV Files', '*.csv')],
            initialdir=current_dir,
        )
        # Disable the open CSV button and enable the preview CSV button
        # TO-DO: Remove this in the future
        self.parent.open_csv()

    # Preview the CSV
    def preview_csv(self):
        if self.parent.csv_df is not None:
            print(f'Success previewing "{self.parent.csv_path}".')
            print(self.parent.csv_df)
            self.preview_csv_window()
        else:
            print(f'Error! Incorrent path "{self.parent.csv_path}". Try loading a CSV or creating a new one.')
    
    # Preview CSV window
    def preview_csv_window(self):
        print('Success opening CSV preview window.')
        # Create the preview window
        self.preview_window = customtkinter.CTkToplevel()
        self.preview_window.title('Preview CSV')
        self.preview_window.geometry('600x400')
        self.preview_window.grid_columnconfigure(0, weight=1)
        self.preview_window.grid_rowconfigure((0, 1), weight=1)
        
        # Make the new window always float on top
        self.preview_window.attributes('-topmost', 1)
        self.preview_window.lift()
        
        # TO-DO: Update this
        self.segmented_button = customtkinter.CTkSegmentedButton(self.preview_window, values=['Row1', 'Row2', 'Row3'])
        self.segmented_button.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        
        # Show the CSV in a textbox
        self.preview_window_textbox = customtkinter.CTkTextbox(self.preview_window, font=customtkinter.CTkFont(family='Consolas'), corner_radius=4)
        self.preview_window_textbox.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
        self.preview_window_textbox.insert('0.0', self.parent.csv_df)


# CSV Reader App
class AVApp(customtkinter.CTk):
    def __init__(self, csv_path: str = ''):
        # Inherit CTk properties
        super().__init__()
        # Set the window's title
        self.title('AV Issues 0.1.0')
        # Set the window's width & height
        self.geometry('400x400')
        # Set the appearance
        self._set_appearance_mode('System')

        # Get the CSV file path
        self.csv_path = csv_path
        # Create empty dataframe and dict
        self.csv_df = None
        self.csv_dict = None

        # Use a grid system
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create a frame for the OpenShowCSVFrame
        self.open_show_csv_frame = OpenShowCSVFrame(self, self)
        self.open_show_csv_frame.grid(
            row=0, column=0, padx=10, pady=(10, 0), sticky='nsew'
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
            self.csv_dict = self.csv_df.to_dict()
            print('Created dictionary from CSV data')
        # If the file path is invalid
        except FileNotFoundError:
            print(f'Error! File path "{self.csv_path}" does not exist.')
            print('Try running create_new_csv() or fix the file path.')


# Set the CSV file path
csv_file_path = 'src/updated_av_issues.csv'

# Create the app
app = AVApp(csv_file_path)
# Run it
app.mainloop()
