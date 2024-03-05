from tkinter import Menu

class MenubarFrame(Menu):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.file_menu = Menu(self, tearoff=0)
        self.file_menu.add_command(
            label='Open',
            command=self.master.navbar_frame.open_image,
            font=("Arial", 14)
        )        
        self.file_menu.add_command(
            label='Save As',
            command=self.master.navbar_frame.save_image_as,
            font=("Arial", 14)
        )        

        self.file_menu.add_command(
            label='Exit',
            command=self.master.destroy,
            font=("Arial", 14)
        )        
        self.add_cascade(label="File", menu=self.file_menu)
        
        self.edit_menu = Menu(self, tearoff=0)
        self.edit_menu.add_command(
            label='Undo',
            command=self.master.image_canvas.image_processor.undo,
            font=("Arial", 14)
        )
        self.edit_menu.add_command(
            label='Reset',
            command=self.master.image_canvas.image_processor.reset,
            font=("Arial", 14)
        )
        self.edit_menu.add_command(
            label='Select',
            command=self.master.image_canvas.selectArea,
            font=("Arial", 14)
        )   
        self.edit_menu.add_command(
            label='Remove Background',
            command=self.master.image_canvas.image_processor.remove_bg,
            font=("Arial", 14)
        )        
        self.edit_menu.add_command(
            label='Add Background Image',
            command=self.master.image_canvas.image_processor.add_bgimg,
            font=("Arial", 14)
        )        

        self.edit_menu.add_command(
            label='Add Background Color',
            command=self.master.image_canvas.image_processor.add_bgcolor,
            font=("Arial", 14)
        )        
        self.add_cascade(label="Edit", menu=self.edit_menu)

        self.options_menu = Menu(self, tearoff=0)
        self.options_menu.add_command(
            label='Light/Dark Mode',
            command=self.master.change_mod,
            font=("Arial", 14)
        )        
        
        self.add_cascade(label="Options", menu=self.options_menu)
