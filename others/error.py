import subprocess

def detachret(cond, err, dir):
	if not cond:
		subprocess.run(('hdiutil','detach',dir), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		raise Exception(err)
def retassure(cond, err):
	if not cond:
		raise Exception(err)

def reterror(err):
	raise Exception(err)
