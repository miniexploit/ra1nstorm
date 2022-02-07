from pathlib import Path
from typing import Optional
import sys, os
import hashlib
import json
import shutil
from zipfile import ZipFile, is_zipfile


class IPSW:
	def __init__(self, ipsw: Path):
		self.ipsw = ipsw
		self.verify_ipsw()
	def __str__(self) -> str:
		return str(self.ipsw)

	def read_file(self, file: str) -> Optional[bytes]:
		try:
			with ZipFile(self.ipsw, 'r') as ipsw:
				return ipsw.read(file)
		except KeyError:
			sys.exit(f"[ERROR] File not in IPSW: {file}")
	def extract_file(self, file, location):
		try:
			print(f"Extracting '{file}'...")
			with ZipFile(self.ipsw, 'r') as ipsw, open(location, 'wb') as f:
				f.write(ipsw.read(file))
		except:
			sys.exit(f"[ERROR] Couldn't extract {file}")
	def verify_ipsw(self):
		if not os.path.exists(self.ipsw):
			sys.exit(f"[ERROR] iPSW not found at: {self.ipsw}")
		if not is_zipfile(self.ipsw):
			sys.exit(f"[ERROR] '{self.ipsw}' is not a valid iPSW")
	def get_ipswinfo(self, buildmanifest):
		ios_ver = ""
		for ver in buildmanifest.version:
			ios_ver += f"{ver}."
		ios_ver = ios_ver[:-1]
		print(f"iPSW info: Version: {ios_ver} BuildID: {buildmanifest.get_buildid()}")
		if not buildmanifest.version[0] >= 11 or not buildmanifest.version[0] <= 14:
			sys.exit(f"[ERROR] iOS {buildmanifest.version[0]}.{buildmanifest.version[1]} is not supported. Exiting.")
