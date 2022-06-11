#EVASION
#HEAR
#get all process actually running
from mimetypes import init
from typing import final
import psutil
import pyautogui


def do_keyboard_hotkey(input_list :list):
    #do keyboard hotkey
    final_lst = []
    for command in input_list :
        final_lst.append(f"'{command}'")
    final_str= ",".join(final_lst)
    eval(f"pyautogui.hotkey({final_str})")



def get_all_process():
    process_list = {}
    for proc in psutil.process_iter():
        #add process to dict with pid as key
        process_list[proc.pid] = proc.name()
    return process_list


def detect():
    detect_list = ["Deezer.exe","brave.exe"]
    final_list = {}
    #get all process actually running
    process_list = get_all_process()
    #get all process running in background
    for proc in psutil.process_iter():
        if proc.name() in detect_list:
            print(proc.name, "detected")
            #check if process is running in background
            if proc.is_running():
                print(proc.name, "is running in background")
                #check if process is not running in foreground
                final_list[proc.pid] = proc.name()
                if not proc.is_running():
                    print(proc.name, "is not running in foreground")
                    
    return final_list

def try_kill(pid):
    try:
        #try to kill process
        psutil.Process(pid).kill()
        print("Process with pid: ", pid, " killed")
    except:
        print("Process with pid: ", pid, " not killed")

def main():
    dangerous= detect()
    if dangerous != {}:
        for pid in dangerous:
            try_kill(pid)
    else:
        print("No dangerous process detected")

do_keyboard_hotkey(["alt","z"])
