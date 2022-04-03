from pathlib import Path
from typing import Optional
import sys, os
import hashlib
import json
import shutil
import plistlib
import os, sys
from others.error import retassure, reterror
from zipfile import ZipFile, is_zipfile


class IPSW:
	def __init__(self, ipsw: Path):
		self.ipsw = ipsw
		self.otaable = False
		self.verify_ipsw()

	def __str__(self) -> str:
		return str(self.ipsw)

	def read_file(self, file: str) -> Optional[bytes]:
		try:
			with ZipFile(self.ipsw, 'r') as ipsw:
				return ipsw.read(file)
		except KeyError:
			reterror(f"File not in IPSW: {file}")
	def extract_file(self, file, location):
		try:
			print(f"Extracting '{file}'...")
			with ZipFile(self.ipsw, 'r') as ipsw, open(location, 'wb') as f:
				f.write(ipsw.read(file))
		except:
			reterror(f"Couldn't extract {file}")

	def verify_ipsw(self):
		print("Verifying iPSW...")
		retassure(os.path.exists(self.ipsw), f"iPSW not found at: {self.ipsw}")
		retassure(is_zipfile(self.ipsw), f"'{self.ipsw}' is not a valid iPSW")

	def get_ipswinfo(self, buildmanifest):
		ios_ver = ""
		for ver in buildmanifest.version:
			ios_ver += f"{ver}."
		self.version = ios_ver[:-1]
		print(f"iPSW info: Version: {self.version} BuildID: {buildmanifest.buildid}")
		self.int_version = buildmanifest.version[0]
		retassure(10 <= buildmanifest.version[0] <= 14, f"iOS {self.version} is not supported")
		if self.version == "10.3.3":
			self.otaable = True
