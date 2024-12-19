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
        # Load CSV button
        self.button_open_csv = customtkinter.CTkButton(
            master, text='Open CSV', command=self.load_csv
        )
        # Place Load CSV button
        self.button_open_csv.grid(row=0, column=0, padx=10, pady=(10, 0), sticky='w')
        # If CSV file valid, disable the button
        if hasattr(self.parent, 'csv_path') and self.parent.csv_path != '':
            self.button_open_csv.configure(state='disabled')
        
        
        # Read CSV file
        # self.button_open_csv.

    # Load the CSV
    def load_csv(self):
        # Get the location of this script '/src' where the 'updated_av_issues.csv' file is located
        current_dir = os.path.join(os.getcwd(), 'src')
        self.parent.csv_path = filedialog.askopenfile(
            title='Select a CSV file', filetypes=[('CSV Files', '*.csv')],
            initialdir=current_dir
        )
        self.button_open_csv.configure(state='disabled')
        print(f'Success! Loaded "{self.parent.csv_path}".')


# CSV Reader App
class AVApp(customtkinter.CTk):
    def __init__(self, csv_path: str=''):
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
            row=0, column=0, padx=10, pady=(10, 0), sticky='nsw'
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
# app = AVApp(csv_file_path)
app = AVApp()
# Run it
app.mainloop()
