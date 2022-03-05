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
		args = (
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
		)
		if apnonce:
			args.append('--apnonce')
			args.append(self.device.apnonce) 
		retassure(subprocess.run(args, stdout=subprocess.PIPE, universal_newlines=True).returncode == 0, "Failed to save SHSH blobs. Exiting.")
		if '/apnonceblobs' in save_path:
			self.apnonce_blob = glob.glob(f"{save_path}/*.shsh*")[0]
		else:
			self.blob = glob.glob(f"{save_path}/*.shsh*")[0]
			
	def sign_bootloader(self, path, output, type):
		print(f"Signing {type}...")
		args = (
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
		)
		retassure(subprocess.run(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0, "Failed to sign bootloader. Exiting.")
		
	def save_im4m(self, output, custom_blob=None):
		print("Saving IM4M for signing bootchain...")
		if custom_blob:
			args = (
				'img4tool',
				'-e',
				'-s',
				custom_blob,
				'-m',
				output
			)
		else:
			args = (
				'img4tool',
				'-e',
				'-s',
				self.apnonce_blob,
				'-m',
				output
			)
		retassure(subprocess.run(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0, "Failed to save IM4M. Exiting.")
		self.im4m = output

	def restore(self, ibss, ibec, ramdisk, kernelcache, update, custom_blob=None, log_path=None):
		print("Restoring device...")
		if custom_blob:
			args = (
				'futurerestore',
				'-t',
				custom_blob,
				'--skip-blob',
				'--latest-sep',
				'--use-pwndfu',
				'-g',
				ibss,
				'-f',
				ibec,
				'--rdsk',
				ramdisk,
				'--rkrn',
				kernelcache
			)	
		else:	
			args = (
					'futurerestore',
					'-t',
					self.blob,
					'--skip-blob',
					'--latest-sep',
					'--use-pwndfu',
					'--ibss-img4',
					ibss,
					'--ibec-img4',
					ibec,
					'--rdsk',
					ramdisk,
					'--rkrn',
					kernelcache
				)
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
			froutput = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf8").stdout
			with open(f'{log_path}/restore.log', 'w') as f:
				f.write(froutput)
			retassure('Done: restoring succeeded!' in froutput, f'Restore failed! Log saved to {log_path}/restore.log')
			print(f'Restore succeeded! Log saved to {log_path}/restore.log')
		else:
			subprocess.run(args, universal_newlines=True)
