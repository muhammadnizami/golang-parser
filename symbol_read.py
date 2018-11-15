import string

keywords = ['break','default','func','interface','select',
	'case','defer','go','map','struct',
	'chan','else','goto','package','switch',
	'const','fallthrough','if','range','type',
	'continue','for','import','return','var'
]

operators = ['+','&','+=','&=','&&','==','!=','(',')',
	'-','|','-=','|=','||','<','<=','[',']',
	'*','^','*=','^=','<-','>','>=','{','}',
	'/','<<','/=','<<=','++','=',':=',',',';',
	'%','>>','%=','>>=','--','!','...','.',':',
	'&^','&^=']

op_chars = set([x for y in operators for x in operators])


def read_symbols(preprocessed_characters):
	"""
	a generator function
	reads terminal symbols for go's EBNF grammar
	yields tuples (symbol, line_number, column_number)
	the line_number and column_number corresponds with the position of 
	the character in the original file
	if there is no more symbols to read, yield (None, line_number, column_number)
	"""
	charbuffer = []

	token_type_candidate = '' #candidates:, 'ki' (keywords or identifier),
								# 'id' (surely identifier), 'op' (operator),
								# '"' (string with \" delim), "'" (string with \' delim) '' (other)

	count_string_backslash = 0
	prev_isspace=False

	for c, l, col in preprocessed_characters:
		if token_type_candidate is 'ki':
			if c in string.ascii_letters:
				charbuffer = charbuffer + [(c,col)]
			else:
				if c not in string.digits+'_' and to_keyword(charbuffer) in keywords:
					yield to_keyword(charbuffer), l, charbuffer[0][1], prev_isspace
					charbuffer = []
				else:
					yield from flush_characters(charbuffer, l, prev_isspace)
					charbuffer = []
				if c.isspace():
					token_type_candidate = ''
					prev_isspace=True
				elif c in string.digits+'_':
					token_type_candidate = 'id'
					yield c, l, col, prev_isspace
				elif c in op_chars:
					token_type_candidate = 'op'
					charbuffer = charbuffer+[(c,col)]
				elif c in ['"',"'"]:
					yield c, l, col, prev_isspace
					token_type_candidate = c
				else:
					token_type_candidate = ''
					yield c, l, col, prev_isspace
		elif token_type_candidate is 'id':
			if c in string.ascii_letters + string.digits+'_':
				yield c, l, col, prev_isspace
			elif c.isspace():
				token_type_candidate=''
			elif c in op_chars:
				token_type_candidate = 'op'
				charbuffer = charbuffer+[(c,col)]
			elif c in ['"',"'"]:
				yield c, l, col, prev_isspace
				token_type_candidate = c
			else:
				token_type_candidate = ''
				yield c, l, col, prev_isspace
		elif token_type_candidate is 'op':
			if c in op_chars:
				charbuffer = charbuffer+[(c,col)]
			else:
				yield from yield_op(charbuffer, l, prev_isspace)
				charbuffer = []
				if c.isspace():
					token_type_candidate = ''
				elif c in string.ascii_letters:
					charbuffer = charbuffer+[(c,col)]
					token_type_candidate = 'ki'
				elif c in '_':
					yield c, l, col, prev_isspace
					token_type_candidate = 'id'
				elif c in ['"',"'"]:
					yield c, l, col, prev_isspace
					token_type_candidate = c
				else:
					yield c, l, col, prev_isspace
					token_type_candidate = ''
		elif token_type_candidate in ['"',","]:
			if c is token_type_candidate:
				if count_string_backslash % 2 == 0:
					token_type_candidate = ''
			if c is '\\':
				count_string_backslash = count_string_backslash + 1
			else:
				count_string_backslash = 0
			yield c, l, col, prev_isspace
		elif token_type_candidate is '':
			if c in string.ascii_letters:
				charbuffer = charbuffer+[(c,col)]
				token_type_candidate = 'ki'
			elif c in op_chars:
				charbuffer = charbuffer+[(c,col)]
				token_type_candidate = 'op'
			elif c is '_':
				yield c, l, col, prev_isspace
			elif c in ['"', ","]:
				yield c, l, col, prev_isspace
				token_type_candidate = c
			elif not c.isspace():
				yield c, l, col, prev_isspace

		if len(charbuffer)==0:
			prev_isspace = c.isspace()

def flush_characters(charbuffer,l,prev_isspace):

	if len(charbuffer)>0:
		c, col = charbuffer.pop(0)
		yield c, l, col, prev_isspace
	for c, col in charbuffer:
		yield c, l, col, False

def to_keyword(charbuffer):
	return ''.join([c for c,col in charbuffer])

def yield_op(charbuffer, l, prev_isspace):
	opchunkstr = to_keyword(charbuffer)
	matched_ops = [x for x in operators if x in opchunkstr]
	longest_op = max(matched_ops, key=lambda s: len(s))
	remainder_strs = opchunkstr.split(longest_op)

	#recursion
	pos = 0
	for i in range(len(remainder_strs)-1):
		if remainder_strs[i] is not '':
			yield from yield_op(charbuffer[pos:pos+len(remainder_strs[i])], l, prev_isspace and pos==0)
			pos = pos + len(remainder_strs[i])
		yield longest_op, l, charbuffer[pos][1], prev_isspace and pos==0
		pos = pos + len(longest_op)
	i = len(remainder_strs)-1
	if remainder_strs[i] is not '':
		yield from yield_op(charbuffer[pos:pos+len(remainder_strs[i])], l, prev_isspace and pos==0)
		pos = pos + len(remainder_strs[i])



if __name__ =='__main__':
	import sys
	import preprocess
	if len(sys.argv) != 2:
		print("to test: symbol_read.py <inputfile>")
		sys.exit()

	with open(sys.argv[1]) as file:
		preprocess_generator = preprocess.preprocess(file)
		symbol_generator = read_symbols(preprocess_generator)
		prev_line_number = 1
		for symbol,line_number,col_number,prev_isspace in symbol_generator:
			for i in range(prev_line_number,line_number):
				print('')
			if prev_isspace:
				print('<space>',end='')
			print(symbol,end='|')
			prev_line_number = line_number