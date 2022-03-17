import subprocess
import sys
import time
import subprocess
import usb.core
from others.error import retassure, reterror
from others.irecv_devices_struct import irecv_device, irecv_devices


class Device:
	def __init__(self):
		self.cpid = None
		self.bdid = None
		self.ecid = None
		self.identifier = None
		self.board = None
		self.get_device()
		retassure(not any((self.cpid is None, self.bdid is None, self.ecid is None, self.identifier is None, self.board is None)), "Could not get device info")
		self.check_bb()

	def get_device(self):
		device = usb.core.find(idVendor=0x5AC, idProduct=0x1227)
		retassure(device is not None, "No DFU device found")
		print("Device info:", device.serial_number)
		self.cpid = [int(info.replace('CPID:','')) for info in device.serial_number.split(' ') if 'CPID' in info][0]
		self.bdid = [int(info.replace('BDID:',''), 16) for info in device.serial_number.split(' ') if 'BDID' in info][0]
		self.ecid = [info.replace('ECID:','') for info in device.serial_number.split(' ') if 'ECID' in info][0]
		retassure(any((8010 <= self.cpid <= 8015, self.cpid == 8960)), "Device is not supported")
		retassure("PWND:[" in device.serial_number, "Device's not in pwned DFU mode")
		for device in irecv_devices:
			if device.cpid == self.cpid and device.bdid == self.bdid:
				self.identifier = device.product_type
				self.board = device.hardware_model
				break
		
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

