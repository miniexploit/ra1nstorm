import sys

def retassure(cond, err):
	if not cond:
		sys.exit(f"[ERROR] {err}")

def reterror(err):
	sys.exit(f"[ERROR] {err}")