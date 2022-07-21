from turtle import color
from PIL import Image, ImageTk
from typing import Any
import PIL.Image

import easygui
import logging

from pathlib import Path
from pydoc import visiblename

from tkinter import *
from functools import wraps


# Custom modules:
from gui_message import GuiMsg
from genericLogging import*
from UserInput import*
from ProxyChecker import*

# Standard Variables:
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

window = Tk()
window.geometry("502x534")
window.configure(bg = "#292929")

# Custom Objects:
MsgObj = GuiMsg()
InputObj = UserInput()
ProxyCheckerObj = ProxyChecker()

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
def close_processes() -> None:
    ProxyCheckerObj.continue_ = False
    window.destroy()
########################################################
# GUI code:


canvas = Canvas(
    window,
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
    command=lambda: print("button_1 clicked"),
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
    command=lambda: ProxyCheckerObj.main(),
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

result_checked_label = Label(window, text="0 / 0", relief="flat", fg="#ffb97e")
result_checked_label.config(bg="#202020")
result_checked_label.place(x=265.0, y=355.0)

alive_checked_label = Label(window, text="0 / 0", relief="flat", fg="#5fff56")
alive_checked_label.config(bg="#202020")
alive_checked_label.place(x=265.0, y=378.0)
# result_checked_label.config(text="0 / 0")


dead_checked_label = Label(window, text="0 / 0", relief="flat", fg="#ff140f")
dead_checked_label.config(bg="#202020")
dead_checked_label.place(x=265.0, y=403.0)

error_checked_label = Label(window, text="0 / 0", relief="flat", fg="#ff140f")
error_checked_label.config(bg="#202020")
error_checked_label.place(x=265.0, y=428.0)


time_checked_label = Label(window, text="00 : 00: 00", relief="flat", fg="orange")
time_checked_label.config(bg="#202020")
time_checked_label.place(x=245.0, y=450.0)

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
scrollbar = Scrollbar(window)
scrollbar.pack(side = RIGHT, fill = Y)

mylist = Listbox(window, yscrollcommand = scrollbar.set)



################################################################
# The rectangle which contains the alive, dead, and unknown proxies

import random
color_ = ["red", "green"]
for line in range(100):
   mylist.insert(END, f"\t{random.randint(100,192)}.{random.randint(100, 168)}.{random.randint(10,25)}.{random.randint(0, 9)}:{random.randint(100, 60_000)}\t")
   mylist.itemconfig(line, fg=random.choice(color_))

mylist.configure(background="#202020", width="20", borderwidth="0")
mylist.place(x = 163, y = 165)
# mylist.pack(side = LEFT, fill = BOTH)
scrollbar.config(command = mylist.yview, background="red")


window.protocol("WM_DELETE_WINDOW", close_processes)
window.resizable(False, False)
window.mainloop()
################################################################


'''

    Later we'll add a topLevel window which is triggered when they click the settings button which asks
    whether they want to use API #1 (check via sockets) or API #2 (check via web against a link),

    the toplevel window we can create in figma too so it matches the default theme as the main window

'''