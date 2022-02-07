import requests
import json

def get_ramdiskinfo(identifier, board, buildid):
	f = requests.get(f"https://api.m1sta.xyz/wikiproxy/{identifier}/{board}/{buildid}").json()
	for dev in f['keys']:
		if dev['image'] == "RestoreRamdisk":
			RestoreRamdisk = dev['filename']
		elif dev['image'] == "UpdateRamdisk":
			UpdateRamdisk = dev['filename']
			
	return RestoreRamdisk, UpdateRamdisk
def get_keys(identifier, board, buildid):
	f = requests.get(f"https://api.m1sta.xyz/wikiproxy/{identifier}/{board}/{buildid}").json()
	for dev in f['keys']:
		if dev['image'] == "iBSS":
			iBSS = dev['filename']
			iBSS_iv = dev['iv']
			iBSS_key = dev['key']
		if dev['image'] == "iBEC":
			iBEC = dev['filename']
			iBEC_iv = dev['iv']
			iBEC_key = dev['key']
	return iBSS_iv, iBSS_key, iBEC_iv, iBEC_key
def get_bootchaininfo(identifier, board, buildid):
	f = requests.get(f"https://api.m1sta.xyz/wikiproxy/{identifier}/{board}/{buildid}").json()
	for dev in f['keys']:
		if dev['image'] == "iBSS":
			iBSS = dev['filename']
			iBSS_iv = dev['iv']
			iBSS_key = dev['key']
		if dev['image'] == "iBEC":
			iBEC = dev['filename']
			iBEC_iv = dev['iv']
			iBEC_key = dev['key']
	return iBSS, iBEC