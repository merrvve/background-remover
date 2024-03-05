from imageprocessor import ImageProcessor
from tkinter import PhotoImage, Canvas

from PIL import Image, ImageTk

class ImageCanvas(Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.impil_initial = None
        self.impil_processed = None
        self.current_size = None
        
        self.image_processor= ImageProcessor(master=self)        

        
        self.rect = None

        self.start_x = None
        self.start_y = None
        self.x = self.y = 0
      
    def selectPoint(self):
        self.bind("<ButtonPress-1>", self.on_button_press_point)
        self.bind("<ButtonRelease-1>", self.on_button_release_point)
        self.config(cursor="target")
    def on_button_press_point(self, event):
        w, h=int(self.cget('width')),int(self.cget('height'))
        w_im, h_im = self.impil_processed.size
        ratio = w/w_im
        point = (int(event.x/ratio) , int(event.y/ratio))
        self.config(cursor="arrow")

        self.image_processor.lasso_remove(self.impil_processed,point)
        
        
        
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
            self.delete("all")
            image = ImageTk.PhotoImage(im)            
            self.config(width=w, height=h)
            self.create_image(0, 0, anchor="nw", image=image)
            self.impil_processed = im
            self.image=image
            if initial:
                if h>800:
                    x =h/800
                    newsize=(int(w/x),int(h/x))
                    self.resize(newsize)
                    self.current_size=newsize
            
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
            if not w>4000:
                self.resize(size=(w*2,h*2))
            

    def zoom_out(self):
        if self.impil_processed:
            w,h = self.current_size
            self.resize(size=(w//2,h//2))
