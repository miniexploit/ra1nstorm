import sys, os
import subprocess
import glob
import time
from others.error import retassure
import time

class RestoreBootchain:
	def __init__(self, ibss, ibec, ramdisk=None, kernelcache=None):
		self.ibss = ibss
		self.ibec = ibec
		if ramdisk and kernelcache:
			self.ramdisk = ramdisk
			self.kernelcache = kernelcache

class Restore:
	def __init__(self, device_struct, bootchain, ipsw, update):
		self.device = device_struct
		self.bootchain = bootchain
		self.ipsw = ipsw
		self.update = update

	def save_blobs(self, save_path, bm=None):
		print("Saving temporary SHSH...")
		args = [
			'tsschecker',
			'-d',
			self.device.identifier,
			'-B',
			self.device.board,
			'-e',
			self.device.ecid,
			'-s',
			'--save-path',
			save_path,
			'--nocache'
		]
		if bm:
			args.append('-m')
			args.append(bm)
			args.append('--apnonce')
			args.append(self.device.apnonce)
			
		else:
			args.append('-l')
		retassure(subprocess.run(args, stdout=subprocess.DEVNULL, universal_newlines=True).returncode == 0, "Failed to save SHSH blobs")
		if bm:
			self.ota_blob = glob.glob(f"{save_path}/*.shsh*")[0]
		else:
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

	def restore(self, custom_blob=None, log_path=None, ota=False, sep=None, bb=None, bm=None):
		if sep:
			print("Restoring device with OTA method...")
		else:
			print("Restoring device...")
		if custom_blob and not ota:
			args = [
				'futurerestore',
				'-t',
				custom_blob,
				'--skip-blob',
				'--use-pwndfu',
				'--ibss-img4',
				self.bootchain.ibss,
				'--ibec-img4',
				self.bootchain.ibec
			]	
		else:	
			args = [
					'futurerestore',
					'-t',
					self.blob if not ota else self.ota_blob,
					'--use-pwndfu',
					'--skip-blob',
					'--ibss-img4',
					self.bootchain.ibss,
					'--ibec-img4',
					self.bootchain.ibec
				]

		if sep and bb and bm:
			args.append('-s')
			args.append(sep)
			args.append('-m')
			args.append(bm)
			args.append('-b')
			args.append(bb)
			args.append('-p')
			args.append(bm)
			args.append('--ota')
		else:
			args.append('--latest-sep')
			args.append('--rdsk')
			args.append(self.bootchain.ramdisk)
			args.append('--rkrn')
			args.append(self.bootchain.kernelcache)
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
			result = subprocess.run(args, universal_newlines=True)
			retassure(result.returncode == 0, f'Restore failed ({result.returncode})')
			print('Restore succeeded!')
