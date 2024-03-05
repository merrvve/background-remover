import customtkinter
from menubar import MenubarFrame
from navbar import NavbarFrame
from zoomframe import ZoomFrame
from removeoptions import RemoveOptionsDialog
from utils import *
from tkinter import PhotoImage, Canvas, Menu, filedialog
from CTkXYFrame import *
from CTkMessagebox import CTkMessagebox
from CTkColorPicker import *
from threading import Thread
import pathlib
import sys
import os      
import skimage.exposure


import numpy as np
from PIL import Image , ImageOps, ImageTk, ImageDraw, ImageFilter

customtkinter.set_appearance_mode("light")  
customtkinter.set_default_color_theme("dark-blue")

imported = False
remove = None



    
def import_custom_modules():
    global imported
    global remove
    try:
        from rembg import remove
        imported = True
    except ImportError:
        imported = False
        CTkMessagebox(title="Error", message="An error occured while loading remove background module.")




class ImageCanvas(Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.impil_initial = None
        self.impil_processed = None
        self.current_size = None
        self.rect = None

        self.start_x = None
        self.start_y = None
        self.x = self.y = 0
      
    def selectPoint(self):
        self.bind("<ButtonPress-1>", self.on_button_press_point)
        self.bind("<ButtonRelease-1>", self.on_button_release_point)
    def on_button_press_point(self, event):
        # save mouse drag start position
        self.start_x = event.x
        self.start_y = event.y
        w, h=int(self.cget('width')),int(self.cget('height'))
        w_im, h_im = self.impil_processed.size
        ratio = w/w_im
        
        
        
    def on_button_release_point(self, event):
        self.unbind("<ButtonPress-1>")
        self.unbind("<ButtonRelease-1>")  
        
    def selectArea(self):
        self.bind("<ButtonPress-1>", self.on_button_press)
        self.bind("<B1-Motion>", self.on_move_press)
        self.bind("<ButtonRelease-1>", self.on_button_release)
    def unselectArea(self):
        self.unbind("<ButtonPress-1>")
        self.unbind("<B1-Motion>")
        self.unbind("<ButtonRelease-1>")        
    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = event.x
        self.start_y = event.y
        # create rectangle if not yet exist
        #if not self.rect:
        self.rect = self.create_rectangle(self.x, self.y, 1, 1, fill="", dash=(3,5))

    def on_move_press(self, event):
        curX, curY = (event.x, event.y)

        # expand rectangle as you drag the mouse
        self.coords(self.rect, self.start_x, self.start_y, curX, curY)
    def on_button_release(self, event):
        self.delete(self.rect)
        self.rect=None
        self.unselectArea()
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
        
        
     


        

class ImageProcessor():
    def __init__(self, master, **kwargs):
        self.master=master
        self.previous_im = None
        
    def undo(self):
        if self.previous_im:
            self.master.image_canvas.impil_processed = self.previous_im
            self.master.image_canvas.showImage(im = self.master.image_canvas.impil_processed, initial=True)
    def reset(self):
        self.master.image_canvas.impil_processed = self.master.image_canvas.impil_initial
        self.master.image_canvas.showImage(im = self.master.image_canvas.impil_processed, initial=True)

    def add_shadow(self, sigma=20, offset=10, opacity=0.5, shadow_shift=(15, 15)):
        """ Create shadow for an image with a transparent background.  """
        self.previous_im = self.master.image_canvas.impil_processed 
            
        img = self.master.image_canvas.impil_processed
        img = img.convert('RGBA')
        # Create a blurred shadow mask
        shadow = Image.new('RGBA', (img.width + offset * 2, img.height + offset * 2), color="#FFFFFF")
        draw = ImageDraw.Draw(shadow)
        draw.bitmap((offset + shadow_shift[0], offset + shadow_shift[1]), img, fill=(0, 0, 0, int(255 * opacity)))
        shadow_blurred = shadow.filter(ImageFilter.GaussianBlur(sigma))
        
        # Composite the shadow with the image
        result = Image.new('RGBA', (img.width + offset * 2, img.height + offset * 2))
        result.paste(shadow_blurred, (0, 0), mask=shadow_blurred)
        result.paste(img, (offset, offset), mask=img)
        self.master.image_canvas.impil_processed = result
        self.master.image_canvas.showImage(im = self.master.image_canvas.impil_processed, initial=True)
        return result

    def get_options(self):
        #dialog = customtkinter.CTkInputDialog(text="Edge blur radius", title="Blur radius")
        #input = dialog.get_input()
        dialog = RemoveOptionsDialog(self.master)
        dialog.lift()
        dialog.focus_force()
        dialog.grab_set()
        self.master.wait_window(dialog)
        inputs=dialog.get_inputs()
        return inputs
        
    def remove_bg(self,*args):
        input_image = self.master.image_canvas.impil_initial
        output_image = None
        input_array = None
        output_array = None
        global remove 
        global imported
        if imported:
            if (input_image):
                self.previous_im = input_image
                try:
                    # Convert the input image to a numpy array
                    #input_array = array(input_image)
                    # Apply background removal using rembg
                    inputs = self.get_options()
                    only_mask=False if inputs[2]==True else True
                    output_image = remove(input_image,
                                only_mask=only_mask,
                                post_process_mask=inputs[1],
                                alpha_matting=inputs[2])  
                    # Create a PIL Image from the output array
                    if (only_mask):
                        output_image = self.blur_edges(output_image,radius=int(inputs[0]))
                        output_image = self.apply_mask(input_image,output_image)
                    #output_image = Image.fromarray(output_array)
                    if(output_image):    
                        self.master.image_canvas.impil_processed = output_image

                        self.master.image_canvas.showImage(im=output_image,initial=True)
                except Exception as e:
                    CTkMessagebox(title="Error", message=f"An error occurred while removing background: {e}", icon="cancel")
            else:
                CTkMessagebox(title="Info", message="Please load an image to remove background.")
        else:
            CTkMessagebox(title="Error", message=f"Remove background module is not loaded properly.", icon="cancel")
    def blur_edges(self, img, radius=3):
        # Open image
        
        # Apply Gaussian blur
        blurred_img = img.filter(ImageFilter.GaussianBlur(radius=radius))

        # Stretch intensity range
        blurred_np = np.array(blurred_img)
        stretched_np = np.clip(2.0 * blurred_np - 127.5, 0, 255).astype(np.uint8)
        stretched_img = Image.fromarray(stretched_np)        
        return stretched_img
        
        
    def apply_mask(self, original_image, mask):
        
        # Convert the original image to RGBA if it's not already in RGBA format
        if original_image.mode != "RGBA":
            original_image = original_image.convert("RGBA")

        # Convert the mask to grayscale if it's not already in grayscale
        #if mask.mode != "L":
         #   mask = mask.convert("L")
        # Normalize mask values to range [0, 255]
        normalized_mask = mask.point(lambda p: p if p > 127 else 0)

            # Create a new alpha channel with modified transparency values
        alpha = Image.new("L", original_image.size)
        alpha.putdata(normalized_mask.getdata())

        # Apply the new alpha channel to the original image
        result = original_image.copy()
        result.putalpha(alpha)
        # Apply the mask to the alpha channel
        #alpha = original_image.split()[3]  # Get the alpha channel
        #alpha = alpha.point(lambda p: p * normalized_mask.getpixel((0, 0)) / 255)

        # Create a new RGBA image with the modified alpha channel
#        result = Image.new("RGBA", original_image.size)
#        result.paste(original_image, (0, 0), mask=normalized_mask)

        # Save the resulting image

        return result

    def add_bgimg(self):
        if (self.master.image_canvas.impil_processed):
            f_types = [('Jpg Files', '*.jpg'),('PNG Files','*.png')]
            filename= filedialog.askopenfilename(filetypes=f_types)
            if (filename):
                try:
                    im = Image.open(filename)
                    im = im.resize(self.master.image_canvas.impil_processed.size)
                    im.paste(self.master.image_canvas.impil_processed,(0,0),self.master.image_canvas.impil_processed)
                    self.previous_im = self.master.image_canvas.impil_processed
                    self.master.image_canvas.showImage(im, initial=True)
                except Exception as e:
                    CTkMessagebox(title="Error", message=f"An error occurred while adding background image: {e}", icon="cancel")
        else:
            CTkMessagebox(title="Info", message="Please load an image and remove background to add background image.")

    

    def add_bgcolor(self):
        if (self.master.image_canvas.impil_processed):
            self.previous_im = self.master.image_canvas.impil_processed
            try:
                pick_color = AskColor() # open the color picker
                color = pick_color.get() # get the color string
                if (color):
                    bg = Image.new('RGBA', self.master.image_canvas.impil_processed.size, hex_to_rgba(color))
                    bg.paste(self.master.image_canvas.impil_processed,(0,0),self.master.image_canvas.impil_processed)
                    self.master.image_canvas.showImage(bg, initial=True)
            except Exception as e:
                CTkMessagebox(title="Error", message=f"An error occurred while adding background color: {e}", icon="cancel")
        else:
            CTkMessagebox(title="Info", message="Please open an image and remove background to change the background color.")


    def rotate(self):
        if (self.master.image_canvas.impil_processed):
            try:
                self.master.image_canvas.impil_processed = self.master.image_canvas.impil_processed.rotate(90, expand=True)
                self.master.image_canvas.showImage(self.master.image_canvas.impil_processed, initial=False)
            except Exception as e:
                CTkMessagebox(title="Error", message=f"An error occurred while rotating: {e}", icon="cancel")
        else:
            CTkMessagebox(title="Info", message="Please load an image first.")
         

        
class LoadingWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("300x100")
        self.title('Process')
        self.label = customtkinter.CTkLabel(self, text="Loading modules...")
        self.label.pack(padx=20, pady=20)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.is_dark=False
        self.loaded= False
        self.geometry("800x500")
        self.toplevel_window = None
        Thread(target=self.import_modules).start()
        self.title("Background Remover")
        
        self.log = ""
        self.image_processor= ImageProcessor(master=self)

        self.sframe = CTkXYFrame(self)
        self.sframe.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.image_canvas = ImageCanvas(self.sframe, width=700, height=400)
        self.image_canvas.grid(row=0, column=0, sticky="nsew",padx=5, pady=5)
        
        self.zoom_frame = ZoomFrame(master=self)
        self.zoom_frame.grid(row=1, column=1, padx=2, pady=2 , sticky="se")

        self.navbar_frame = NavbarFrame(master=self)
        self.navbar_frame.grid(row=0, column=0, padx=2, pady=2)

        self.menubar = MenubarFrame(master=self)
        self.config(menu=self.menubar)
        
        self.logger = customtkinter.CTkLabel(master=self, text=self.log)
        self.logger.grid(row=2, column=0, columnspan=2, padx=2, pady=2, sticky="ws")
        
        
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(0, weight=8)
        
        
        
    def change_mod(self):
        if self.is_dark:
            customtkinter.set_appearance_mode("light")  
            self.is_dark=False
        else:
            customtkinter.set_appearance_mode("dark")  
            self.is_dark=True
            
    def import_modules(self):
        toplevel_window = LoadingWindow(self)
        toplevel_window.focus()
        self.iconify()
        import_custom_modules()
        toplevel_window.destroy()
        self.deiconify()

    
def main():
    app = App()
    app.mainloop()
    

if __name__ == "__main__":
    main()

        


