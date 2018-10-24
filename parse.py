import preprocess
import symbol_read
# a procedural program for parsing

#state variables
file = None
symbol = None
line_no = None
column_no = None

#helper
def open_symbolic_file(filename):
	global file
	file = open(filename)
	file = preprocess.preprocess(file)
	file = symbol_read.read_symbols(file)

def read_one_symbol():
	global symbol, line_no, column_no
	symbol, line_no, column_no = next(file)

def output_error_and_halt():
	#implement ouput error here
	print("error")
	print("NOT IMPLEMENTED YET")
	halt()

def main(filename):
	#main program
	open_symbolic_file(filename)
	read_one_symbol()
	#call start symbol
	#output final

#GRAMMAR IMPLEMENTATION HERE
# |  |  |  |
# v  v  v  v

def accept(T):
	global symbol
	if T == symbol:
		read_one_symbool()
	else:
		output_error_and_halt()

#all nonterminal symbols
#format: nt_<symbol_name>


#END OF GRAMMAR IMPLEMENTATION
if __name__ == 'main':
	main(filename)