import sys, os
import subprocess
import glob

class Restore:
	def __init__(self, identifier, ipsw):
		self.identifier = identifier
		self.ipsw = ipsw
	def save_blobs(self, ecid, board, save_path, apnonce=None):
		if apnonce:
			print("Saving SHSH for signing bootchain...")
		else:
			print("Saving temporary SHSH...")
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
		if tsschecker.returncode != 0:
			sys.exit("[ERROR] Failed to save SHSH blobs. Exiting.")
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
		sign = subprocess.run(args, stdout=subprocess.DEVNULL)
		if sign.returncode != 0:
			sys.exit("[ERROR] Failed to sign bootloader. Exiting.")
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
		save_im4m = subprocess.run(args, stdout=subprocess.DEVNULL)
		if save_im4m.returncode != 0:
			sys.exit("[ERROR] Failed to save IM4M. Exiting.")
		self.im4m = output
	def restore(self, baseband, ramdisk, kernelcache, update):
		print("Restoring device...")
		if os.path.exists("restore_error.log"):
			os.remove("restore_error.log")
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
		fr = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
		if 'Done: restoring succeeded!' not in fr.stdout:
			log = open("restore_error.log",'w')
			log.write("futurerestore arguments:\n")
			log.write(f"{' '.join(args)}\n\n")
			log.write("futurerestore log:\n")
			log.write(fr.stdout)
			for line in fr.stdout.splitlines():
				if "what=" in line:
					error = line.replace("what=", "")
			log.close()
			sys.exit(f"[ERROR] Restore failed with reason: '{error}', log saved to 'restore_error.log'. Exiting.")
		print("Successfully restored device! ")
