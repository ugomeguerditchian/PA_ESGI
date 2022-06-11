#SCAN
#EYES
import nmap
import os
import sys
import scapy
import requests

def test_access_to_webpage(url):
    #print("[*] Testing access to the webpage: {}".format(url))
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("[*] Access to the webpage: {}".format(url))
            return True
    except:
        print("[*] Access to the webpage: {}".format(url))
        return False

def traceroute(domain):
    #return all ip
    print()
    



def main():
    if test_access_to_webpage("https://pornhub.com"):
        print("next")
    else :
        print("other")
        