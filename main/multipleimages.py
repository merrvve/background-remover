import customtkinter
from tkinter import filedialog
from loadingwindow import LoadingWindow
from CTkMessagebox import CTkMessagebox

class MultipleImagesDialog(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Remove Background of Multiple Images')
        self.geometry('500x300')
        self.image_folder=""
        self.result_folder_name=""
        

        self.open_label_name = customtkinter.CTkLabel(self, text=self.image_folder)
        self.open_label_name.grid(row=0,column=1,padx=5,pady=5)

        self.button_open = customtkinter.CTkButton(self, text="Images Folder", command=self.open_folder)
        self.button_open.grid(row=0,column=0, padx=10, pady=20)


        self.result_label_name = customtkinter.CTkLabel(self, text=self.result_folder_name)
        self.result_label_name.grid(row=1,column=1,padx=5,pady=5)

        self.button_result = customtkinter.CTkButton(self, text="Results Folder", command=self.result_folder)
        self.button_result.grid(row=1,column=0, padx=10, pady=10)

        self.button_start = customtkinter.CTkButton(self, text="Start", command=self.remove_backgrounds)
        self.button_start.grid(row=3,column=1, padx=10, pady=10, sticky='se')


        self.button = customtkinter.CTkButton(self, text="Close", command=self.ok_button_click)
        self.button.grid(row=3,column=2, padx=10, pady=10, sticky='se')

    def folder(self):
        folder = filedialog.askdirectory()
        if folder:
            return folder
        else:
            return ""
            
    def open_folder(self):
        self.image_folder = self.folder()
        self.open_label_name.configure(text="Images Folder: " + self.image_folder.split('/')[-1])

    def result_folder(self):
        self.result_folder_name = self.folder()
        self.result_label_name.configure(text="Result Folder: " + self.result_folder_name.split('/')[-1])

    def remove_backgrounds(self):
        try:
            dialog = LoadingWindow(msg="Removing background from images... Please do not close this dialog...")
            dialog.lift()
            dialog.focus_force()
            dialog.grab_set()
            #remove_backgrounds
            dialog.destroy()
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred while removing backgrounds:  {e}", icon="cancel")   

    def ok_button_click(self):
        self.destroy()
