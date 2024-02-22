import customtkinter
from PIL import Image , ImageOps, ImageTk
import os
import rembg
import numpy as np
from tkinter import PhotoImage, Canvas
from CTkXYFrame import *
from CTkMessagebox import CTkMessagebox

class ImageCanvas(Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.impil_initial = None
        self.impil_processed = None
        self.current_size = None
    def showImage(self, im ,size= None):
        if im:
            if not size:
                size = im.size
            w,h = size
            self.current_size=size
            self.delete("all")
            im = im.resize(size)
            image = ImageTk.PhotoImage(im)
            
            self.config(width=w, height=h)
            self.create_image(0, 0, anchor="nw", image=image)
            if not self.impil_initial:
                self.impil_initial = im
            self.impil_processed = im
            self.image=image
            
    def zoom_in(self):
        w,h =self.current_size
        self.showImage(im=self.impil_initial,size=(w*2,h*2))
        self.current_size=(w*2,h*2)
        

    def zoom_out(self):
        w,h =self.current_size
        self.showImage(im=self.impil_initial,size=(w//2,h//2))
        self.current_size=(w//2,h//2)
        

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
#        screen_size = (700,500)
        f_types = [('Jpg Files', '*.jpg'),('PNG Files','*.png')]
        filename= customtkinter.filedialog.askopenfilename(filetypes=f_types)
        if (filename):
            self.master.current_filename=filename          
            im = Image.open(filename)
            self.master.original_image = im
            self.master.current_image=im
            
#            im = ImageOps.contain(im,screen_size)
            self.master.image_canvas.showImage(im=im)
            
            
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

                self.master.image_canvas.showImage(im=output_image)
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
        self.geometry("800x500")
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
#        photo = ImageTk.PhotoImage(Image.open('o.png'))
        self.image_canvas = ImageCanvas(self.sframe, width=700, height=400)
#        self.image_canvas.create_image(0, 0, anchor="nw", image=photo)
#        self.image_canvas.image= photo
        self.image_canvas.grid(row=0, column=0, sticky="nsew",padx=5, pady=5)
        
        #self.image_label = ImageLabel(self.sframe, text="", image=None)
        #self.image_label.grid(row=0, column=0, sticky="nsew",padx=5, pady=5)
        
        icon1 = PhotoImage(file="plus.png")
        self.button_zoom_in = customtkinter.CTkButton(self,fg_color="transparent", text="", image=icon1, command=self.image_canvas.zoom_in)
        self.button_zoom_in.grid(row=1, column=1, padx=10, pady=10, sticky="se")

        icon1 = PhotoImage(file="minus.png")
        self.button_zoom_out = customtkinter.CTkButton(self,fg_color="transparent", text="", image=icon1, command=self.image_canvas.zoom_out)
        self.button_zoom_out.grid(row=2, column=1, padx=10, pady=10, sticky="se")
        
        
        self.current_image=None
        self.original_image=None
        self.current_filename=None

app = App()
app.mainloop()