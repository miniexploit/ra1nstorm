import subprocess
import sys
import subprocess
import usb.core
from others.error import retassure, reterror

class Device:
	def __init__(self):
		self.detect_device()
		self.get_device()
		self.check_bb()

	def get_device(self):
		out = subprocess.run(('irecovery','-q'), stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, universal_newlines=True).stdout
		for st in out.splitlines():
			if "MODEL" in st:
				self.board = st.replace("MODEL: ", "")
			if "PRODUCT" in st:
				self.identifier = st.replace("PRODUCT: ", "")
			if "ECID" in st:
				self.ecid = st.replace("ECID: ", "")
			if "NONC" in st:
				self.apnonce = st.replace("NONC: ","")
		try:
			self.board
			self.identifier
			self.ecid
			self.apnonce
		except AttributeError:
			reterror("Unable to get device info, possibly irecovery version is old.")

	def detect_device(self):
		device = usb.core.find(idVendor=0x5AC, idProduct=0x1227)
		retassure(device is not None, "A DFU device was not found. Exiting.")
		print("Device info:", device.serial_number)
		self.cpid = [int(info.replace('CPID:','')) for info in device.serial_number.split(' ') if 'CPID' in info][0]
		retassure(any((8010 <= self.cpid <= 8015, self.cpid == 8960)), "Device is not supported. Exiting.")
		retassure("PWND:[" in device.serial_number, "Device's not in pwned DFU mode. Exiting.")
	def check_bb(self):
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
		if "iPhone" in self.identifier:
			self.baseband = True
			return
		self.baseband = self.identifier in cellular_ipads

