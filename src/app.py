import customtkinter
import pandas as pd


customtkinter.set_appearance_mode('System')
customtkinter.set_default_color_theme('blue')


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.width, self.height = 1100, 580
        self.title('AV Issues')
        self.geometry(f'{self.width}x{self.height}')
        
        self.csv_path = None
        self.csv_df = None
        self.csv_dict = None
        
        self.import_csv_data()
        
        self.av_keys = []
        for key, value in enumerate(self.csv_dict[0]):
            self.av_keys.append(value.replace('-', ' ').title())

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky='nsew')
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame,
            text='AV Issues',
            font=customtkinter.CTkFont(size=20, weight='bold'),
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_new_issue = customtkinter.CTkButton(
            self.sidebar_frame, text='New Issue'
        )
        self.sidebar_button_new_issue.grid(row=1, column=0, padx=20, pady=10)

        self.sidebar_button_all_issues = customtkinter.CTkButton(
            self.sidebar_frame, text='View All Issues'
        )
        self.sidebar_button_all_issues.grid(row=2, column=0, padx=20, pady=10)

        self.sidebar_button_load_csv = customtkinter.CTkButton(
            self.sidebar_frame, text='Load CSV'
        )
        self.sidebar_button_load_csv.grid(row=3, column=0, padx=20, pady=10)

        self.appearance_mode_label = customtkinter.CTkLabel(
            self.sidebar_frame, text='Appearance Mode:', anchor='w'
        )
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionmenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame,
            values=['System', 'Light', 'Dark'],
            command=self.change_appearance_mode_event,
        )
        self.appearance_mode_optionmenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        self.scaling_label = customtkinter.CTkLabel(
            self.sidebar_frame, text='UI Scaling', anchor='w'
        )
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionmenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame,
            values=['80%', '90%', '100%', '110%', '120%'],
            command=self.change_scaling_event,
        )
        self.scaling_optionmenu.set('100%')
        self.scaling_optionmenu.grid(row=8, column=0, padx=20, pady=(10, 20))
        
        self.csv_viewer_frame = customtkinter.CTkFrame(self)
        self.csv_viewer_frame.grid(row=0, column=1, padx=20, pady=20, rowspan=4, sticky='nsew')
        
        self.csv_viewer_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14), weight=1)
        self.csv_viewer_frame.grid_rowconfigure((0, 1, 2), weight=1)
        
        for i in range(len(self.av_keys)):
            key_label = customtkinter.CTkLabel(self.csv_viewer_frame, text=self.av_keys[i])
            key_label.grid(row=0, column=i, padx=10, pady=10, sticky='new')

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace('%', '')) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
    
    def import_csv_data(self):
        try:
            self.csv_path = 'src/updated_av_issues.csv'
            print(f'Success! Loaded "{self.csv_path}".')
            self.csv_df = pd.read_csv(self.csv_path)
            self.csv_dict = self.csv_df.to_dict(orient='records')
        except FileExistsError:
            print('Error loading file path. Try creating a new CSV file.')


if __name__ == '__main__':
    app = App()
    app.mainloop()
