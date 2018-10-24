
def preprocess(file):
	"""
	a generator reads the file, preprocesses it
	yields tuples (character, line_number, column_number)
	the characters has underwent:
		- comments replaced with whitespace
		- inserted some characters like ';', etc
	the line_number and column_number corresponds with the position of 
	the character in the original file
	when there is no more line in the file, yield (None, line_number, column_number)
	"""
	pass #replace "pass" with the implementation



#helper generators down below