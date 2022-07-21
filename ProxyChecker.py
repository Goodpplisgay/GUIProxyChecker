import socket
import json
import os
import sys
import time
import threading
import requests
import cloudscraper
from concurrent.futures import ThreadPoolExecutor
from urllib3.exceptions import InsecureRequestWarning
from datetime import datetime, timedelta
from typing import Any, IO

# Custom modules:
from Exceptions import NotExists
from gui_message import GuiMsg
from genericLogging import*


'''
- Need to add support for authenticated proxies for both APIs as well
- The settings will ask which Proxy Checking API they want to use later
    - Use CloudFlare V1.0 bypass, or just regular requests (faster, less accurate)
        - Retries (default): 2
    - Site to check against, etc etc

'''


########################################################################
# Configuration(s):
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
########################################################################
#  Variables:
MsgObj = GuiMsg()
FORMAT: str = sys.getfilesystemencoding()
########################################################################
# Functions:
def config_loader(config_path: str, mandatory_keys: list) -> dict:
    try:
        str_mandatory_keys: str = (" ".join(mandatory_keys)).strip().lower()
        print(str_mandatory_keys)
        if os.path.exists(config_path) != True:
            MsgObj.display_msg(f"Please enter in your timeout, proxies, and number of threads ! ")
            return {}
        settings: str = open(f"{config_path}", "r", encoding=FORMAT).read()
        if len(settings) <= 3:
            MsgObj.display_msg(f"Please enter in your timeout, proxies, and number of threads ! ")
            return {}
        else:
            settings = json.loads(settings)
        print(f"settings.keys() -> {settings.keys()}")
        for key in mandatory_keys:
            print(f"if {key.strip().lower()} not in {(' '.join(settings.keys())).lower()} --> {key.strip().lower() not in (' '.join(settings.keys())).lower():}")
            if key.strip().lower() not in (' '.join(settings.keys())).lower():
                MsgObj.display_msg(f"Please specify your '{key}' ! ")
                return {}
        return settings
    except Exception as err:
        logging.error(f"An exception occured when loading configuration(s) --> {err}")
        MsgObj.display_msg(f"An exception occured when loading configuration(s) --> {err}")
########################################################################

