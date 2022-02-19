import sys, os
import subprocess
import glob
import time
from others.error import retassure

class Restore:
	def __init__(self, device_struct, ipsw):
		self.device = device_struct
		self.ipsw = ipsw

	def save_blobs(self, save_path, apnonce):
		if apnonce:
			print("Saving temporary SHSH for signing bootchain...")
		else:
			print("Saving temporary SHSH for restoring...")
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
			'--nocache',
		]
		if apnonce:
			args.append('--apnonce')
			args.append(self.device.apnonce)
		tsschecker = subprocess.run(args, stdout=subprocess.PIPE, universal_newlines=True)
		retassure(tsschecker.returncode == 0, "Failed to save SHSH blobs. Exiting.")
		if '/apnonceblobs' in save_path:
			self.apnonce_blob = glob.glob(f"{save_path}/*.shsh*")[0]
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
		sign = subprocess.run(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		retassure(sign.returncode == 0, "Failed to sign bootloader. Exiting.")
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
				self.apnonce_blob,
				'-m',
				output
			]
		save_im4m = subprocess.run(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		retassure(save_im4m.returncode == 0, "Failed to save IM4M. Exiting.")
		self.im4m = output

	def getGeneratorFromSHSH2(self):	# just put here, might be used in the future
		with open(self.blob, 'rb') as f:
			data = plistlib.loads(f.read())
		retassure(data['generator'] is not None, "Failed to read nonce generator from SHSH. Exiting.")
		return data['generator']

	def restore(self, ramdisk, kernelcache, update, custom_blob=None, log_path=None):
		print("Restoring device...")
		if custom_blob:
			args = [
				'futurerestore',
				'-t',
				custom_blob,
				'--skip-blob',
				'--latest-sep',
				'--use-pwndfu',
				'--rdsk',
				ramdisk,
				'--rkrn',
				kernelcache
			]	
		else:	
			args = [
					'futurerestore',
					'-t',
					self.blob,
					'--skip-blob',
					'--latest-sep',
					'--use-pwndfu',
					'--rdsk',
					ramdisk,
					'--rkrn',
					kernelcache
				]
		if self.device.baseband:
			args.append('--latest-baseband')
		else:
			args.append('--no-baseband')
		if update:
			args.append('-u')
		args.append(self.ipsw)
		if log_path:
			if log_path.endswith('/'):
				log_path = log_path[:-1]
			print(os.popen(' '.join(args)).read(), file=open(f'{log_path}/restore.log', 'a'))
			retassure('Done: restoring succeeded!' in open(f'{log_path}/restore.log','r').read(), f'Restore failed! Log saved to {log_path}/restore.log')
			print(f'Restore succeeded! Log saved to {log_path}/restore.log')
		else:
			subprocess.run(args, universal_newlines=True)
