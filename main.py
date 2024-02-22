import customtkinter
from PIL import Image , ImageOps
import os
import rembg
import numpy as np
from tkinter import PhotoImage
from CTkXYFrame import *
from CTkMessagebox import CTkMessagebox

class ImageLabel(customtkinter.CTkLabel):
    def __init__(self, master, text="", image=None, **kwargs):
        super().__init__(master, text="", image=image, **kwargs)
        self.image=image
        self.pilimage= None
        self.current_size = None

    def showImage(self, im, size = None):            
        if not size:
            size = im.size
        self.pilimage = im
        self.current_size = size
        show_image = customtkinter.CTkImage(light_image=im, size=size)
        self = ImageLabel(self.master, text="", image=show_image)
 #       self.label2 = customtkinter.CTkLabel(self, image=show_image,text='')
        self.grid(column=0, row=1, padx=10,pady=10 ,sticky="nsew")
        
    def zoom_in(self):
        xsize, ysize = self.current_size
        self.showImage(im=self.pilimage,size=(xsize*2,ysize*2))

    def zoom_out(self):
        xsize, ysize = self.current_size
        self.showImage(im=self.pilimage,size=(xsize//2,ysize//2))



class ImageFrame(customtkinter.CTkFrame):
    def __init__(self, master, label_text='', **kwargs):
        super().__init__(master, **kwargs)
        
        # add widgets onto the frame, for example:
        self.label = customtkinter.CTkLabel(self,text=label_text)
        self.label.grid(row=0, column=0, padx=20)


        self.image=None
        self.label2 = customtkinter.CTkLabel(self, image=self.image, text='')
        self.label2.grid(column=0, row=1, padx=10,pady=10 ,sticky="nsew")

        self.grid_rowconfigure(1, weight=8)

        # add zoom in
        icon1 = PhotoImage(file="plus.png")
        self.button_zoom_in = customtkinter.CTkButton(self,fg_color="transparent", text="", image=icon1, command=self.zoom_in)
        self.button_zoom_in.grid(row=2, column=0, padx=10, pady=10, sticky="se")

        self.button_zoom_out = customtkinter.CTkButton(self,fg_color="transparent", text="", image=icon1, command=self.zoom_out)
        self.button_zoom_out.grid(row=2, column=1, padx=10, pady=10, sticky="se")

    def showImage(self, im, size = None):       
        self.master.current_image = im
        if not size:
            size = im.size
        show_image = customtkinter.CTkImage(light_image=im, size=size)
        self.label2 = customtkinter.CTkLabel(self, image=show_image,text='')
        self.label2.grid(column=0, row=1, padx=10,pady=10 ,sticky="nsew")
        
    def zoom_in(self):
        xsize, ysize = self.master.current_image.size

        self.showImage(im=self.master.current_image,size=(xsize*2,ysize*2))

    def zoom_out(self):
        xsize, ysize = self.master.current_image.size
        self.master.current_image = self.master.current_image.resize((xsize//2,ysize//2))
        self.showImage(im=self.master.current_image)
        
class NavbarFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.button_open = customtkinter.CTkButton(self, text="Open File", command=self.open_image)
        self.button_open.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.button_rembg = customtkinter.CTkButton(self, text="Remove Background", command=self.remove_bg)
        self.button_rembg.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        

        self.button_save_as = customtkinter.CTkButton(self, text="Save As...", command=self.save_image_as)
        self.button_save_as.grid(row=2, column=0, padx=10, pady=10, sticky="w")

    def open_image(self,*args):
        screen_size = (700,500)
        f_types = [('Jpg Files', '*.jpg'),('PNG Files','*.png')]
        filename= customtkinter.filedialog.askopenfilename(filetypes=f_types)
        if (filename):
            self.master.current_filename=filename          
            im = Image.open(filename)
            self.master.original_image = im
            self.master.current_image=im
            
            im = ImageOps.contain(im,screen_size)
            self.master.image_label.showImage(im=im)
            
            
    def remove_bg(self,*args):
        # Load the input image
        input_image = self.master.original_image
        output_image = None
        if (input_image):
            try:
                # Convert the input image to a numpy array
                input_array = np.array(input_image)
                # Apply background removal using rembg
                output_array = rembg.remove(input_array)
                # Create a PIL Image from the output array
                output_image = Image.fromarray(output_array)

                self.master.current_image = output_image

                self.master.image_label.showImage(im=output_image)
            except Exception as e:
                CTkMessagebox(title="Error", message=f"An error occurred while removing background: {e}", icon="cancel")

                
    def save_image_as(self,*args):
        file = None
        if(self.master.current_image):
            files = [('PNG Files','*.png')]
            file = customtkinter.filedialog.asksaveasfilename(filetypes = files, defaultextension = files) 
        if (file):
            try:
                self.master.current_image.save(file, format='PNG')
            except Exception as e:
                CTkMessagebox(title="Error", message=f"An error occurred while saving the image: {e}", icon="cancel")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x600")
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(0, weight=8)

        self.navbar_frame = NavbarFrame(master=self)
        self.navbar_frame.grid(row=0, column=0, padx=2, pady=2)
        
        #self.image_frame = ImageFrame(master=self, label_text='Image')
        #self.image_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.sframe = CTkXYFrame(self)
        self.sframe.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
      #  impil = Image.open('WMAkv.jpg')
      #  show_image = customtkinter.CTkImage(light_image=impil, size= impil.size)
        
        self.image_label = ImageLabel(self.sframe, text="", image=None)
        self.image_label.grid(row=0, column=0, sticky="nsew",padx=5, pady=5)
        
        icon1 = PhotoImage(file="plus.png")
        self.button_zoom_in = customtkinter.CTkButton(self,fg_color="transparent", text="", image=icon1, command=self.image_label.zoom_in)
        self.button_zoom_in.grid(row=1, column=1, padx=10, pady=10, sticky="se")

        icon1 = PhotoImage(file="minus.png")
        self.button_zoom_out = customtkinter.CTkButton(self,fg_color="transparent", text="", image=icon1, command=self.image_label.zoom_out)
        self.button_zoom_out.grid(row=2, column=1, padx=10, pady=10, sticky="se")
        
        
        self.current_image=None
        self.original_image=None
        self.current_filename=None

app = App()
app.mainloop()