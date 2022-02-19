import requests

def get_keys(identifier, board, buildid):
	f = requests.get(f"https://api.m1sta.xyz/wikiproxy/{identifier}/{board}/{buildid}").json()
	for dev in f['keys']:
		if dev['image'] == "iBSS":
			iBSS_iv = dev['iv']
			iBSS_key = dev['key']
		if dev['image'] == "iBEC":
			iBEC_iv = dev['iv']
			iBEC_key = dev['key']
	try:
		return iBSS_iv, iBSS_key, iBEC_iv, iBEC_key
	except UnboundLocalError:
		print("[WARNING] Unable to get firmware keys, either the bootchain is not encrypted or the wikiproxy does not have the firmware keys.")
		input("Continue or not? (Press ENTER to continue, Ctrl-C to quit)")
