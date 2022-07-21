import sys
from tkinter import *
from tkinter import ttk
from genericLogging import *

class GuiMsg:
    def __init__(self) -> None:
        ...
    def display_msg(self, msg: str, do_formatting: bool = False) -> None:
        try:
            #Create an instance of Tkinter frame
            win_ = Toplevel()

            #Set the geometry of Tkinter frame
            win_.geometry("300x170")

            Label(win_, text=f"\n", font=("Courier 15 bold")).pack()

            def close_window():
                win_.destroy()
            #Initialize a Label to display the User Input
            try:
                if do_formatting == True:
                    new_msg: str = ""
                    counter: int = 0
                    for character in msg:
                        if character == ' ' and counter >= 20 and character != '\n':
                            new_msg += f"{character}\n"
                            counter = 0
                        else:
                            new_msg += f"{character}"
                        counter += 1

                    msg = new_msg
            except Exception as err:
                print(f"In GUI_Message.py -> {err}")
                sys.exit(0)
            label=Label(win_, text=f"{msg}", font=("Courier 15 bold"))
            label.pack()

            #Create a Button to validate Entry Widget
            ttk.Button(win_, text= "OK", width= 100, command = close_window).pack(pady=10)

            win_.resizable(True, True)
        except Exception as err:
            # Need to add the Logging here and not just print it out
            logging.error(f"In 'gui_Message.py' in function 'display_msg' --> {err}")
