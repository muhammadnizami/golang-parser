
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

	#states
	line_number = 1
	is_block_comment = False

	is_in_string = False
	for line in file:
		last_nonwhitespace_i = None
		if line[len(line)-1] == '\n':
			last = len(line)-1
		else:
			last = len(line)
		for i in range(last):
			if is_block_comment:
				if i>0 and line[i-1:i+1] == '*/':
					is_block_comment = False
			elif i<len(line)-1 and line[i:i+2] == '/*':
				is_block_comment = True
				yield (' ', line_number, i+1)
			elif i<len(line)-1 and line[i:i+2] == '//':
				yield (' ', line_number, i+1)
				break
			else:
				yield (line[i], line_number, i+1)
				if not line[i].isspace():
					last_nonwhitespace_i = i
				if line[i] is is_in_string:
					count_backslash = 0
					while i-count_backslash-1>0 and line[i-count_backslash-1] is '\\':
						count_backslash = count_backslash + 1
					if count_backslash % 2 == 0:
						is_in_string = False
				elif line[i] in ['"', "'"] and not is_in_string:
					is_in_string = line[i]
		if last_nonwhitespace_i is not None and not is_in_string:
			if line_needs_semicolon(line,last_nonwhitespace_i):
				yield(';',line_number,last_nonwhitespace_i+2)

		yield ('\n',line_number,len(line)-1)
		line_number = line_number + 1

		#check if need to insert ';'


#helper functions
import string
semicolon_indicator_chars = list(string.ascii_letters)+list(string.digits)+[')',']','}','_','"',"'",]

def line_needs_semicolon(line, last_nonwhitespace_i):
	if last_token_is_semicolonless_keyword(line,last_nonwhitespace_i):
		return False
	if line[last_nonwhitespace_i] in semicolon_indicator_chars:
		return True
	if last_nonwhitespace_i > 0:
		if line[last_nonwhitespace_i] is '.' and line[last_nonwhitespace_i-1] in string.digits:
			return True
		if line[last_nonwhitespace_i-1:last_nonwhitespace_i+1] in ['++','--']:
			return True
	return False

def last_token_is_semicolonless_keyword(line, last_nonwhitespace_i):
	keyword_candidate = ''
	i = last_nonwhitespace_i
	while i>=0 and line[i] in string.ascii_letters+string.digits+'_':
		keyword_candidate = line[i] + keyword_candidate
		i = i-1
	return keyword_candidate in semicolonless_keywords

semicolonless_keywords = set(['default','func','interface','select',
	'case','defer','go','map','struct',
	'chan','else','goto','package','switch',
	'const','if','range','type',
	'for','import','var'
	]) #break, continue, fallthrough, and return needs semicolon


if __name__ =='__main__':
	import sys
	if len(sys.argv) != 2:
		print("to test: preprocess.py <inputfile>")
		sys.exit()

	with open(sys.argv[1]) as file:
		preprocess_generator = preprocess(file)
		prev_line_number = 1
		for char,line_number,col_number in preprocess_generator:
			for i in range(prev_line_number+1,line_number):
				print('')
			print(char,end='')
			prev_line_number = line_number