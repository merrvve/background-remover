import customtkinter
from PIL import Image , ImageOps, ImageTk
import os
import rembg
import numpy as np
from tkinter import PhotoImage, Canvas, Menu
from CTkXYFrame import *
from CTkMessagebox import CTkMessagebox
from CTkColorPicker import *
customtkinter.set_appearance_mode("light")  
customtkinter.set_default_color_theme("dark-blue")


class ImageCanvas(Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.impil_initial = None
        self.impil_processed = None
        self.current_size = None
    def showImage(self, im, initial=False):
        if im:
            
            w,h = im.size
            self.current_size=im.size
            self.delete("all")
            image = ImageTk.PhotoImage(im)            
            self.config(width=w, height=h)
            self.create_image(0, 0, anchor="nw", image=image)
            self.impil_processed = im
            self.image=image
            if initial:
                if h>800:
                    x =h/800
                    self.resize((int(w/x),int(h/x)))
        
            
    def resize(self,size):
        self.current_size=size
        self.delete("all")
        w,h = size
        im = self.impil_processed.resize(size)
        image = ImageTk.PhotoImage(im)            
        self.config(width=w, height=h)
        self.create_image(0, 0, anchor="nw", image=image)
        self.image=image
            
    def zoom_in(self):
        if self.impil_processed:
            w,h = self.current_size
            self.resize(size=(w*2,h*2))
            

    def zoom_out(self):
        if self.impil_processed:
            w,h = self.current_size
            self.resize(size=(w//2,h//2))
        
class ZoomFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        icon1 = customtkinter.CTkImage(light_image=Image.open("zoom-in.png"))
        self.button_zoom_in = customtkinter.CTkButton(self, width=50,fg_color="transparent", text="", image=icon1, command=self.master.image_canvas.zoom_in)
        self.button_zoom_in.grid(row=0, column=0, padx=2, pady=2, sticky="se")

        icon1 = customtkinter.CTkImage(light_image=Image.open("zoom-out.png"))
        self.button_zoom_out = customtkinter.CTkButton(self, width=50,fg_color="transparent", text="", image=icon1, command=self.master.image_canvas.zoom_out)
        self.button_zoom_out.grid(row=0, column=1, padx=2, pady=2, sticky="se")
 
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
            label='Remove Background',
            command=self.master.image_processor.remove_bg,
            font=("Arial", 14)
        )        
        self.edit_menu.add_command(
            label='Add Background Image',
            command=self.master.image_processor.add_bgimg,
            font=("Arial", 14)
        )        

        self.edit_menu.add_command(
            label='Add Background Color',
            command=self.master.image_processor.add_bgcolor,
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


        
class NavbarFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.button_open = customtkinter.CTkButton(self, text="Open File", command=self.open_image)
        self.button_open.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.button_rembg = customtkinter.CTkButton(self, text="Remove Background", command=self.master.image_processor.remove_bg)
        self.button_rembg.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        

        self.button_save_as = customtkinter.CTkButton(self, text="Save As...", command=self.save_image_as)
        self.button_save_as.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.button_add_bgimg = customtkinter.CTkButton(self, text="Add Background Img", command=self.master.image_processor.add_bgimg)
        self.button_add_bgimg.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        self.button_add_bgcolor = customtkinter.CTkButton(self, text="Add Background Color", command=self.master.image_processor.add_bgcolor)
        self.button_add_bgcolor.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        self.button_rotate = customtkinter.CTkButton(self, text="Rotate", command=self.master.image_processor.rotate)
        self.button_rotate.grid(row=5, column=0, padx=10, pady=10, sticky="w")

    def open_image(self,*args):
        f_types = [('Jpg Files', '*.jpg'),('PNG Files','*.png')]
        filename= customtkinter.filedialog.askopenfilename(filetypes=f_types)
        if (filename):
            im = Image.open(filename)
            self.master.image_canvas.impil_initial = im

            self.master.image_canvas.showImage(im=im, initial=True)
                        
                
    def save_image_as(self,*args):
        file = None
        if(self.master.image_canvas.impil_processed):
            files = [('PNG Files','*.png')]
            file = customtkinter.filedialog.asksaveasfilename(filetypes = files, defaultextension = files) 
            if (file):
                try:
                    self.master.image_canvas.impil_processed.save(file, format='PNG')
                except Exception as e:
                    CTkMessagebox(title="Error", message=f"An error occurred while saving the image: {e}", icon="cancel")
        else:
            CTkMessagebox(title="Info", message="No images found to save.")

class ImageProcessor():
    def __init__(self, master, **kwargs):
        self.master=master
    
    def remove_bg(self,*args):
        # Load the input image
        input_image = self.master.image_canvas.impil_initial
        output_image = None
        if (input_image):
            try:
                # Convert the input image to a numpy array
                input_array = np.array(input_image)
                # Apply background removal using rembg
                output_array = rembg.remove(input_array)
                # Create a PIL Image from the output array
                output_image = Image.fromarray(output_array)

                self.master.image_canvas.impil_processed = output_image

                self.master.image_canvas.showImage(im=output_image,initial=True)
            except Exception as e:
                CTkMessagebox(title="Error", message=f"An error occurred while removing background: {e}", icon="cancel")
        else:
            CTkMessagebox(title="Info", message="Please load an image to remove background.")
    def add_bgimg(self):
        if (self.master.image_canvas.impil_processed):
            f_types = [('Jpg Files', '*.jpg'),('PNG Files','*.png')]
            filename= customtkinter.filedialog.askopenfilename(filetypes=f_types)
            if (filename):
                try:
                    im = Image.open(filename)
                    im = im.resize(self.master.image_canvas.impil_processed.size)
                    im.paste(self.master.image_canvas.impil_processed,(0,0),self.master.image_canvas.impil_processed)
                    self.master.image_canvas.showImage(im, initial=True)
                except Exception as e:
                    CTkMessagebox(title="Error", message=f"An error occurred while adding background image: {e}", icon="cancel")
        else:
            CTkMessagebox(title="Info", message="Please load an image and remove background to add background image.")


    def add_bgcolor(self):
        if (self.master.image_canvas.impil_processed):
            try:
                pick_color = AskColor() # open the color picker
                color = pick_color.get() # get the color string
                bg = Image.new('RGBA', self.master.image_canvas.impil_processed.size, (255, 0, 0, 100))
                bg.paste(self.master.image_canvas.impil_processed,(0,0),self.master.image_canvas.impil_processed)
                self.master.image_canvas.showImage(bg, initial=True)
            except Exception as e:
                CTkMessagebox(title="Error", message=f"An error occurred while adding background color: {e}", icon="cancel")
        else:
            CTkMessagebox(title="Info", message="Please open an image and remove background to change the background color.")


    def rotate(self):
        if (self.master.image_canvas.impil_processed):
            try:
                pass
            except Exception as e:
                CTkMessagebox(title="Error", message=f"An error occurred while rotating: {e}", icon="cancel")
        else:
            CTkMessagebox(title="Info", message="Please load an image first.")



class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x500")
        self.is_dark=False
        
        self.title("Background Remover")
        self.iconbitmap('favicon.ico')
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(0, weight=8)

        self.image_processor= ImageProcessor(master=self)

        self.navbar_frame = NavbarFrame(master=self)
        self.navbar_frame.grid(row=0, column=0, padx=2, pady=2)

        self.menubar = MenubarFrame(master=self)
        self.config(menu=self.menubar)
        
        
        self.sframe = CTkXYFrame(self)
        self.sframe.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.image_canvas = ImageCanvas(self.sframe, width=700, height=400)
        self.image_canvas.grid(row=0, column=0, sticky="nsew",padx=5, pady=5)
        
        self.zoom_frame = ZoomFrame(master=self)
        self.zoom_frame.grid(row=1, column=1, padx=2, pady=2 , sticky="se")
    def change_mod(self):
        if self.is_dark:
            customtkinter.set_appearance_mode("light")  
            self.is_dark=False
        else:
            customtkinter.set_appearance_mode("dark")  
            self.is_dark=True

app = App()
app.mainloop()