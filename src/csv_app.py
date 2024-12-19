import customtkinter
import pandas as pd
from tkinter import filedialog

# Buttons for the App
class OpenShowCSVFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        # Inherit the master CTkFrame properties
        super().__init__(master)
        
        # Load CSV button
        self.button_open_csv = customtkinter.CTkButton(master, text="Open CSV", command=self.load_csv)
    
    # Load the CSV
    def load_csv(self, master):
        master.csv_path = filedialog.askopenfile(title="Select a CSV file", filetypes=("CSV Files", "*.csv"))

# CSV Reader App
class AVApp(customtkinter.CTk):
    def __init__(self, csv_path):
        # Inherit CTk properties
        super().__init__()
        # Set the window's title
        self.title("AV Issues 0.1.0")
        # Set the window's width & height
        self.geometry("400x400")
        # Set the appearance
        self.set_appearance_mode("System")
        self.set_default_color_theme("dark-blue")

        # Get the CSV file path
        self.csv_path = csv_path
        # Create empty dataframe and dict
        self.csv_df = None
        self.csv_dict = None

    # Open the CSV, create a dict from its contents
    def open_csv(self):
        # Try to open the file
        try:
            # Read the CSV file
            self.csv_df = pd.read_csv(self.csv_path)
            print(f'Success! Loaded "{self.csv_path}".')

            # Create dict
            self.csv_dict = self.csv_df.to_dict()
            print("Created dictionary from CSV data")
        # If the file path is invalid
        except FileNotFoundError:
            print(f'Error! File path "{self.csv_path}" does not exist.')
            print("Try running create_new_csv() or fix the file path.")
            # TO-DO: Change this to be optional


# Create the app
app = AVApp()
# Run it
app.mainloop()
