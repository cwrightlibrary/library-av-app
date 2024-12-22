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
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky='nsew')
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text='AV App', font=customtkinter.CTkFont(size=20, weight='bold'))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.sidebar_button_new_issue = customtkinter.CTkButton(self.sidebar_frame, text='New Issue')
        self.sidebar_button_new_issue.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_all_issues = customtkinter.CTkButton(self.sidebar_frame, text='All Issues')
        self.sidebar_button_all_issues.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_load_csv = customtkinter.CTkButton(self.sidebar_frame, text='Load CSV')
        self.sidebar_button_load_csv.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text='Appearance Mode:', anchor='w')
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionmenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=['System', 'Light', 'Dark'], command=self.change_appearance_mode_event)
        self.appearance_mode_optionmenu.grid(row=6, column=0, padx=20, pady=(10, 10))
    
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == '__main__':
    app = App()
    app.mainloop()