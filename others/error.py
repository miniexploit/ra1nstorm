import subprocess
import os, sys
import inspect

class Ra1nstormException(Exception):
	def __init__(self, err, caller):
		self.err = err
		self.caller = caller

def detachret(cond, err, dir):
	if not (cond):
		caller_frame = inspect.stack()[1]
		caller = os.path.basename(caller_frame.filename)
		subprocess.run(('hdiutil','detach',dir), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		raise Ra1nstormException(err, caller)

def retassure(cond, err):
	if not (cond):
		caller_frame = inspect.stack()[1]
		caller = os.path.basename(caller_frame.filename)
		raise Ra1nstormException(err, caller)

def reterror(err):
	caller_frame = inspect.stack()[1]
	caller = os.path.basename(caller_frame.filename)
	raise Ra1nstormException(err, caller)
