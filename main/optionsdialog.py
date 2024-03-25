import customtkinter
from typing import Union, Callable

class FloatSpinbox(customtkinter.CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 step_size: Union[int, float] = 1,
                 command: Callable = None,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.step_size = step_size
        self.command = command

        self.configure(fg_color=("gray78", "gray28"))  # set frame color

        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands

        self.subtract_button = customtkinter.CTkButton(self, text="-", width=height-6, height=height-6,
                                                       command=self.subtract_button_callback)
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.entry = customtkinter.CTkEntry(self, width=width-(2*height), height=height-6, border_width=0)
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")

        self.add_button = customtkinter.CTkButton(self, text="+", width=height-6, height=height-6,
                                                  command=self.add_button_callback)
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

        # default value
        self.entry.insert(0, "0.0")

    def add_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = float(self.entry.get()) + self.step_size
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return

    def subtract_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = float(self.entry.get()) - self.step_size
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return

    def get(self) -> Union[float, None]:
        try:
            return float(self.entry.get())
        except ValueError:
            return None

    def set(self, value: float):
        self.entry.delete(0, "end")
        self.entry.insert(0, str(float(value)))

class LassoOptionsDialog(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Lasso Remove Tool Options')
        self.geometry('400x150')
        
        self.input = 20  
        self.tol_label = customtkinter.CTkLabel(self, text="Tolerence:")
        self.tol_label.grid(row=0,column=0,padx=10,pady=5)

        self.spinbox = FloatSpinbox(self, width=150, step_size=1)
        self.spinbox.grid(row=0,column=1,padx=10, pady=5)
        
        self.spinbox.set(30)

        self.button = customtkinter.CTkButton(self, text="OK", command=self.ok_button_click)
        self.button.grid(row=3,column=1, padx=30, pady=30)

    def get_input(self):
        return self.input        

    def ok_button_click(self):
        try:
            self.input = self.spinbox.get()
        except ValueError:
            pass
        self.destroy()


class RemoveOptionsDialog(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Options')
        self.geometry('400x250')
        self.inputs = [0, False, False,True]  # Initialize inputs with None
        self.radius_label = customtkinter.CTkLabel(self, text="Edge blur radius:")
        self.radius_label.grid(row=0,column=0,padx=10,pady=5)
        #self.input_radius = customtkinter.CTkEntry(self, placeholder_text="0")
        #self.input_radius.grid(row=0,column=1,padx=10,pady=5)
        self.spinbox_1 = FloatSpinbox(self, width=150, step_size=1)
        self.spinbox_1.grid(row=0,column=1,padx=10, pady=5)

        self.spinbox_1.set(0)
        
        self.post_label = customtkinter.CTkLabel(self, text="Postprocess Mask:")
        self.post_label.grid(row=1,column=0,padx=10,pady=5)
        
        self.switch_var = customtkinter.BooleanVar(value=False)
        self.switch_post = customtkinter.CTkSwitch(self, text="", variable=self.switch_var, onvalue=True, offvalue=False)
        self.switch_post.grid(row=1,column=1,padx=10,pady=5)

        self.alpha_mat_label = customtkinter.CTkLabel(self, text="Alpha matting:")
        self.alpha_mat_label.grid(row=2,column=0,padx=10,pady=5)
        
        self.alpha_mat_var = customtkinter.BooleanVar(value=False)
        self.alpha_mat = customtkinter.CTkSwitch(self, text="", variable=self.alpha_mat_var, onvalue=True, offvalue=False)
        self.alpha_mat.grid(row=2,column=1,padx=10,pady=5)

        self.remove_white_label = customtkinter.CTkLabel(self, text="Remove remaining white pixels:")
        self.remove_white_label.grid(row=3,column=0,padx=10,pady=5)
        
        self.remove_white_var = customtkinter.BooleanVar(value=True)
        self.remove_white_switch = customtkinter.CTkSwitch(self, text="", variable=self.remove_white_var, onvalue=True, offvalue=False)
        self.remove_white_switch.grid(row=3,column=1,padx=10,pady=5)

        self.button = customtkinter.CTkButton(self, text="OK", command=self.ok_button_click)
        self.button.grid(row=4,column=1, padx=30, pady=30)

    def get_inputs(self):
        return self.inputs

    def ok_button_click(self):
        try:
            num1 = self.spinbox_1.get()
            num1 = int(num1) if num1 else 0
            num2 = self.switch_var.get()
            num3 = self.alpha_mat_var.get()
            num4= self.remove_white_var.get()
            self.inputs = [num1, num2, num3, num4]
        except ValueError:
            # Handle non-numeric inputs
            pass
        self.destroy()
