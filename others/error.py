def retassure(cond, err):
	if not cond:
		raise Exception(err)

def reterror(err):
	raise Exception(err)