class ProxyChecker:
    def __init__(self) -> None:
        # Will have a simple function which iterates through the ProxyChecker results and updates the GUI's labels
        self.settings: dict = {}
        self.results: dict = {
            "Checked": 0,
            "Alive": 0,
            "Dead": 0,
            "Time": "0:0:0:0",
            "Errors": 0
        }
        self.result_files: dict = {}
        self.continue_: bool = True # Can be switched at moments notice via the "STOP" button in the GUI
        self.running: bool = False
        self.critical_exit: bool = False

        self.proxies: list = []

        # Don't need to thread lock, will be using a dynamic index in gui_better.py to keep track of dead proxy list
        self.resulting_proxies: dict = {
            "Alive": [],
            "Dead": []
        }
        
    def clean_proxies(self, proxies: list) -> list:
        cleaned_proxies: list = []
        try:
            for proxy in list(set(proxies)):
                if type(proxy) == type(b""):
                    proxy = proxy.decode(FORMAT)
                proxy = proxy.strip().rstrip().replace('\n', '').replace(' ', '')
                if len(proxy) < 5 or proxy.count('.') < 3 or ':' not in proxy:
                    self.record_result(f"{proxy} --> Invalid Format", "Dead")
                    continue
                cleaned_proxies.append(proxy)
            return cleaned_proxies
        except Exception as err:
            logging.error(f"when cleaning proxies exception occured -> '{err}'")
            MsgObj.display_msg(f"when cleaning proxies exception occured -> '{err}'")
            return cleaned_proxies
    def record_result(self, line: str, key: str) -> None:
        try:
            self.resulting_proxies[key].append(line.replace('\n', '').strip().rstrip())
            line = f"{line}\n" if '\n' not in line else line    
            self.result_files[key].write(f"{line}")
            self.result_files[key].flush()
            self.results[key] += 1
            self.results["Checked"] = f'{self.results["Alive"]+self.results["Dead"]:,}/{len(self.proxies):,}'
        except Exception as err:
            logging.error(f"When writing line --> '{line}' due to exception -> '{err}'")
    def counter(self) -> None:
        def CalculateTimePassed(current: float, start: float) -> str:
            sec = timedelta(seconds=int(current-start))
            d = datetime(1,1,1) + sec
            time_passed: str = "%d:%d:%d:%d" % (d.day-1, d.hour, d.minute, d.second)
            return time_passed
        start: float = time.time()
        while self.continue_:
            current: float = time.time()
            self.results["Time"] = CalculateTimePassed(current, start)
            time.sleep(3)

    def api_one_check_proxy(self, proxy: str) -> None:
        """ Uses sockets to check the proxy ( not safe since ISP will be sus why you're connecting to so many foreign IPs ) """
        if self.continue_ != True:
            return
        try:
            HOST, PORT = proxy.split(':', 1)
            PORT: int = int(PORT)
        except Exception as err:
            self.record_result(f"{proxy} --> Invalid Format", "Dead")
            logging.error(f"When trying to exract HOST and PORT from proxy --> '{proxy}'")
            return
        try:
            if self.continue_ != True:
                return
            socketObj: Any = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socketObj.settimeout(3)
            socketObj.connect((HOST, PORT))
            self.record_result(f"{proxy}", "Alive")
            print(f"Alive Proxy -> {proxy}")
        except Exception as err:
            print(f"DEAD -> {proxy}, HOST={HOST}, PORT={PORT}, Exception -> {err}")
            self.record_result(f"{proxy}", "Dead")
    def api_two_check_proxy(self, proxy: str) -> None:
        """ 
        Uses a website or a custom domain to check whether the proxy is alive against ( reccommended, can do proxy ban checking ) 
        with this feature in a sense in the future
        
        """
        ...
    def reset_values(self) -> None:
        self.results: dict = {
            "Checked": 0,
            "Alive": 0,
            "Dead": 0,
            "Time": "Completed.",
            "Errors": 0
        }
        self.running = False
        self.continue_ = True
    def thread_runner(self) -> None:
        '''Possible to do daemon=True for this threadpool in case the user closes the GUI?'''
        try:
            apis: dict = {
                '1': self.api_one_check_proxy,
                '2': self.api_two_check_proxy
            }
            # Need to make this daemon-like so that when the GUI window closes, this threadpool also terminates
            # executor = Pool()
            proxy_line: int = 0
            proxies_len: int = len(self.proxies)
            api_function: function = apis[self.settings["Api"]]
            ''' When going into production refactor this using threading events instead of this crap: '''
            self.running = True
            while self.continue_:
                try:
                    if self.continue_ != True:
                        break
                    if threading.active_count()-3 >= int(self.settings["Threads"].strip().rstrip()) and self.continue_ == True:
                        time.sleep(0.01)
                        continue
                    if proxy_line >= proxies_len:
                        break
                    proxy: str = self.proxies[proxy_line]
                    # Had to refrain from threadpool due to slow GUI closing speeds + freezing, maybe this will be better:
                    threading.Thread(target=api_function, args=(proxy,), daemon=True).start()
                    proxy_line += 1
                except Exception as err:
                    print(f"{err} [0x92738]")
                    self.results["Errors"] += 1
                    logging.error(f"When attempting to spawn a new thread the following exception occured --> '{err}'")
                    time.sleep(0.008)
                    continue
                
            # with ThreadPoolExecutor(max_workers=int(self.settings["Threads"])) as executor: # this should in theory run forever
            #     executor.map(apis[self.settings["Api"]], self.proxies)
            self.continue_ = False
            print(f"DONE ! ")
            if self.critical_exit == True:
                logging.error(f"Initiated the critical exit ! ")
                sys.exit(0)
            else:
                self.results["Time"] = "Completing..."
                while self.results["Alive"]+self.results["Dead"] != len(self.proxies):
                    time.sleep(0.01)
                    continue
                time.sleep(3.5)
                logging.error(f"Naturally completed checking all of the proxies ! ")
                MsgObj.display_msg("Finished ! ")
                self.reset_values()
                return
                # Reset all values of GUI and proxy class variables here
        except Exception as err:
            MsgObj.display_msg(f"When running threads --> {err}")
            logging.error(f"When running threads --> {err}")
    def main(self) -> None:
        try:
            mandatory_keys: list = ["Threads", "Timeout", "Proxies Path", "Api"]
            self.settings = config_loader(config_path=f"settings.json", mandatory_keys=mandatory_keys)
            if self.settings == {}: # An error occured when loading the configurations
                return
            for key in mandatory_keys:
                if len(self.settings[key]) == 0 or f"{self.settings[key]}" == ' ':
                    MsgObj.display_msg(f"Please specify '{key}', don't leave it empty ! ")
                    return
            # Check Proxies file + Load + Clean it
            if os.path.exists(self.settings["Proxies Path"]) != True:
                raise NotExists(f"Proxies file --> '{self.settings['Proxies Path']}' does not exist ! ")
            self.proxies = self.clean_proxies(list(set(open(self.settings["Proxies Path"], "rb").readlines())))
            if len(self.proxies) == 0:
                raise Exception(f"Proxies file is empty after cleaning ! ")
            # Load result files
            base_directory: str = "Proxy-Checker-Results"
            current_time: str = f"{time.time()}"
            if f"{base_directory}" not in os.listdir():
                os.mkdir(f"{base_directory}")
            os.mkdir(f"{base_directory}/{current_time}")
            # base_directory = f"{base_directory}/{current_time}"
            self.result_files = {
                "Alive": open(f"{base_directory}/{current_time}/Alive.txt", "a", encoding=FORMAT),
                "Dead": open(f"{base_directory}/{current_time}/Dead.txt", "a", encoding=FORMAT),
            }
            # Start the counter so that we can keep track of how long the program has been running for
            threading.Thread(target=self.counter, daemon=True).start()
            self.thread_runner()
        except Exception as err:
            logging.error(f"In proxyclass the following exception occured --> '{err}'")
            MsgObj.display_msg(f"In proxyclass the following exception occured --> '{err}'")