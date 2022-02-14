import sys, os
import subprocess
import glob
import time
from others.error import retassure

class Restore:
	def __init__(self, identifier, ipsw):
		self.identifier = identifier
		self.ipsw = ipsw

	def save_blobs(self, ecid, board, save_path, apnonce=None):
		if apnonce:
			print("Saving temporary SHSH for signing bootchain...")
		else:
			print("Saving temporary SHSH for restoring...")
		args = [
			'tsschecker',
			'-d',
			self.identifier,
			'-B',
			board,
			'-e',
			ecid,
			'-l',
			'-s',
			'--save-path',
			save_path,
			'--nocache'
		]
		if apnonce:
			args.append('--apnonce')
			args.append(apnonce)
		tsschecker = subprocess.run(args, stdout=subprocess.PIPE, universal_newlines=True)
		retassure(tsschecker.returncode == 0, "Failed to save SHSH blobs. Exiting.")
		if '/apnonceblobs' in save_path:
			self.blob = glob.glob(f"{save_path}/*.shsh*")[0]
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
	def save_im4m(self, output):
		print("Saving IM4M for signing bootloaders...")
		args = [
			'img4tool',
			'-e',
			'-s',
			self.blob,
			'-m',
			output
		]
		save_im4m = subprocess.run(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		retassure(save_im4m.returncode == 0, "Failed to save IM4M. Exiting.")
		self.im4m = output
	def restore(self, baseband, ramdisk, kernelcache, update):
		print("Restoring device...")
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
		if baseband:
			args.append('--latest-baseband')
		else:
			args.append('--no-baseband')
		if update:
			args.append('-u')
		args.append(self.ipsw)
		subprocess.run(args, universal_newlines=True)
