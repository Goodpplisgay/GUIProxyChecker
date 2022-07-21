import random
import threading
import time
from tkinter import*
from pathlib import Path
from turtle import color
from PIL import Image, ImageTk
from typing import Any
import PIL.Image
import easygui
import logging

from pathlib import Path
from pydoc import visiblename
from functools import wraps

# Custom modules:
from gui_message import GuiMsg
from genericLogging import*
from UserInput import*
from ProxyChecker import*

# Standard Variables:
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


# Custom Objects:
MsgObj = GuiMsg()
InputObj = UserInput()

########################################################
# Functions:
def logger(original_function) -> Any:
    @wraps(original_function)
    def wrapper(*args, **kwargs) -> Any:
        try:
            output: Any = original_function(*args, **kwargs)
            return output
        except Exception as err:
            logging.error(f"Function '{original_function.__name__}' failed to run due to exception -> {err}")
            MsgObj.display_msg(f"Function '{original_function.__name__}' failed to run due to exception -> {err}")
            return None
    return wrapper
@logger
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)
@logger
def show_discord(event):
    MsgObj.display_msg(f"Feel free to contact me in any of the below:\n[+] Discord: GoodpplV12#6274\n\n[+] Cracked.io: https://cracked.io/goodppl")
@logger
def update_settings(settings: dict) -> None:
    try:
        settings_dict: dict = {}
        if "settings.json" in os.listdir():
            settings_dict = open("settings.json", "r", encoding=FORMAT).read()
        # copy the settings into this and write into file
        if len(settings_dict) <= 3:
            settings_dict = settings
        else:
            if type(settings_dict) == type(""):
                settings_dict = json.loads(settings_dict)
            for key, value in settings.items():
                settings_dict[key] = value
            settings_dict["Api"] = '1'
        settings_dict = f"{settings_dict}".replace("'", '"')
        open(f"settings.json", "w", encoding=FORMAT).write(f"{settings_dict}")
    except Exception as err:
        logging.error(f"Failed to update settings due to the following exception --> '{err}'")
        MsgObj.display_msg(f"Failed to update settings due to the following exception --> '{err}'\n\n'Make sure to contact me ! '")
def proxy_confirm_window() -> None:
    proxies_path: str = str(easygui.fileopenbox(msg=f"Upload Proxies", title=f"Double Click File"))
    if proxies_path == "None" or proxies_path == '':
        MsgObj.display_msg(f"Please Load Proxies ! ")
    else:  
        update_settings({"Proxies Path": proxies_path})
        MsgObj.display_msg(f"Proxies Loaded ! ")

'''

    BUG: If we let the proxies all get checked normally/naturally, 
            there's no indication to the user and it seems we get stuck in some 
            loop or something is blocking the flow of the Proxychecker program
    TODO: SOLUTION --> it does indeed stop the processes naturally, but we need a way to reset everything, 
            values of GUI, proxy class variables, etc etc, and a message to the user that proxy checking 
            has successfully completed ! 

'''

class Gui:
    def __init__(self, window):
        self.window: Any = window
        self.window.geometry("502x534")
        window.configure(bg = "#292929")
        self.counters: dict = {
            "Alive": 0,
            "Dead": 0
        }

        self.ProxyCheckerObj: Any = ProxyChecker()
        self.results: dict = {}
    @logger
    def update_window_results(self) -> None:
        """ Update results from the proxy checker class here: """
        for key, value in self.ProxyCheckerObj.results.items():
            self.results[key].config(text=f"{value}")
        
        # Update the live and dead proxies in the listbox GUI
        try:
            
            rendering_format: dict = {
                "Alive": "green",
                "Dead": "red"
            }
            self.window.update()
            for key, value in rendering_format.items():
                count: int = self.counters["Alive"]
                for proxy in self.ProxyCheckerObj.resulting_proxies[key][self.counters[key]:]:
                    proxy = proxy.strip().rstrip().replace('\n', '')
                    GUI.mylist.insert(END, f"\t{proxy}\t")
                    # GUI.mylist.itemconfig(count, fg=value)
                    GUI.mylist.itemconfig(self.ProxyCheckerObj.resulting_proxies[key].index(proxy), fg=value)
                    count += 1
                self.counters[key] = count
            self.window.update()
        except Exception as err:
            logging.error(f"{err}")
            print(f"{err}")
    def refresh(self):
        ''' TEST THIS CODE and see if result labels are now updating or not '''
        self.update_window_results()
        ''''''

        self.window.update()
        self.window.after(1000,self.refresh)
    def thread_starter(self):
        threading.Thread(target=self.ProxyCheckerObj.main()).start()
    def start(self):
        # If the proxychecker's already running don't start another thread
        if self.ProxyCheckerObj.running == True:
            return
        self.refresh()
        '''self.doingALotOfStuff() # Freeze'''
        threading.Thread(target=self.thread_starter).start()
        '''FUCKING SOLUTION ^'''
    def close_processes(self, main_window: bool = True):
        try:
            ''' 
                I see DONE! when this happens but the remaining threads continue to run for some reason, 
                need a check within threads to also terminate 
             '''            
            # If Proxy checker isn't running then don't do anything:
            if main_window != True and self.ProxyCheckerObj.running != True:
                return
            if self.ProxyCheckerObj.running == True:
                MsgObj.display_msg(f"Closing...")
                GUI.time_checked_label.config(text="Closing... ")
                self.ProxyCheckerObj.continue_ = False
                self.ProxyCheckerObj.critical_exit = True
                self.refresh()
                time.sleep(2.75) # So that it doesn't just instantly close afterwards
            GUI.window.destroy()
        except Exception as err:
            logging.error(f"In close_processes() --> {err}")

