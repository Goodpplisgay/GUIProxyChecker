from tkinter import *
from tkinter import ttk
from gui_message import GuiMsg
from typing import Any
from genericLogging import *

MsgObj = GuiMsg()

class UserInput:
    def __init__(self) -> None:
        self.string: str = ""
        self.entry: Any = None
    def display_text(self) -> str:
        try:
            self.string = f"{self.entry.get()}"
            self.win__.destroy()
            print(f"{self.string}")
            return self.string
        except Exception as err:
            print(f"{err}")
            pass
    def get_user_input(self, msg: str) -> str:
        try:
            #Create an instance of Tkinter frame
            self.win__: Any = Toplevel()
            #Set the geometry of Tkinter frame
            self.win__.geometry("300x100")    
            #Initialize a Label to display the User Input
            label=Label(self.win__, text=f"hi", font=("Courier 15 bold"))
            label.pack()
            label.configure(text=f"{msg}")
            #Create an Entry widget to accept User Input
            self.entry = Entry(self.win__, width = 20)
            self.entry.focus_set()
            self.entry.pack()
            #Create a Button to validate Entry Widget
            ttk.Button(self.win__, text= "Continue", width= 20, command=self.display_text).pack(pady=10)
            self.win__.resizable(True, True)
            self.win__.wait_window()
        except Exception as err:
            logging.error(f"When getting user input the following error occured -> {err}\nPlease report this to us ! ")
            MsgObj.display_msg(f"When getting user input the following error occured -> {err}\nPlease report this to us ! ")
            return f"Error"
        finally:
            return self.string