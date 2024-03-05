import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import skimage.exposure
from CTkMessagebox import CTkMessagebox
from tkinter import filedialog
from optionsdialog import RemoveOptionsDialog, LassoOptionsDialog
from CTkColorPicker import *
from utils import hex_to_rgba
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


class ImageProcessor():
    def __init__(self, master, **kwargs):
        self.master=master
        self.previous_im = None
        
        
    def undo(self):
        if self.previous_im:
            self.master.impil_processed = self.previous_im
            self.master.showImage(im = self.master.impil_processed, initial=True)
    def reset(self):
        self.master.impil_processed = self.master.impil_initial
        self.master.showImage(im = self.master.impil_processed, initial=True)

    def add_shadow(self, sigma=20, offset=10, opacity=0.5, shadow_shift=(15, 15)):
        """ Create shadow for an image with a transparent background.  """
        self.previous_im = self.master.impil_processed 
            
        img = self.master.impil_processed
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
        self.master.impil_processed = result
        self.master.showImage(im = self.master.impil_processed, initial=True)
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
        
    def get_lasso_options(self):
        dialog = LassoOptionsDialog(self.master)
        dialog.lift()
        dialog.focus_force()
        dialog.grab_set()
        self.master.wait_window(dialog)
        input=dialog.get_input()
        return input
        
    def lasso_remove(self, img, pixel, tolerance=30):
        try:
            input = int(self.get_lasso_options())
            self.master.config(cursor="watch")        
            img = img.convert('RGBA')
            self.previous_im = self.master.impil_processed
            ImageDraw.floodfill(img,pixel, (0,0,0,0), thresh=tolerance)
            self.master.impil_processed = img
            self.master.showImage(im=img,initial=True)
            self.master.config(cursor="arrow")
        
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred while removing area selected with lasso tool: {e}", icon="cancel")   
    def remove_bg(self,*args):
        self.master.config(cursor="watch")        
                    
        input_image = self.master.impil_initial
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
                    input_array = np.array(input_image)
                    # Apply background removal using rembg
                    inputs = self.get_options()
                    only_mask=False if inputs[2]==True else True
                    output_array = remove(input_array,
                                only_mask=only_mask,
                                post_process_mask=inputs[1],
                                alpha_matting=inputs[2])  
                    # Create a PIL Image from the output array
                    output_image = Image.fromarray(output_array)
                    if (only_mask):
                        output_image = self.blur_edges(output_image,radius=int(inputs[0]))
                        output_image = self.apply_mask(input_image,output_image)
                    #output_image = Image.fromarray(output_array)
                    if(output_image):    
                        self.master.impil_processed = output_image
                        self.master.showImage(im=output_image,initial=True)
                    
                except Exception as e:
                    CTkMessagebox(title="Error", message=f"An error occurred while removing background: {e}", icon="cancel")
            else:
                CTkMessagebox(title="Info", message="Please load an image to remove background.")
        else:
            CTkMessagebox(title="Error", message=f"Remove background module is not loaded properly.", icon="cancel")
        self.master.config(cursor="arrow")
        
    def blur_edges(self, img, radius=3):
        try:
            # Apply Gaussian blur
            blurred_img = img.filter(ImageFilter.GaussianBlur(radius=radius))

            # Stretch intensity range
            blurred_np = np.array(blurred_img)
            stretched_np = np.clip(2.0 * blurred_np - 127.5, 0, 255).astype(np.uint8)
            stretched_img = Image.fromarray(stretched_np)        
            return stretched_img
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred while removing background: {e}", icon="cancel")
        
    def apply_mask(self, original_image, mask):
        # Convert the original image to RGBA if it's not already in RGBA format
        if original_image.mode != "RGBA":
            original_image = original_image.convert("RGBA")

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
        if (self.master.impil_processed):
            f_types = [('Jpg Files', '*.jpg'),('PNG Files','*.png')]
            filename= filedialog.askopenfilename(filetypes=f_types)
            if (filename):
                try:
                    im = Image.open(filename)
                    im = im.resize(self.master.impil_processed.size)
                    im.paste(self.master.impil_processed,(0,0),self.master.impil_processed)
                    self.previous_im = self.master.impil_processed
                    self.master.showImage(im, initial=True)
                except Exception as e:
                    CTkMessagebox(title="Error", message=f"An error occurred while adding background image: {e}", icon="cancel")
        else:
            CTkMessagebox(title="Info", message="Please load an image and remove background to add background image.")

    

    def add_bgcolor(self):
        if (self.master.impil_processed):
            self.previous_im = self.master.impil_processed
            try:
                pick_color = AskColor() # open the color picker
                color = pick_color.get() # get the color string
                if (color):
                    bg = Image.new('RGBA', self.master.impil_processed.size, hex_to_rgba(color))
                    bg.paste(self.master.impil_processed,(0,0),self.master.impil_processed)
                    self.master.showImage(bg, initial=True)
            except Exception as e:
                CTkMessagebox(title="Error", message=f"An error occurred while adding background color: {e}", icon="cancel")
        else:
            CTkMessagebox(title="Info", message="Please open an image and remove background to change the background color.")


    def rotate(self):
        if (self.master.impil_processed):
            try:
                self.master.impil_processed = self.master.impil_processed.rotate(90, expand=True)
                self.master.showImage(self.master.impil_processed, initial=False)
            except Exception as e:
                CTkMessagebox(title="Error", message=f"An error occurred while rotating: {e}", icon="cancel")
        else:
            CTkMessagebox(title="Info", message="Please load an image first.")
