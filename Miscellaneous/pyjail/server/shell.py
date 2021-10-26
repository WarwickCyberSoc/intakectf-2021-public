import code
import string

class FrozenDict(dict):
	def __init__(self, v):
		super().__init__(v)
	def __setitem__(self, k, v):
		# no changey for you
		print("bonked")
		exit(1)

def restrict(buffer_list):
	# no ascii letters for you, muwhaahahha
	for line in buffer_list:
		for char in string.ascii_letters:
			if char in line:
				print("bonked")
				exit(1)
			
	return True

shell = code.InteractiveConsole(filename="superfunchallenge")
locals = {}
shell.runcode=lambda code: restrict(shell.buffer) and exec(code, FrozenDict({"__builtins__": FrozenDict({})}), setattr(shell, "filename", "superfunchallenge"))
shell.interact()