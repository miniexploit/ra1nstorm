import os, sys
import shutil
import psutil
import subprocess
from others.error import retassure, reterror

class check_requirements:
	def __init__(self):
		print("Checking dependencies...")
		self.check_bin('futurerestore')
		self.check_bin('img4')
		self.check_bin('img4tool')
		self.check_bin('irecovery')
		self.check_bin('tsschecker')
		self.check_bin('Kernel64Patcher')
		self.check_bin('Kairos')
		self.check_bin('ldid')
		self.check_bin('asr64_patcher')
		print("Checking hard disk free space...")
		self.check_space()
	def check_bin(self, binary):
		retassure(shutil.which(binary) is not None, f"{binary} not found, make sure it's in PATH")
		if binary == "irecovery":
			try: # check
				subprocess.check_call((binary, '-V'), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
			except subprocess.CalledProcessError:
				reterror("This irecovery version is too old. Exiting.")
			irecv_ver = subprocess.run((binary, '-V'), stdout=subprocess.PIPE, universal_newlines=True).stdout.replace("irecovery ","") # double check
			retassure(int(irecv_ver[:-1].replace(".", "")) >= 101, f"Expected irecovery version to be greater than or equal to 1.0.1 but found version {irecv_ver}. Exiting.")
		elif binary == "futurerestore":
			fr_usage = subprocess.run((binary), stdout=subprocess.PIPE, universal_newlines=True).stdout
			retassure(not any(("--rdsk" not in fr_usage, "--rkrn" not in fr_usage, "--skip-blob" not in fr_usage)), "This Futurerestore build does not allow specifying custom ramdisk and kernelcache. Exiting.")
	def check_space(self):
		disk = psutil.disk_usage('/')
		if disk.free / (2**30) < 3:
			reterror("Less than 3GB free space on this computer. Exiting.")
