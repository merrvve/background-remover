import customtkinter

class LoadingWindow(customtkinter.CTkToplevel):
    def __init__(self, msg, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.msg=msg
        self.geometry("400x100")
        self.title('Process')
        self.config(cursor="watch")
        self.label = customtkinter.CTkLabel(self, text=self.msg)
        self.label.pack(padx=20, pady=20)