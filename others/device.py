import subprocess
import sys
import subprocess
import usb.core
from others.error import retassure, reterror


def issupported(identifier):
	supported_devices = [
	'iPhone6,1', 'iPhone6,2', 'iPhone7,1', 'iPhone7,2', 'iPhone8,1', 'iPhone8,2', 'iPhone9,1', 'iPhone9,2', 'iPhone9,3', 'iPhone9,4', 'iPhone10,1', 'iPhone10,2', 'iPhone10,3', 'iPhone10,4', 'iPhone10,5', 'iPhone10,6',
	# iPad
	'iPad4,1', 'iPad4,2', 'iPad4,3', 'iPad4,5', 'iPad4,6', 'iPad4,8', 'iPad4,9', 'iPad5,1', 'iPad5,2', 'iPad5,4', 'iPad6,4', 'iPad6,8', 'iPad7,2', 'iPad7,4', 'iPad8,3', 'iPad8,4', 'iPad8,7', 'iPad8,8', 'iPad8,10', 'iPad8,12', 'iPad11,2', 'iPad11,4', 'iPad13,2'
	]
	return identifier in supported_devices
def get_devinfo():
	out = subprocess.run(('irecovery','-q'), stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, universal_newlines=True).stdout
		
	for st in out.splitlines():
		if "MODEL" in st:
			board = st.replace("MODEL: ", "")
		if "PRODUCT" in st:
			identifier = st.replace("PRODUCT: ", "")
		if "ECID" in st:
			ecid = st.replace("ECID: ", "")
		if "NONC" in st:
			apnonce = st.replace("NONC: ","")
	return identifier, board, ecid, apnonce
def detect_device():
	device = usb.core.find(idVendor=0x5AC, idProduct=0x1227)
	retassure(device is not None, "A DFU device was not found. Exiting.")
	print("Device info:", device.serial_number)
	retassure("PWND:[" in device.serial_number, "Device's not in pwned DFU mode. Exiting.")
def check_bb(identifier):
	cellular_ipads = [
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
	return identifier in cellular_ipads
