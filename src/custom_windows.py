import tkinter as tk

class CustomWindow:
    def __init__(self):
        pass
    
    def custom_showinfo(self, title: str = 'showinfo', icon: str = 'src/icon.png', message: str = 'Information'):
        top = tk.Toplevel()
        top.title(title)
        
        img = tk.PhotoImage(file=icon)
        
        label = tk.Label(top, image=img, text=message, compound='top', wraplength=500, justify=tk.LEFT, anchor='w')
        label.pack(padx=10, pady=10)
        
        button = tk.Button(top, text='OK', command=top.destroy)
        button.pack(pady=5)
        
        label.img = img
        
        label_width = label.winfo_reqwidth()
        label_height = label.winfo_reqheight()
        button_width = button.winfo_reqwidth()
        button_height = button.winfo_reqheight()
        
        total_width = max(label_width, button_width) + 20
        total_height = label_height + button_height + 40

        top.geometry(f'{total_width}x{total_height}')
        
        top.mainloop