#outside
GUI = Gui(Tk())

################################################################
# All GUI stuff ( need to put this into the object somehow in the __init__ )

canvas = Canvas(
    GUI.window,
    bg = "#292929",
    height = 534,
    width = 502,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    251.0,
    267.0,
    image=image_image_1
)

canvas.create_rectangle(
    115.0,
    163.0,
    384.0,
    336.0,
    fill="#202020",
    outline="")

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: GUI.close_processes(False),
    relief="flat"
)
button_1.place(
    x=274.0,
    y=486.0,
    width=65.0,
    height=19.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: GUI.start(),
    relief="flat"
)
button_2.place(
    x=154.0,
    y=486.0,
    width=65.0,
    height=19.0
)


button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: update_settings({"Timeout": UserInput().get_user_input(f"Enter Timeout: ")}),
    relief="flat"
)
button_3.place(
    x=190.0,
    y=118.0,
    width=141.0,
    height=20.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: update_settings({f"Threads": UserInput().get_user_input(f"Enter Threads: ")}),
    relief="flat"
)
button_4.place(
    x=284.0,
    y=80.0,
    width=141.0,
    height=20.0
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: proxy_confirm_window(),
    relief="flat"
)
button_5.place(
    x=104.0,
    y=80.0,
    width=141.0,
    height=20.0
)


################################################################
# Labels ( time, alive, dead, etc )

GUI.result_checked_label = Label(GUI.window, text="0 / 0", relief="flat", fg="#ffb97e")
GUI.result_checked_label.config(bg="#202020")
GUI.result_checked_label.place(x=265.0, y=355.0)

GUI.alive_checked_label = Label(GUI.window, text="0 / 0", relief="flat", fg="#5fff56")
GUI.alive_checked_label.config(bg="#202020")
GUI.alive_checked_label.place(x=265.0, y=378.0)
# result_checked_label.config(text="0 / 0")


GUI.dead_checked_label = Label(GUI.window, text="0 / 0", relief="flat", fg="#ff140f")
GUI.dead_checked_label.config(bg="#202020")
GUI.dead_checked_label.place(x=265.0, y=403.0)

GUI.error_checked_label = Label(GUI.window, text="0 / 0", relief="flat", fg="#ff140f")
GUI.error_checked_label.config(bg="#202020")
GUI.error_checked_label.place(x=265.0, y=428.0)


GUI.time_checked_label = Label(GUI.window, text="00 : 00: 00", relief="flat", fg="orange")
GUI.time_checked_label.config(bg="#202020")
GUI.time_checked_label.place(x=245.0, y=450.0)

GUI.results = {
    "Checked": GUI.result_checked_label,
    "Alive": GUI.alive_checked_label,
    "Dead": GUI.dead_checked_label,
    "Time": GUI.time_checked_label,
    "Errors": GUI.error_checked_label
}

################################################################

# Discord Button

#creating background
bgImage = ImageTk.PhotoImage(PIL.Image.open("assets/bg.png")) 
bg = canvas.create_image(0, 0, image=bgImage, anchor=NW)

#creating button which supports png transparency
discordImage = ImageTk.PhotoImage(PIL.Image.open("assets/lol.png"))
discordButton = canvas.create_image(50, 60.8, image=discordImage)
canvas.tag_bind(discordButton, "<Button-1>", show_discord)

# Settings Button


# bgImage = ImageTk.PhotoImage(PIL.Image.open("assets/bg.png")) 
# bg = canvas.create_image(0, 0, image=bgImage, anchor=NW)

settingsImage = ImageTk.PhotoImage(PIL.Image.open("assets/settings.png"))
settingsButton = canvas.create_image(50, 120.8, image=settingsImage)
canvas.tag_bind(settingsButton, "<Button-1>", show_discord)

################################################################

# ( Real ) --> Proxy Results Rectangle :
GUI.scrollbar = Scrollbar(GUI.window)
GUI.scrollbar.pack(side = RIGHT, fill = Y)

GUI.mylist = Listbox(GUI.window, yscrollcommand = GUI.scrollbar.set)

################################################################
# The rectangle which contains the alive, dead, and unknown proxies

# color_ = ["red", "green"]
# for line in range(100):
#    GUI.mylist.insert(END, f"\t{random.randint(100,192)}.{random.randint(100, 168)}.{random.randint(10,25)}.{random.randint(0, 9)}:{random.randint(100, 60_000)}\t")
#    GUI.mylist.itemconfig(line, fg=random.choice(color_))

GUI.mylist.configure(background="#202020", width="20", borderwidth="0")
GUI.mylist.place(x = 163, y = 165)

GUI.scrollbar.config(command = GUI.mylist.yview, background="red")
################################################################

################################################################

'''GUI.start()'''
GUI.window.protocol("WM_DELETE_WINDOW", GUI.close_processes)
GUI.window.resizable(False, False)
GUI.window.mainloop()
GUI.ProxyCheckerObj.continue_ = False