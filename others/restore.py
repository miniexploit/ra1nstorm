import sys, os
import subprocess
import glob
import time
from others.error import retassure

class RestoreBootchain:
	def __init__(self, ibss, ibec, ramdisk, kernelcache):
		self.ibss = ibss
		self.ibec = ibec
		self.ramdisk = ramdisk
		self.kernelcache = kernelcache

class Restore:
	def __init__(self, device_struct, bootchain, ipsw, update):
		self.device = device_struct
		self.bootchain = bootchain
		self.ipsw = ipsw
		self.update = update

	def save_blobs(self, save_path):
		print("Saving temporary SHSH...")
		args = [
			'tsschecker',
			'-d',
			self.device.identifier,
			'-B',
			self.device.board,
			'-e',
			self.device.ecid,
			'-l',
			'-s',
			'--save-path',
			save_path,
			'--nocache'
		]
		retassure(subprocess.run(args, stdout=subprocess.PIPE, universal_newlines=True).returncode == 0, "Failed to save SHSH blobs")
		self.blob = glob.glob(f"{save_path}/*.shsh*")[0]
			
	def sign_bootloader(self, path, output, type):
		print(f"Signing {type}...")
		args = [
			'img4',
			'-i',
			path,
			'-o',
			output,
			'-M',
			self.im4m,
			'-A',
			'-T',
			type.lower()
		]
		retassure(subprocess.run(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0, "Failed to sign bootloader")
		
	def save_im4m(self, output, custom_blob=None):
		print("Saving IM4M for signing bootchain...")
		if custom_blob:
			args = [
				'img4tool',
				'-e',
				'-s',
				custom_blob,
				'-m',
				output
			]
		else:
			args = [
				'img4tool',
				'-e',
				'-s',
				self.blob,
				'-m',
				output
			]
		retassure(subprocess.run(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0, "Failed to save IM4M")
		self.im4m = output

	def restore(self, custom_blob=None, log_path=None):
		print("Restoring device...")
		if custom_blob:
			args = [
				'futurerestore',
				'-t',
				custom_blob,
				'--skip-blob',
				'--latest-sep',
				'--use-pwndfu',
				'--ibss-img4',
				self.bootchain.ibss,
				'--ibec-img4',
				self.bootchain.ibec,
				'--rdsk',
				self.bootchain.ramdisk,
				'--rkrn',
				self.bootchain.kernelcache
			]	
		else:	
			args = [
					'futurerestore',
					'-t',
					self.blob,
					'--skip-blob',
					'--latest-sep',
					'--use-pwndfu',
					'--ibss-img4',
					self.bootchain.ibss,
					'--ibec-img4',
					self.bootchain.ibec,
					'--rdsk',
					self.bootchain.ramdisk,
					'--rkrn',
					self.bootchain.kernelcache
				]
		if self.device.baseband:
			args.append('--latest-baseband')
		else:
			args.append('--no-baseband')
		if self.update:
			args.append('-u')
		args.append(self.ipsw)
		if log_path:
			if log_path.endswith('/'):
				log_path = log_path[:-1]
			result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf8")
			with open(f'{log_path}/restore.log', 'w') as f:
				f.write(result.stdout)
			retassure(result.returncode == 0, f'Restore failed ({result.returncode}). Log saved to {log_path}/restore.log')
			print(f'Restore succeeded! Log saved to {log_path}/restore.log')
		else:
			result = subbprocess.run(args, universal_newlines=True)
			retassure(result.returncode == 0, f'Restore failed ({result.returncode})')
