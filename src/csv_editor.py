import customtkinter as ctk
from tkinter import PhotoImage

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title('Menu Bar App')
        self.geometry('800x600')
        
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.menubar_frame = ctk.CTkFrame(self, height=30, corner_radius=0)
        self.menubar_frame.grid(row=0, column=0, sticky='new')
        self.menubar_frame.grid_rowconfigure(0, weight=1)
        
        self.menubar_items = [
            ['File', ['New', 'Open', 'Save', 'Save As', 'Exit']],
            ['Edit', ['Undo', 'Redo', 'Cut', 'Copy', 'Paste', 'Delete', 'Select All']],
            ['View', ['Zoom In', 'Zoom Out', 'Full Screen']],
            ['Help', ['About']]
            ]
        self.menubar_buttons = []
        
        for index, item in enumerate(self.menubar_items):
            menubar_button = ctk.CTkOptionMenu(self.menubar_frame, values=item[1], button_color=('#3B8ED0', '#1F6AA5'), button_hover_color=('#3B8ED0', '#1F6AA5'), corner_radius=0, width=60, command=self.menu_click())
            menubar_button.set(item[0])
            menubar_button.grid(row=0, column=index, padx=(0, 5), sticky='nsew')
            self.menubar_buttons.append(menubar_button)
        
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=1, column=0, sticky='nsew')
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        self.test_label = ctk.CTkLabel(self.main_frame, text='Test Label')
        self.test_label.grid(row=0, column=0, padx=20, pady=20)
    
    def menu_click(self):
        print('Menu Clicked')


if __name__ == '__main__':
    app = App()
    app.mainloop()