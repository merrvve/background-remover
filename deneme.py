import time
from threading import Thread, Event
import customtkinter
class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.label = customtkinter.CTkLabel(self, text="ToplevelWindow")
        self.label.pack(padx=20, pady=20)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.is_dark = False
        self.loaded = Event()  # Event to synchronize loading
        self.toplevel_window = None
        
        # Create loading screen
        self.toplevel_window = ToplevelWindow(self)

        # Start loading modules in another thread
        thread = Thread(target=self.load_modules)
        thread.start()


    def load_modules(self):
        # Simulate loading time
        time.sleep(10)  # Adjust the sleep time as needed
        # Your module loading code here
        # For demonstration purposes, I'll just set loaded to True
        self.loaded.set()
        

    def initialize_main_window(self):
        # Initialize main window components here
        self.geometry("800x500")
        self.title("Background Remover")
        # Your other components initialization goes here

def main():
    app = App()
    app.mainloop()
    
    
if __name__ == "__main__":
    main()
