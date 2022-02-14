import plistlib

class Manifest:
	def __init__(self, manifest: bytes):
		self.manifest = plistlib.loads(manifest)
		self.version = tuple(int(_) for _ in self.manifest['ProductVersion'].split('.'))
		self.buildid = self.manifest['ProductBuildVersion']
		self.supported_devices = self.manifest['SupportedProductTypes']
	def get_buildid(self):
		return self.manifest['ProductBuildVersion']
		
	def get_bootchaininfo(self, board):
		for deviceclass in self.manifest['BuildIdentities']:
			if deviceclass['Info']['DeviceClass'] == board:	
				devclass = deviceclass
				break
		return devclass['Manifest']['iBSS']['Info']['Path'], devclass['Manifest']['iBEC']['Info']['Path']
	def get_kernelinfo(self, board):
		for deviceclass in self.manifest['BuildIdentities']:
			if deviceclass['Info']['DeviceClass'] == board:	
				devclass = deviceclass
				break
		return devclass['Manifest']['RestoreKernelCache']['Info']['Path']
