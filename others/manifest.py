import plistlib

class Manifest:
	def __init__(self, manifest: bytes):
		self.manifest = plistlib.loads(manifest)
		self.version = tuple(int(_) for _ in self.manifest['ProductVersion'].split('.'))
		self.buildid = self.manifest['ProductBuildVersion']
		self.supported_devices = self.manifest['SupportedProductTypes']
	def get_buildid(self):
		return self.manifest['ProductBuildVersion']