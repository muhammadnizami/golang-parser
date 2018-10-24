
def read_symbols(preprocessed_characters):
	"""
	a generator function
	reads terminal symbols for go's EBNF grammar
	yields tuples (symbol, line_number, column_number)
	the line_number and column_number corresponds with the position of 
	the character in the original file
	if there is no more symbols to read, yield (None, line_number, column_number)
	"""
	pass #implement here