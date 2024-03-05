import customtkinter
from utils import resource_path
from PIL import Image
class ZoomFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        iconpath = resource_path('assets','zoom-in.png')
        icon1 = customtkinter.CTkImage(light_image=Image.open(iconpath))
        self.button_zoom_in = customtkinter.CTkButton(self, width=50,fg_color="transparent", text="", image =icon1, command=self.master.image_canvas.zoom_in)
        self.button_zoom_in.grid(row=0, column=1, padx=2, pady=2, sticky="se")

        iconpath = resource_path('assets','zoom-out.png')
        icon1 = customtkinter.CTkImage(light_image=Image.open(iconpath))
        
        self.button_zoom_out = customtkinter.CTkButton(self, width=50, fg_color="transparent", text="", image =icon1, command=self.master.image_canvas.zoom_out)
        self.button_zoom_out.grid(row=0, column=2, padx=2, pady=2, sticky="se")
