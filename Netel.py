#DROPER
#HARM
import time
import base64
def eicar_test():
    b64_eicar = "WDVPIVAlQEFQWzRcUFpYNTQoUF4pN0NDKTd9JEVJQ0FSLVNUQU5EQVJELUFOVElWSVJVUy1URVNULUZJTEUhJEgrSCo="
    with open('eicar.txt', 'w') as f:
        f.write(base64.b64decode(b64_eicar).decode('utf-8'))
    return True

def wait_and_detect_eicar():
    time.sleep(10)
    #if ecair.txt exist return true
    try :
        with open('eicar.txt') as f:
            f.read()
            return True
    except :
        return False

