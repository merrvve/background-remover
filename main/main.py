import customtkinter
from menubar import MenubarFrame
from navbar import NavbarFrame
from zoomframe import ZoomFrame
from loadingwindow import LoadingWindow
from imageprocessor import import_custom_modules
from imagecanvas import ImageCanvas
from utils import resource_path
from CTkXYFrame import *
from threading import Thread

customtkinter.set_appearance_mode("light")  
customtkinter.set_default_color_theme("dark-blue")





class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.is_dark=False
        self.loaded= False
        self.geometry("800x500")
        self.toplevel_window = None
        Thread(target=self.import_modules).start()
        
        self.title("Background Remover")

        self.logger = customtkinter.CTkLabel(master=self, text="Loading...")
        self.logger.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ws")
        
        
        self.sframe = CTkXYFrame(self)
        self.sframe.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.image_canvas = ImageCanvas(self.sframe, log=self.logger, width=700, height=400)
        self.image_canvas.grid(row=0, column=0, sticky="nsew",padx=5, pady=5)
        
        self.zoom_frame = ZoomFrame(master=self)
        self.zoom_frame.grid(row=1, column=1, padx=2, pady=2 , sticky="se")

        self.navbar_frame = NavbarFrame(master=self)
        self.navbar_frame.grid(row=0, column=0, padx=2, pady=2)

        self.menubar = MenubarFrame(master=self)
        self.config(menu=self.menubar)
        
        
        
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(0, weight=8)
        
    def change_log(self,log):
        self.logger.configure(text=log)
        
    def change_mod(self):
        if self.is_dark:
            customtkinter.set_appearance_mode("light")  
            self.is_dark=False
        else:
            customtkinter.set_appearance_mode("dark")  
            self.is_dark=True
            
    def import_modules(self):
        toplevel_window = LoadingWindow(msg="Loading modules...")
        toplevel_window.focus()
        self.change_log("Loading necessary modules...")
        self.iconify()
        
        import_custom_modules()
        toplevel_window.destroy()
        self.config(cursor="arrow")
        self.deiconify()
        self.change_log("Ready")
        
    
def main():
    app = App()
    app.mainloop()
    

if __name__ == "__main__":
    main()

        


