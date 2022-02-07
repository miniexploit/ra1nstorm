import subprocess
import sys
import subprocess
import usb.core
def get_devinfo():
	out = subprocess.run(('irecovery','-q'), stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, universal_newlines=True).stdout
		
	for st in out.splitlines():
		if "MODEL" in st:
			board = st.replace("MODEL: ", "")
		if "PRODUCT" in st:
			identifier = st.replace("PRODUCT: ", "")
		if "ECID" in st:
			ecid = st.replace("ECID: ", "")
	try:
		return identifier, identifier[:identifier.find(",")].lower(), board, ecid
	except UnboundLocalError:
		sys.exit("[ERROR] Unable to get device info, make sure irecovery version is >= 1.0.1. Exiting.")
def detect_device():
	device = usb.core.find(idVendor=0x5AC, idProduct=0x1227)
	if device is None:
		sys.exit("[ERROR] A DFU device was not found. Exiting.")
	print("Device info:", device.serial_number)
	if "PWND:[" not in device.serial_number:
		sys.exit("[ERROR] Device's not in pwned DFU mode. Exiting.")
def check_bb(identifier):
	cellular_ipad = [
			'iPad4,2',
			'iPad4,3',
			'iPad4,5',
			'iPad4,6',
			'iPad4,8',
			'iPad4,9',
			'iPad5,2',
			'iPad5,4',
			'iPad6,8',
			'iPad6,4',
			'iPad7,2',
			'iPad7,4',
			'iPad8,3',
			'iPad8,4',
			'iPad8,7',
			'iPad8,8',
			'iPad8,10',
			'iPad8,12',
			'iPad11,2',
			'iPad11,4',
			'iPad13,2']
	if "iPhone" in identifier:
		return True
	return identifier in cellular_ipad
