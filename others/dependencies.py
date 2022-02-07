import os, sys
import shutil
import psutil
import subprocess

class check_requirements:
	def __init__(self):
		print("Checking dependencies...")
		self.check_bin('futurerestore')
		self.check_bin('img4')
		self.check_bin('img4tool')
		self.check_bin('irecovery')
		self.check_bin('tsschecker')
		self.check_bin('Kernel64Patcher')
		self.check_bin('asr64_patcher')
		print("Checking hard disk free space...")
		self.check_space()
	def check_bin(self, binary):
		if shutil.which(binary) is None:
			sys.exit(f"[ERROR] {binary} not found, make sure it's in PATH")
		if binary == "irecovery":
			try:
				subprocess.check_call((binary, '-V'), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
			except subprocess.CalledProcessError:
				sys.exit("[ERROR] This irecovery version is too old. Exiting.")
		elif binary == "futurerestore":
			fr_usage = subprocess.run((binary), stdout=subprocess.PIPE, universal_newlines=True).stdout
			if "--rdsk" not in fr_usage or "--rkrn" not in fr_usage or "--skip-blob" not in fr_usage:
				print("[ERROR] This Futurerestore build can't be used. Exiting.")
				print("Make sure Futurerestore allows specifying ramdisk and kernel.")
				sys.exit(1)
	def check_space(self):
		disk = psutil.disk_usage('/')
		if disk.free / (2**30) < 3:
			sys.exit("[ERROR] Less than 3GB free space on this computer. Exiting.")
