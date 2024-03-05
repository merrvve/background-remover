import customtkinter
from tkinter import filedialog
from PIL import Image
from pathlib import Path
from CTkMessagebox import CTkMessagebox

class NavbarFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.button_open = customtkinter.CTkButton(self, text="Open File", command=self.open_image)
        self.button_open.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.button_rembg = customtkinter.CTkButton(self, text="Remove Background", command=self.master.image_canvas.image_processor.remove_bg)
        self.button_rembg.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        

        self.button_save_as = customtkinter.CTkButton(self, text="Save As...", command=self.save_image_as)
        self.button_save_as.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.button_add_bgimg = customtkinter.CTkButton(self, text="Add Background Img", command=self.master.image_canvas.image_processor.add_bgimg)
        self.button_add_bgimg.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        self.button_add_bgcolor = customtkinter.CTkButton(self, text="Add Background Color", command=self.master.image_canvas.image_processor.add_bgcolor)
        self.button_add_bgcolor.grid(row=4, column=0, padx=10, pady=10, sticky="w")

#        self.button_add_shadow = customtkinter.CTkButton(self, text="Add Shadow", command=self.master.image_canvas.image_processor.add_shadow)
#        self.button_add_shadow.grid(row=5, column=0, padx=10, pady=10, sticky="w")

        self.button_rotate = customtkinter.CTkButton(self, text="Rotate", command=self.master.image_canvas.image_processor.rotate)
        self.button_rotate.grid(row=5, column=0, padx=10, pady=10, sticky="w")

        self.button_select = customtkinter.CTkButton(self, text="Select", command=self.master.image_canvas.selectPoint)
        self.button_select.grid(row=6, column=0, padx=10, pady=10, sticky="w")

        self.button_undo = customtkinter.CTkButton(self, text="Undo", command=self.master.image_canvas.image_processor.undo)
        self.button_undo.grid(row=7, column=0, padx=10, pady=10, sticky="w")

        self.button_reset = customtkinter.CTkButton(self, text="Reset", command=self.master.image_canvas.image_processor.reset)
        self.button_reset.grid(row=8, column=0, padx=10, pady=10, sticky="w")
                


    def open_image(self,*args):
        f_types = [('All Image Files', '*.{.bmp .dib .gif .jfif .jpe .jpg .jpeg .png .apng  .hdf .jp2 .j2k .jpc .jpf .jpx .j2c .icns .ico .im .iim .mpg .mpeg .tif .tiff}'), ('.BMP Files', '*.bmp'), ('.DIB Files', '*.dib'), ('.GIF Files', '*.gif'), ('.JFIF Files', '*.jfif'), ('.JPE Files', '*.jpe'), ('.JPG Files', '*.jpg'), ('.JPEG Files', '*.jpeg'), ('.PNG Files', '*.png'), ('.APNG Files', '*.apng'), ('.HDF Files', '*.hdf'), ('.JP2 Files', '*.jp2'), ('.J2K Files', '*.j2k'), ('.JPC Files', '*.jpc'), ('.JPF Files', '*.jpf'), ('.JPX Files', '*.jpx'), ('.J2C Files', '*.j2c'), ('.ICNS Files', '*.icns'), ('.ICO Files', '*.ico'), ('.TIF Files', '*.tif'), ('.TIFF Files', '*.tiff')]
        #supported_formats = Image.registered_extensions()

        # Construct a list of tuples in the format you provided
        #f_types = [(f"{format.upper()} Files", f"*{format.lower()}") for format in supported_formats]
        #f_types.insert(0, ("All Image Files", "*.{" + " ".join(supported_formats).lower() + "}"))

        filename= filedialog.askopenfilename(filetypes=f_types)
        if (filename):
            im = Image.open(filename)
            self.master.image_canvas.impil_initial = im

            self.master.image_canvas.showImage(im=im, initial=True)
                        
                
    def save_image_as(self,*args):
        file = None
        if(self.master.image_canvas.impil_processed):
            files = [('PNG Files','*.png'), ('.JPG Files', '*.jpg'), ('.JPEG Files', '*.jpeg'),('.GIF Files', '*.gif'),('.BMP Files', '*.bmp')]
            file = filedialog.asksaveasfilename(filetypes = files, defaultextension = files) 
            extension = Path(file).suffix
            if (file):
                if extension == '.png':
                    try:
                        self.master.image_canvas.impil_processed.save(file, format='PNG')
                    except Exception as e:
                        CTkMessagebox(title="Error", message=f"An error occurred while saving the image: {e}", icon="cancel")
                else:
                    try:
                        self.master.image_canvas.impil_processed.save(file)
                    except Exception as e:
                        if (str(e)=="cannot write mode RGBA as JPEG" or str(e)=="cannot write mode P as JPEG"):
                            CTkMessagebox(title="Info", message="Transparent areas will be lost in jpg/jpeg format.")
                            im = self.master.image_canvas.impil_processed.convert('RGB')
                            im.save(file)
                        else:
                            CTkMessagebox(title="Error", message=f"An error occurred while saving the image: {e}", icon="cancel")
                            
        else:
            CTkMessagebox(title="Info", message="No images found to save.")
