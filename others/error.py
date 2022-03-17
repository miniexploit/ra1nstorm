import subprocess

class Ra1nstormException(Exception):
	pass

def detachret(cond, err, dir):
	if not cond:
		subprocess.run(('hdiutil','detach',dir), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		raise Ra1nstormException(err)

def retassure(cond, err):
	if not cond:
		raise Ra1nstormException(err)

def reterror(err):
	raise Ra1nstormException(err)
