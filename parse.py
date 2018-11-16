import preprocess
import symbol_read
import string
from termcolor import colored
# a procedural program for parsing

#state variables
file = None
symbol = None
line_no = None
column_no = None
prev_isspace = False

#helper
def open_symbolic_file(filename):
	global file
	file = open(filename)
	file = preprocess.preprocess(file)
	file = symbol_read.read_symbols(file)

def read_one_symbol():
	global symbol, line_no, column_no, prev_isspace
	symbol, line_no, column_no, prev_isspace = next(file)

def output_error_and_halt():
	#implement ouput error here
	print("error")
	print("symbol", symbol, "line_no", line_no, "column_no", column_no)
	raise SystemExit

def main(filename):
	try:
		#main program
		open_symbolic_file(filename)
		read_one_symbol()
		#call start symbol
		nt_SourceFile()

		#output if no error
		with open(filename) as file:
			for line in file:
				print(line,end='')

		print("no error was found. file syntax is valid")
	except SystemExit as e:
		print("specifically in the file please see below")
		print("=========================================")
		if line_no!="last":
			#output final error
			with open(filename) as file:
				l=1
				for line in file:
					c_no=1
					for c in line:
						if l==line_no and c_no == column_no:
							print(colored(c,'red'),end='')
						elif (l==line_no and c_no > column_no) or (l>line_no):
							print(colored(c,'grey'),end='')
						else:
							print(c,end='')
						c_no=c_no+1
					l=l+1
			print('\033[0m')
		print("=========================================")
		print("error! see above")

#GRAMMAR IMPLEMENTATION HERE
# |  |  |  |
# v  v  v  v
def accept(T):
	global symbol
	if T == symbol:
		read_one_symbol()
	else:
		output_error_and_halt()

def acceptset(Ts):
	global symbol
	if symbol in Ts:
		read_one_symbol()
	else:
		output_error_and_halt()

def acceptsemicolon():
	#this is to abide to the specification's semicolon ignorance rule no. 2:
	#	To allow complex statements to occupy a single line, a semicolon may be omitted before a closing ")" or "}".
	global symbol
	if symbol==";":
		read_one_symbol()
	elif symbol!="}":
		output_error_and_halt()



#all nonterminal symbols
#format: nt_<symbol_name>

# <newline> ::= /* the Unicode code point U+000A */ 
def nt_newline():
	accept('\n')

# <unicode_char> ::= /* an arbitrary Unicode code point except newline */ 
def nt_unicode_char():
	accept(symbol)

# <unicode_letter> ::= /* a Unicode code point classified as "Letter" */
def nt_unicode_letter():
	if symbol in set(string.ascii_letters):
		accept(symbol)

# <unicode_digit> ::= /* a Unicode code point classified as "Number, decimal digit" */ 
def nt_unicode_digit():
	if symbol in set(string.digits):
		accept(symbol)

# <letter> ::= unicode_letter | "_"
def nt_letter(): 
	if symbol == "_":
		accept("_")
	elif symbol in set(string.ascii_letters):
		accept(symbol)
	else:
		output_error_and_halt()
	
# <decimal_digit> ::= "0" … "9"
def nt_decimal_digit():
	if symbol in set(string.digits):
		accept(symbol)

# <octal_digit> ::= "0" … "7"
def nt_octal_digit():
	if symbol in set(string.digits):
		accept(symbol)

# <hex_digit> ::= "0" … "9" | "A" … "F" | "a" … "f"
def nt_hex_digit():
	if symbol in set(string.digits):
		accept(symbol)
	elif symbol in set({"A","B","C","D","E","F","a","b","c","d","e","f"}):
		accept(symbol)

import traceback
# <identifier> ::= letter { letter | unicode_digit }
def nt_identifier():
	nt_letter()
	while symbol in set(string.ascii_letters+string.digits+"_") and not prev_isspace:
		if symbol in set(string.ascii_letters+"_"):
			nt_letter()
		elif symbol in set(string.digits):
			nt_unicode_digit()

# <int_lit> ::= decimal_lit | octal_lit | hex_lit
def nt_int_lit():
	if symbol in set(string.digits):
		nt_decimal_lit()
	if symbol in set(string.octdigits):
		nt_octal_lit()
	if symbol in set(string.hexdigits):
		nt_hex_lit()

# <decimal_lit> ::= ( "1" … "9" ) { decimal_digit }
def nt_decimal_lit():
	if symbol == '1':
		accept('1')
	elif symbol == '2':
		accept('2')
	elif symbol == '3':
		accept('3')
	elif symbol == '4':
		accept('4')
	elif symbol == '5':
		accept('5')
	elif symbol == '6':
		accept('6')
	elif symbol == '7':
		accept('7')
	elif symbol == '8':
		accept('8')
	elif symbol == '9':
		accept('9')
	else:
		output_error_and_halt()

	while symbol in set(string.digits):
		nt_decimal_digit()
	
# <octal_lit> ::= "0" { octal_digit }
def nt_octal_lit():
	accept("0")
	while symbol in set(string.octdigits):
		nt_octal_digit()

# <hex_lit> ::= "0" ( "x" | "X" ) hex_digit { hex_digit }
def nt_hex_lit():
	accept("0")
	if symbol == "x":
		accept("x")
	elif symbol == "X":
		accept("X")
	else:
		output_error_and_halt()
	nt_hex_digit()
	while symbol in set(string.hexdigits):
		nt_hex_digit()

# <float_lit> ::= decimals "." [ decimals ] [ exponent ] | decimals exponent | "." decimals [ exponent ]
def nt_float_lit():
	if symbol == ".":
		accept(".")
		nt_decimals()
		if symbol in set({"e","E"}):
			nt_exponent()
	else:
		nt_decimals()
		accept(".")
		if symbol in set(string.digits):
			nt_decimals()
		if symbol in set({"e","E"}):
			nt_exponent()
	
# <decimals> ::= decimal_digit { decimal_digit }
def nt_decimals():
	nt_decimal_digit()
	while symbol in set(string.digits):
		nt_decimal_digit()

# <exponent> ::= ( "e" | "E" ) [ "+" | "-" ] decimals
def nt_exponent():
	if symbol == "e":
		accept("e")
	elif symbol == "E":
		accept("E")
	else:
		output_error_and_halt()

	if symbol == "+":
		accept("+")
	elif symbol == "-":
		accept("-")

	nt_decimals()

# <imaginary_lit> ::= (decimals | float_lit) "i"
def nt_imaginary_lit():
	if symbol in set(string.digits):
		nt_decimals()
	elif symbol == ".":
		float_lit()
	accept("i")

# <rune_lit> ::= " ' " ( unicode_value | byte_value ) " ' "
def nt_rune_lit():
	accept("'")
	if symbol in set(string.unicode_value):
		nt_unicode_value()
	elif symbol in set(string.hexdigits).union(string.octdigits):
		nt_byte_value()
	else:
		output_error_and_halt()
	accept("'")

# <unicode_value> ::= unicode_char | little_u_value | big_u_value | escaped_char
def nt_unicode_value():
	if symbol != "\\":
		nt_unicode_char()
	else:
		accept("\\")
		if symbol == "u":
			nt_little_u_value()
		elif symbol == "U":
			nt_big_u_value()
		else:
			nt_escaped_char()

# <byte_value> ::= octal_byte_value | hex_byte_value
def nt_byte_value():
	if symbol == "x":
		nt_hex_byte_value()
	else:
		nt_octal_byte_value()
		
# <octal_byte_value> ::= `\` octal_digit octal_digit octal_digit
def nt_octal_byte_value():
	nt_octal_digit()
	nt_octal_digit()
	nt_octal_digit()
	
# <hex_byte_value> ::= `\` "x" hex_digit hex_digit
def nt_hex_byte_value():
	accept("x")
	nt_hex_digit()
	nt_hex_digit()


# <little_u_value> ::= `\` "u" hex_digit hex_digit hex_digit hex_digit
def nt_little_u_value():
	# accept('\\')
	accept("u")
	nt_hex_digit()
	nt_hex_digit()
	nt_hex_digit()
	nt_hex_digit()
	
# <big_u_value> ::= `\` "U" hex_digit hex_digit hex_digit hex_digit hex_digit hex_digit hex_digit hex_digit
def nt_big_u_value():
	# accept('\\')
	accept("U")
	nt_hex_digit()
	nt_hex_digit()
	nt_hex_digit()
	nt_hex_digit()
	nt_hex_digit()
	nt_hex_digit()
	nt_hex_digit()
	nt_hex_digit()
	

# <escaped_char> ::= `\` ( "a" | "b" | "f" | "n" | "r" | "t" | "v" | `\` | "'" | `"` )
def nt_escaped_char():
	# accept('\\')
	if symbol == "a":
		accept("a")
	elif symbol == "b":
		accept("b")
	elif symbol == "f":
		accept("f")
	elif symbol == "n":
		accept("n")
	elif symbol == "r":
		accept("r")
	elif symbol == "t":
		accept("t")
	elif symbol == "v":
		accept("v")
	elif symbol == "\\":
		accept("\\")
	elif symbol == "'":
		accept("'")
	elif symbol == '"':
		accept('"')
	
# <string_lit> ::= raw_string_lit | interpreted_string_lit
def nt_string_lit():
	if symbol == "'":
		nt_raw_string_lit()
	elif symbol == '"':
		nt_interpreted_string_lit()
# <raw_string_lit> ::= "`" { unicode_char | newline } "`"
def nt_raw_string_lit():
	accept("'")
	while symbol in set(string.ascii_letters).union({"\n"}):
		if symbol == "\n":
			nt_newline()
		else:
			nt_unicode_char()
	accept('"')
	accept("'")

# <interpreted_string_lit> ::= `"` { unicode_value | byte_value } `"`
#	THIS IS NOT LL(1)
#	change to: <interpreted_string_lit> ::= `"` { unicode_or_byte_value } `"`
def nt_interpreted_string_lit():
	accept('"')
	while symbol != '"':
		nt_unicode_or_byte_value()
	accept('"')

# added a new rule:
#	<unicode_or_byte_value> ::= unicode_char | "\\" ( little_u_value | big_u_value | escaped_char | byte_value )
def nt_unicode_or_byte_value():
	if symbol!="\\":
		nt_unicode_char()
	else:
		accept("\\")
		if symbol=="u":
			nt_little_u_value()
		elif symbol=="U":
			nt_big_u_value()
		elif symbol in {"a", "b", "f", "n", "r","t", "v", "\\", "'", '"' }:
			nt_escaped_char()
		else:
			nt_byte_value()

# <Type> ::= TypeName | TypeLit | "(" Type ")"
def nt_Type():
	if symbol == "(":
		accept("(")
		nt_Type()
		accept(")")
	elif symbol in set({"[","struct","*","func","interface","map","chan","<-"}):
		nt_TypeLit()
	elif symbol in set(string.ascii_letters).union({"_"}):
		nt_TypeName()

# <TypeName> ::= identifier | QualifiedIdent
def nt_TypeName():
	if symbol in set(string.ascii_letters).union({"_"}):
		nt_identifier()
	elif symbol in set(string.ascii_letters).union({"_"}):
		nt_QualifiedIdent()

# <TypeLit> ::= ArrayType | StructType | PointerType | FunctionType | InterfaceType | SliceType | MapType | ChannelType
def nt_TypeLit():
	if symbol == "[":
		nt_ArrayType()
	elif symbol == "struct":
		nt_StructType()
	elif symbol == "*":
		nt_PointerType()
	elif symbol == "func":
		nt_FunctionType()
	elif symbol == "interface":
		nt_InterfaceType()
	elif symbol == "[]":
		nt_SliceType()
	elif symbol == "map":
		nt_MapType()
	else:
		nt_ChannelType()

# <ArrayType> ::= "[" ArrayLength "]" ElementType
def nt_ArrayType():
	accept("[")
	nt_ArrayLength()
	accept("]")
	nt_ElementType()

# <ArrayLength> ::= Expression
def nt_ArrayLength():
	nt_Expression()

# <ElementType> ::= Type
def nt_ElementType():
	nt_Type()

# <SliceType> ::= "[" "]" ElementType
def nt_SliceType():
	accept("[]")
	nt_ElementType()

# <StructType> ::= "struct" "{" { FieldDecl ";" } "}"
def nt_StructType():
	accept("struct")
	accept("{")
	while symbol in set(string.ascii_letters).union({"_"}):
		nt_FieldDecl()
		acceptsemicolon()
	accept("}")

# <FieldDecl> ::= (IdentifierList Type | EmbeddedField) [ Tag ]
def nt_FieldDecl():
	if symbol in set(string.ascii_letters).union({"_"}):
		nt_IdentifierList()
		nt_Type()
	elif symbol in set(string.ascii_letters).union({"_","*"}):
		nt_EmbeddedField()
	else:
		output_error_and_halt()
	
	if symbol in set(string.ascii_letters):
		nt_Tag()

# <EmbeddedField> ::= [ "*" ] TypeName
def nt_EmbeddedField():
	if symbol == "*":
		accept("*")
	nt_TypeName()

# <Tag> ::= string_lit
def nt_Tag():
	nt_string_lit()

# <PointerType> ::= "*" BaseType
def nt_PointerType():
	accept("*")
	nt_BaseType()

# <BaseType> ::= Type
def nt_BaseType():
	nt_Type()

# <FunctionType> ::= "func" Signature
def nt_FunctionType():
	accept("func")
	nt_Signature()

# <Signature> ::= Parameters [ Result ]
def nt_Signature():
	nt_Parameters()
	if symbol in set(string.ascii_letters).union({"(","_"}):
		nt_Result()

# <Result> ::= Parameters | Type
def nt_Result():
	if symbol == "(":
		nt_Parameters()
	elif symbol in set(string.ascii_letters).union({"(","_"}):
		nt_Type()

# <Parameters> ::= "(" [ ParameterList [ "," ] ] ")"
def nt_Parameters():
	accept("(")
	if symbol in set(string.ascii_letters).union({"(","_"}):
		nt_ParameterList()
		if symbol == ",":
			accept(",")
	accept(")")

# <ParameterList> ::= ParameterDecl { "," ParameterDecl }
def nt_ParameterList():
	nt_ParameterDecl()
	while symbol == ",":
		accept(",")
		nt_ParameterDecl()

# <ParameterDecl> ::= [ IdentifierList ] [ "..." ] Type
def nt_ParameterDecl():
	if symbol in set(string.ascii_letters).union({"_"}):
		nt_IdentifierList()
	if symbol == "...":
		accept("...")
	nt_Type()

# <InterfaceType> ::= "interface" "{" { MethodSpec ";" } "}"
def nt_InterfaceType():
	accept("interface")
	accept("{")
	while symbol in set(string.ascii_letters).union({"_"}):
		nt_MethodSpec()
		acceptsemicolon()
	accept("}")

# <MethodSpec> ::= MethodName Signature | InterfaceTypeName
def nt_MethodSpec():
	if symbol in set(string.ascii_letters).union({"_"}):
		nt_MethodName()
		nt_Signature()
	elif symbol in set(string.ascii_letters).union({"_"}):
		nt_InterfaceTypeName()

# <MethodName> ::= identifier
def nt_MethodName():
	nt_identifier()

# <InterfaceTypeName> ::= TypeName
def nt_InterfaceType():
	nt_TypeName()

# <MapType> ::= "map" "[" KeyType "]" ElementType
def nt_MapType():
	accept("map")
	accept("[")
	nt_KeyType()
	accept("]")
	nt_ElementType()

# <KeyType> ::= Type
def nt_KeyType():
	nt_Type()

# <ChannelType> ::= ( "chan" | "chan" "<-" | "<-" "chan" ) ElementType
def nt_ChannelType():
	if symbol == "chan":
		accept("chan")
		if symbol == "<-":
			accept("<-")
	elif symbol == "<-":
		accept("<-")
		accept("chan")
	else:
		output_error_and_halt()
	nt_ElementType()

# <Block> ::= "{" StatementList "}"
def nt_Block():
	accept("{")
	nt_StatementList()
	accept("}")

# <StatementList> ::= { Statement ";" }
def nt_StatementList():
	while symbol in set(string.ascii_letters+'.').union({"_"}).union({"const", "type", "var","go","return","break","continue","goto","fallthrough","{","if","switch","select","for","defer"}).union(nt_unary_op_set).union(nt_literal_first_set):
		nt_Statement()
		acceptsemicolon()

# <Declaration> ::= ConstDecl | TypeDecl | VarDecl
def nt_Declaration():
	if symbol == "const":
		nt_ConstDecl()
	elif symbol == "type":
		nt_TypeDecl()
	elif symbol == "var":
		nt_VarDecl()
	else:
		output_error_and_halt()

# <TopLevelDecl> ::= Declaration | FunctionDecl | MethodDecl
# change to:
#	<TopLevelDecl> ::= Declaration | "func" ( MethodDecl | FunctionDecl )
#	MethodDecl and FunctionDecl is also changed
def nt_TopLevelDecl():
	if symbol in set({"const", "type", "var"}):
		nt_Declaration()
	elif symbol == "func":
		accept("func")
		if symbol == "(":
			nt_MethodDecl()
		elif symbol in set(string.ascii_letters).union({"_","("}):
			nt_FunctionDecl()

# <ConstDecl> ::= "const" ( ConstSpec | "(" { ConstSpec ";" } ")" )
def nt_ConstDecl():
	accept("const")
	if symbol in set(string.ascii_letters).union({"_","("}):
		if symbol == "(":
			accept("(")
			nt_ConstSpec()
			acceptsemicolon()
			accept(")")
		else:
			nt_ConstSpec()

# <ConstSpec> ::= IdentifierList [ [ Type ] "::=" ExpressionList ]
def nt_ConstSpec():
	nt_IdentifierList()
	if symbol in set(string.ascii_letters):
		if symbol in set(string.ascii_letters):
			nt_Type()
		accept("::=")
		nt_ExpressionList()
	
# <IdentifierList> ::= identifier { "," identifier }
def nt_IdentifierList():
	nt_identifier()
	while symbol == ",":
		accept(",")
		nt_identifier

# <ExpressionList> ::= Expression { "," Expression }
def nt_ExpressionList():
	nt_Expression()
	while symbol == ",":
		accept(",")
		nt_Expression()
		
# <TypeDecl> ::= "type" ( TypeSpec | "(" { TypeSpec ";" } ")" )
def nt_TypeDecl():
	accept("type")
	if symbol in set(string.ascii_letters).union({"_"}):
		nt_TypeSpec()
	elif symbol == "(":
		accept("(")
		while symbol in set(string.ascii_letters).union({"_"}):
			nt_TypeSpec()
			acceptsemicolon()
		accept(")")
	else:
		output_error_and_halt()

# <TypeSpec> ::= AliasDecl | TypeDef
# change to:
#	<TypeSpec> ::= identifier [ "=" ] Type
def nt_TypeSpec():
	nt_identifier()
	if symbol== "=":
		accept("=")
	nt_Type()
	
# <AliasDecl> ::= identifier "=" Type
def nt_AliasDecl():
	nt_identifier()
	accept("=")
	nt_Type()

# <TypeDef> ::= identifier Type
def nt_TypeDef():
	nt_identifier()
	nt_Type()

# <VarDecl> ::= "var" ( VarSpec | "(" { VarSpec ";" } ")" )
def nt_VarDecl():
	accept("var")
	if symbol == "(":
		accept("(")
		while symbol in set(string.ascii_letters).union({"_"}):
			nt_VarSpec()
			acceptsemicolon()
		accept(")")
	elif symbol in set(string.ascii_letters).union({"_"}):
		nt_VarSpec()
	else:
		output_error_and_halt()

# <VarSpec> ::= IdentifierList ( Type [ "=" ExpressionList ] | "=" ExpressionList )
def nt_VarSpec():
	nt_IdentifierList()
	if symbol == "=":
		accept("=")
		nt_ExpressionList()
	elif symbol in set(string.ascii_letters).union({"_","(","[","struct","*","func","interface","map","chan","<-"}):
		nt_Type()
		if symbol == "=":
			accept("=")
			nt_ExpressionList()
	else:
		output_error_and_halt()

# <ShortVarDecl> ::= IdentifierList ":=" ExpressionList
def nt_ShortVarDecl():
	nt_IdentifierList()
	accept(":=")
	nt_ExpressionList()

# <FunctionDecl> ::= "func" FunctionName Signature [ FunctionBody ]
# change to: <FunctionDecl> ::= "func" FunctionName Signature [ FunctionBody ]
def nt_FunctionDecl():
	nt_FunctionName()
	nt_Signature()
	if symbol == "{":
		nt_FunctionBody()

# <FunctionName> ::= identifier
def nt_FunctionName():
	nt_identifier()

# <FunctionBody> ::= Block
def nt_FunctionBody():
	nt_Block()

# <MethodDecl> ::= "func" Receiver MethodName Signature [ FunctionBody ]
# change to: <MethodDecl> ::= Receiver MethodName Signature [ FunctionBody ]
def nt_MethodDecl():
	nt_Receiver()
	nt_MethodName()
	nt_Signature()
	if symbol == "{":
		nt_FunctionBody()

# <Receiver> ::= Parameters
def nt_Receiver():
	nt_Parameters()

# <Operand> ::= Literal | OperandName | "(" Expression ")"
def Operand():
	if symbol in set(string.ascii_letters+"_"):
		nt_OperandName()
	elif symbol == "(":
		accept("(")
		nt_Expression()
		accept(")")
	else:
		nt_Literal()

nt_literal_first_set = set(string.digits+".'`"+'"').union({"struct","[","map","func"})
# <Literal> ::= BasicLit | CompositeLit | FunctionLit
def nt_Literal():
	if symbol in set(string.digits+".'`"+'"'):
		nt_BasicLit()
	elif symbol in {"struct","[","map"}.union(set(string.ascii_letters+'_')):
		nt_CompositeLit()
	elif symbol == "func":
		nt_FunctionLit()
	else:
		output_error_and_halt()
# <BasicLit> ::= int_lit | float_lit | imaginary_lit | rune_lit | string_lit
# change to: <BasicLit> ::= numeric_lit | rune_lit | string_lit
def nt_BasicLit():
	if symbol in set(string.digits+"."):
		nt_numeric_lit()
	elif symbol=="'":
		nt_rune_lit()
	elif symbol in set('"`'):
		nt_string_lit()
	else:
		output_error_and_halt()
#	added rule: <numeric_lit> ::= 	decimal_lit [ "." [ decimals ] ] [ exponent ] |
#									"0" ( ( "x" | "X" ) hex_digit { hex_digit } |
#										{ decimal_digit } [ "." [ decimals ] ] [ exponent ] |
#									"." decimals [ exponent ]
#				(we assume that octal_digit is included in decimal_digit, although it might output "malformed integer")
def nt_numeric_lit():
	if symbol in set("123456789"):
		nt_decimal_lit()
		if symbol==".":
			accept(".")
			if symbol in set(string.digits):
				nt_decimals()
		if symbol in {"e","E"}:
			nt_exponent()
	elif symbol=="0":
		accept("0")
		if symbol in {"x","X"}:
			acceptset({"x","X"})
			nt_hex_digit()
			while symbol in set(string.hexdigits):
				nt_hex_digit()
		elif symbol in set(string.digits+".eE"):
			while symbol in set(string.digits):
				nt_decimal_digit()
			if symbol==".":
				accept(".")
				if symbol in set(string.digits):
					nt_decimals()
			if symbol in {"e","E"}:
				nt_exponent()
	elif symbol==".":
		accept(".")
		nt_decimals()
		if symbol in {"e","E"}:
			nt_exponent()	
	else:
		output_error_and_halt()
	if symbol=="i":
		accept("i")
# <OperandName> ::= identifier | QualifiedIdent.
# NOT LL(1)
# change to: <OperandName> ::= identifier [ "." identifier] 
def nt_OperandName():
	nt_identifier()
	if symbol==".":
		accept(".")
		nt_identifier()

# <QualifiedIdent> ::= PackageName "." identifier
def nt_QualifiedIdent():
	nt_PackageName()
	accept(".")
	nt_identifier()

# <CompositeLit> ::= LiteralType LiteralValue
def nt_CompositeLit():
	nt_LiteralType()
	nt_LiteralValue()

# <LiteralType> ::= StructType | ArrayType | "[" "..." "]" ElementType | SliceType | MapType | TypeName
def nt_LiteralType():
	if symbol=="struct":
		nt_StructType()
	elif symbol=="[": #ArrayType or "[" "..." "]" ElementType or SliceType
		accept("[")
		if symbol=="...":
			accept("...")
			nt_ElementType()
		elif symbol=="]":
			accept("]")
			nt_ElementType()
		else:
			accept("[")
			nt_ArrayLength()
			accept("]")
			nt_ElementType()
	elif symbol=="map":
		nt_MapType()
	elif symbol in set(string.ascii_letters+'_'):
		nt_TypeName()

# <LiteralValue> ::= "{" [ ElementList [ "," ] ] "}"
# <ElementList> ::= KeyedElement { "," KeyedElement }
#	this one is implementation for both LiteralValue and ElementList
#		<LiteralValue> ::= "{" [ KeyedElement { "," KeyedElement } "," ] "}"
def nt_LiteralValue():
	accept("{")
	if symbol != "}":
		nt_KeyedElement()
		while symbol ==",":
			accept(",")
			if symbol != "}":
				nt_KeyedElement()
	accept("}")

# <KeyedElement> ::= [ Key ":" ] Element
#	Key and element is the same, so:
def nt_KeyedElement():
	nt_Element() #also works with key
	if symbol==":":
		accept(":")
		nt_Element()

# <Key> ::= FieldName | Expression | LiteralValue
# not LL(1)
# FieldName is also covered in Expression, so:
def nt_Key():
	if symbol != "{":
		nt_Expression()
	else:
		nt_LiteralValue()

# <FieldName> ::= identifier
def nt_FieldName():
	nt_identifier()

# <Element> ::= Expression | LiteralValue
def nt_Element():
	if symbol!="{":
		nt_Expression()
	else:
		nt_LiteralValue()

# <FunctionLit> ::= "func" Signature FunctionBody
def nt_FunctionLit():
	accept("func")
	nt_Signature()
	nt_FunctionBody()

# <PrimaryExpr> ::= Operand | Conversion | MethodExpr | PrimaryExpr Selector | PrimaryExpr Index | PrimaryExpr Slice | PrimaryExpr TypeAssertion | PrimaryExpr Arguments
#	FOLLOW(Selector) contains "." which is in FIRST(Selector)
#	<PrimaryExpr> ::= ( identifier | Literal | "(" Expression ")" ) { SelectorOrTypeAssertion | IndexOrSlice }
def nt_PrimaryExprFront():
	if symbol in set(string.ascii_letters + "_"):
		nt_identifier()
	elif symbol=="(":
		count_openparentheses = 0
		while symbol=="(":
			accept("(")
			count_openparentheses += 1

		if symbol in {"[","struct","*","func","interface","map","chan"}: #obviously Type, then conversion
			isConversion=True
			nt_Type()
		elif symbol=="<-": #might be ChannelType, might be not
			accept("<-")
			if symbol=="chan":
				accept("chan")
				nt_ElementType()
				isConversion = True
			else:
				isConversion = False
				nt_Expression()
		else:
			isConversion = False
			nt_Expression()

		while count_openparentheses > 0:
			accept(")")
			count_openparentheses -= 1

		if isConversion: # "(" Expression [ "," ] ")"
			accept("(")
			nt_Expression()
			if symbol==",":
				accept(",")
			accept(")")

	else:
		nt_Literal()
def nt_PrimaryExpr():
	nt_PrimaryExprFront()
	while symbol in {".", "[", "("}:
		if symbol==".":
			nt_SelectorOrTypeAssertion()
		elif symbol=="[":
			nt_IndexOrSlice()
		else: #symbol=="("
			# Arguments, also includes conversion
			nt_Arguments()
# also FOLLOW(TypeAssertion) is the same
# <Selector> ::= "." identifier
# <Index> ::= "[" Expression "]"
# <Slice> ::= "[" [ Expression ] ":" [ Expression ] "]" | "[" [ Expression ] ":" Expression ":" Expression "]"
# <TypeAssertion> ::= "." "(" Type ")"
def nt_SelectorOrTypeAssertion():
	accept(".")
	if symbol=="(":
		accept("(")
		nt_Type()
		accept(")")
	else:
		nt_identifier()
def nt_IndexOrSlice():
	accept("[")
	if symbol != ":":
		nt_Expression()
	if symbol=="]":
		accept("]")
	else:
		accept(":")
		if symbol !="]":
			nt_Expression()
		if symbol == "]":
			accept("]")
		else:
			accept(":")
			nt_Expression()
			accept("]")

# <Arguments> ::= "(" [ ( ExpressionList | Type [ "," ExpressionList ] ) [ "..." ] [ "," ] ] ")"
def nt_Arguments():
	accept("(")
	if symbol != ")":
		count_openparentheses=0
		while symbol=="(": #possible Type
			accept("(")
			count_openparentheses+=1
		if symbol in set({"[","struct","*","func","interface","map","chan"}): #definitely Type
			nt_Type()
			while count_openparentheses>0:
				accept(")")
				count_openparentheses-=1
		elif symbol=="<-": #might be ChannelType, might be not
			accept("<-")
			if symbol=="chan":
				accept("chan")
				nt_ElementType()
				while count_openparentheses>0:
					accept(")")
					count_openparentheses-=1
			else:
				nt_Expression() #TypeName is included
				while count_openparentheses>0:
					accept(")")
					count_openparentheses-=1
					#remember:
					#	<PrimaryExpr> ::= Operand | Conversion | MethodExpr | PrimaryExpr Selector | PrimaryExpr Index | PrimaryExpr Slice | PrimaryExpr TypeAssertion | PrimaryExpr Arguments
					while symbol in {".", "[", "("}:
							if symbol==".":
								nt_SelectorOrTypeAssertion()
							elif symbol=="[":
								nt_IndexOrSlice()
							else: #symbol=="("
								# Arguments, also includes conversion
								nt_Arguments()
					#	<Expression> ::= UnaryExpr | Expression binary_op Expression
					if symbol != ")":
						nt_binary_op()
						nt_Expression()
		else:
			nt_Expression() #TypeName is included
			while count_openparentheses>0:
				accept(")")
				count_openparentheses-=1
				#remember:
				#	<PrimaryExpr> ::= Operand | Conversion | MethodExpr | PrimaryExpr Selector | PrimaryExpr Index | PrimaryExpr Slice | PrimaryExpr TypeAssertion | PrimaryExpr Arguments
				while symbol in {".", "[", "("}:
						if symbol==".":
							nt_SelectorOrTypeAssertion()
						elif symbol=="[":
							nt_IndexOrSlice()
						else: #symbol=="("
							# Arguments, also includes conversion
							nt_Arguments()
				#	<Expression> ::= UnaryExpr | Expression binary_op Expression
				if symbol != ")":
					nt_binary_op()
					nt_Expression()

		while symbol==",":
			# cannot use ExpressionList because of possible final ","
			accept(",")
			if symbol != ")":
				nt_Expression()
		if symbol=="...":
			accept("...")
		if symbol==",":
			accept(",")
	accept(")")

# <MethodExpr> ::= ReceiverType "." MethodName
def nt_MethodExpr():
	nt_ReceiverType()
	accept(".")
	nt_MethodName()

# <ReceiverType> ::= Type
def nt_ReceiverType():
	nt_Type()

# <Expression> ::= UnaryExpr | Expression binary_op Expression
#	NOT LL(1)
#	convert to: UnaryExpr { binary_op UnaryExpr }
#	FOLLOW(Expression): ,;]):
def nt_Expression():
	nt_UnaryExpr()
	while symbol not in {",",";","}","]",")",":","{"}:
		nt_binary_op()
		nt_UnaryExpr()

# <UnaryExpr> ::= PrimaryExpr | unary_op UnaryExpr
def nt_UnaryExpr():
	if symbol in nt_unary_op_set:
		nt_unary_op()
	nt_PrimaryExpr()

# <binary_op> ::= "||" | "&&" | rel_op | add_op | mul_op
def nt_binary_op():
	if symbol=="||":
		accept("||")
	elif symbol=="&&":
		accept("&&")
	elif symbol in nt_rel_op_set:
		nt_rel_op()
	elif symbol in nt_add_op_set:
		nt_add_op()
	elif symbol in nt_mul_op_set:
		nt_mul_op()
	else:
		output_error_and_halt()

# <rel_op> ::= "==" | "!=" | "<" | "<=" | ">" | ">="
nt_rel_op_set = {"==" , "!=" , "<" , "<=" , ">" , ">="}
def nt_rel_op():
	acceptset(nt_rel_op_set)

# <add_op> ::= "+" | "-" | "|" | "^"
nt_add_op_set = {"+" , "-" , "|" , "^"}
def nt_add_op():
	acceptset(nt_add_op_set)

# <mul_op> ::= "*" | "/" | "%" | "<<" | ">>" | "&" | "&^"
nt_mul_op_set = {"*" , "/" , "%" , "<<" , ">>" , "&" , "&^"}
def nt_mul_op():
	acceptset(nt_mul_op_set)

# <unary_op> ::= "+" | "-" | "!" | "^" | "*" | "&" | "<-"
nt_unary_op_set = {"+","-","!","^","*","&","<-"}
def nt_unary_op():
	acceptset(nt_unary_op_set)

nt_binary_op_set = nt_rel_op_set.union(nt_add_op_set).union(nt_mul_op_set).union({"||","&&"})
# <Conversion> ::= Type "(" Expression [ "," ] ")"
def nt_Conversion():
	nt_Type()
	accept("(")
	nt_Expression()
	if symbol==",":
		accept(",")
	accept(")")

# <Statement> ::= Declaration | LabeledStmt | SimpleStmt | GoStmt | ReturnStmt | BreakStmt | ContinueStmt | GotoStmt | FallthroughStmt | Block | IfStmt | SwitchStmt | SelectStmt | ForStmt | DeferStmt
# change to: <Statement> ::= Declaration | LabeledStmtOrSimpleStmt | GoStmt | ReturnStmt | BreakStmt | ContinueStmt | GotoStmt | FallthroughStmt | Block | IfStmt | SwitchStmt | SelectStmt | ForStmt | DeferStmt
def nt_Statement():
	if symbol in set({"const", "type", "var"}):
		nt_Declaration()
	elif symbol=="go":
		nt_GoStmt()
	elif symbol=="return":
		nt_ReturnStmt()
	elif symbol=="break":
		nt_BreakStmt()
	elif symbol=="continue":
		nt_ContinueStmt()
	elif symbol=="goto":
		nt_GotoStmt()
	elif symbol=="fallthrough":
		nt_FallthroughStmt()
	elif symbol=="{":
		nt_Block()
	elif symbol=="if":
		nt_IfStmt()
	elif symbol=="switch":
		nt_SwitchStmt()
	elif symbol=="select":
		nt_SelectStmt()
	elif symbol=="for":
		nt_ForStmt()
	elif symbol=="defer":
		nt_DeferStmt()
	else:
		nt_LabeledStmtOrSimpleStmt()

# add new rule: <LabeledStmtOrSimpleStmt>
def nt_LabeledStmtOrSimpleStmt():
	if symbol in {";","{","}"}:
		nt_EmptyStmt()
	elif symbol in set(string.ascii_letters+"_"): #begins with identifier
		nt_identifier()
		if symbol==":": #LabeledStmt
			accept(":")
			nt_Statement()
		else:
			if symbol==",":
				accept(",")
				nt_IdentifierList()
			if symbol == ":=":
				accept(":=")
				nt_ExpressionList()
			else:
				statementFinished = False
				#finish the expression
				while symbol in {".", "[", "("}:
					if symbol==".":
						nt_SelectorOrTypeAssertion()
					elif symbol=="[":
						nt_IndexOrSlice()
					else: #symbol=="("
						# Arguments, also includes conversion
						nt_Arguments()

				if symbol in {",","+", "-", "|", "^","*", "/", "%", "<<", ">>", "&", "&^"}:
					acceptset({",","+", "-", "|", "^","*", "/", "%", "<<", ">>", "&", "&^"})
					if symbol=="=":
						accept("=")
						nt_ExpressionList()
						statementFinished=True
					nt_ExpressionList()
				elif symbol not in {",","++","--","<-","=",";","}"}:
					if symbol in nt_assign_op_set:
						nt_assign_op()
					else:
						nt_binary_op()
					nt_ExpressionList()

				if symbol=="," and not statementFinished:
					accept(",")
					nt_ExpressionList()

				#after that:
				nt_SimpleStmtRhs(statementFinished)
	else: #begins with expression
		# ExpressionStmt | SendStmt | IncDecStmt | Assignment
		# Expression [ "<-" Expression | "++" | "--" | [ "," ExpressionList ] assign_op ExpressionList]
		nt_Expression()
		nt_SimpleStmtRhs()

# <SimpleStmt> ::= EmptyStmt | ExpressionStmt | SendStmt | IncDecStmt | Assignment | ShortVarDecl
#	NOT LL(1)
def nt_SimpleStmt():
	if symbol in {";","{","}"}:
		nt_EmptyStmt()
	elif symbol in set(string.ascii_letters+"_"): #begins with identifier
		nt_IdentifierList()
		if symbol == ":=":
			accept(":=")
			nt_ExpressionList()
		else:
			statementFinished = False
			#finish the expression
			if symbol=="(": #Conversion, identifier is type, then follows "(" Expression [ "," ] ")"
				accept("(")
				nt_Expression()
				if symbol==",":
					nt_Expression()
				accept(")")
			while symbol in {".", "[", "("}:
				if symbol==".":
					nt_SelectorOrTypeAssertion()
				elif symbol=="[":
					nt_IndexOrSlice()
				else: #symbol=="("
					# Arguments, also includes conversion
					nt_Arguments()
			if symbol in {",","+", "-", "|", "^","*", "/", "%", "<<", ">>", "&", "&^"}:
				acceptset({",","+", "-", "|", "^","*", "/", "%", "<<", ">>", "&", "&^"})
				if symbol=="=":
					accept("=")
					nt_ExpressionList()
					statementFinished=True
				nt_ExpressionList()
			elif symbol not in {",","++","--","<-","=",";","}"}:
				nt_binary_op()
				nt_ExpressionList()

			if symbol=="," and not statementFinished:
				accept(",")
				nt_ExpressionList()

			#after that:
			nt_SimpleStmtRhs(statementFinished)
	else: #begins with expression
		# ExpressionStmt | SendStmt | IncDecStmt | Assignment
		# Expression [ "<-" Expression | "++" | "--" | [ "," ExpressionList ] assign_op ExpressionList]
		nt_Expression()
		nt_SimpleStmtRhs()

# <EmptyStmt> ::=
def nt_EmptyStmt():
	pass

# <LabeledStmt> ::= Label ":" Statement
def nt_LabeledStmt():
	nt_Label()
	accept(":")
	nt_Statement()

# <Label> ::= identifier
def nt_Label():
	nt_identifier()
# <ExpressionStmt> ::= Expression
def nt_ExpressionStmt():
	nt_Expression()

# <SendStmt> ::= Channel "<-" Expression
def nt_SendStmt():
	nt_Channel()
	accept("<-")
	nt_Expression()

# <Channel> ::= Expression
def nt_Channel():
	nt_Expression()

# <IncDecStmt> ::= Expression ( "++" | "--" )
def nt_IncDecStmt():
	nt_Expression()
	if symbol=="++":
		accept("++")
	else:
		accept("--")

# <Assignment> ::= ExpressionList assign_op ExpressionList
def nt_Assignment():
	nt_ExpressionList()
	nt_assign_op()
	nt_ExpressionList()

# <assign_op> ::= [ add_op | mul_op ] "="
# turns out this isn't consistent
# we now refer to the operator list
nt_assign_op_set = ['+=','&=','-=','|=','<=','*=','^=','>=','/=','<<=','%=','>>=','&^=','=']
def nt_assign_op():
	acceptset(nt_assign_op_set)

# <IfStmt> ::= "if" [ SimpleStmt ";" ] Expression Block [ "else" ( IfStmt | Block ) ]
#	FIRST(SimpleStmt) also contains FIRST(Expression)
#	<IfStmt> ::= "if" [ [ ExpressionStmt | SendStmt | IncDecStmt | Assignment | ShortVarDecl] ";" ] Expression Block [ "else" ( IfStmt | Block ) ]
#	<IfStmt> ::= "if" [ [ Expression [ "<-" Expression | "++" | "--" | { "," Expression } assign_op ExpressionList ] | IdentifierList ":::=" ExpressionList] ";" ] Expression Block [ "else" ( IfStmt | Block ) ]
def nt_IfStmt():
	accept("if")
	if symbol in set(string.ascii_letters+"_"): #maybe identifierlist, maybe expression
		nt_identifier()
		if symbol=="," or symbol==":=" : #obviously identifierList
			if symbol==",":
				accept(",")
				nt_IdentifierList()
			accept(":=")
			nt_ExpressionList()
			acceptsemicolon()
			nt_Expression()
		else:
			while symbol in {".", "[", "("}:
				if symbol==".":
					nt_SelectorOrTypeAssertion()
				elif symbol=="[":
					nt_IndexOrSlice()
				else: #symbol=="("
					# Arguments, also includes conversion
					nt_Arguments()
			#	<Expression> ::= UnaryExpr | Expression binary_op Expression
			if symbol not in {"<-", "++", "--", ",", ";", "{"}:
				nt_binary_op()
				nt_Expression()
			if symbol!="{":
				nt_SimpleStmtRhs()

	elif symbol == ";":
		acceptsemicolon()
		nt_Expression()
	else:
		nt_Expression()
		if symbol!="{":
			nt_SimpleStmtRhs()
			acceptsemicolon()
			nt_Expression()
	nt_Block()
	if symbol=="else":
		accept("else")
		if symbol=="if":
			nt_IfStmt()
		else:
			nt_Block()

def nt_SimpleStmtRhs(statementFinished=False):
	stmtdone = False
	while not stmtdone and symbol in {"<-","++","--",",","+", "-", "|", "^","*", "/", "%", "<<", ">>", "&", "&^","="}.union(nt_binary_op_set):
		if symbol=="<-":
			accept("<-")
			nt_Expression()
			stmtdone=True
		elif symbol=="++":
			accept("++")
			stmtdone=True
		elif symbol=="--":
			accept("--")
			stmtdone=True
		elif symbol in {",","+", "-", "|", "^","*", "/", "%", "<<", ">>", "&", "&^","="}.union(nt_binary_op_set) and not statementFinished:
			if symbol==",":
				accept(",")
				nt_ExpressionList()
			if symbol in nt_binary_op_set:
				nt_binary_op()
			elif symbol in nt_assign_op_set:
				nt_assign_op()
				stmtdone=True
			nt_ExpressionList()

# <SwitchStmt> ::= ExprSwitchStmt | TypeSwitchStmt
# maybe ExprSwitchStmt and TypeSwitchStmt needs to be merged
# change to: <SwitchStmt> ::= "switch" [ SimpleStmt ";" ] ( [ Expression ] "{" { ExprCaseClause } "}" | TypeSwitchGuard "{" { TypeCaseClause } "}" )
#	<SwitchStmt> ::= "switch" [ SimpleStmt ";" ] ( "{" { ExprCaseClause } | ( Expression "{" ExprCaseClause | [ identifier ":=" ] PrimaryExpr "." "(" "type" ")" "{" { TypeCaseClause } )) "}"
def nt_SwitchStmt():
	accept("switch")

	if symbol != "{":
		if symbol in set(string.ascii_letters+"_"): #might be identifier
			nt_identifier()
			if symbol==":=": #this one is obvious
				accept(":=")
				nt_PrimaryExpr()
				accept(".")
				accept("(")
				accept("case")
				accept(")")
				isTypeSwitchStmt = True
			else:
				#might be SimpleStmt or Expression or PrimaryExpr
				isTypeSwitchStmt = tryParseUntilTypeSwitchGuard()

		else: #might be SimpleStmt or PrimaryExpr
			if symbol==";":
				accept(";")
			else: #might be SimpleStmt that begins with Expression; or PrimaryExpr
				if symbol in nt_unary_op_set: #obviously not PrimaryExpr
					# ExpressionStmt | SendStmt | IncDecStmt | Assignment
					# Expression [ "<-" Expression | "++" | "--" | [ "," ExpressionList ] assign_op ExpressionList]
					nt_Expression()
					isSurelyStmt = symbol in {"<-","++","--",",","+", "-", "|", "^","*", "/", "%", "<<", ">>", "&", "&^","="}
					nt_SimpleStmtRhs()
					if isSurelyStmt or symbol==";":
						accept(";")
						if symbol=="{":
							isTypeSwitchStmt=False
						else:
							#might be Expression, or PrimaryExpr
							nt_PrimaryExprFront()
							isTypeSwitchStmt = tryParseUntilTypeSwitchGuard()
					else:
						isTypeSwitchStmt=False

				else: #PrimaryExpr or PrimaryExpr binary_op Expression
						#if PrimaryExpr, cannot use nt_PrimaryExpr() because there is "." "(" "type" ")" after
					nt_PrimaryExprFront()
					isTypeSwitchStmt = tryParseUntilTypeSwitchGuard()
	else:
		isTypeSwitchStmt = False
	accept("{")
	if isTypeSwitchStmt:
		while symbol != "}":
			nt_TypeCaseClause()
	else:
		while symbol != "}":
			nt_ExprCaseClause()
	accept("}")

def tryParseUntilTypeSwitchGuard():
	isTypeSwitchGuard=False
	while symbol in {".", "[", "("} and not isTypeSwitchGuard:
		if symbol==".":
			accept(".")
			if symbol=="(":
				accept("(")
				if symbol=="type":
					isTypeSwitchGuard=True
				else:
					nt_Type()
				accept(")")
			else:
				nt_identifier()
		elif symbol=="[":
			nt_IndexOrSlice()
		else: #symbol=="("
			# Arguments, also includes conversion
			nt_Arguments()
	if not isTypeSwitchGuard:
		if symbol != "{":
			nt_binary_op()
			nt_Expression()
	return isTypeSwitchGuard

# <ExprSwitchStmt> ::= "switch" [ SimpleStmt ";" ] [ Expression ] "{" { ExprCaseClause } "}"
def nt_ExprSwitchStmt():
	accept("switch")
	#TODO continue.
	#	FIRST(SimpleStmt) can be FIRST(Expression)

# <ExprCaseClause> ::= ExprSwitchCase ":" StatementList
def nt_ExprCaseClause():
	nt_ExprSwitchCase()
	accept(":")
	nt_StatementList()

# <ExprSwitchCase> ::= "case" ExpressionList | "default"
def nt_ExprSwitchCase():
	if symbol=="case":
		accept("case")
		nt_ExpressionList()
	else:
		accept("default")

# <TypeSwitchStmt> ::= "switch" [ SimpleStmt ";" ] TypeSwitchGuard "{" { TypeCaseClause } "}"
#	This one is also not LL(1)
#	TODO implement this

# <TypeSwitchGuard> ::= [ identifier ":=" ] PrimaryExpr "." "(" "type" ")"
#	Not LL(1)
def nt_TypeSwitchGuard():
	if symbol in set(string.ascii_letters+"_"):
		nt_identifier()
		if symbol==":=":
			accept(":=")
			#cannot use nt_PrimaryExpr() here because "." is in FOLLOW(Selector)
			#nt_PrimaryExpr()
			#TODO fix this
		else:
			while symbol in {".","["}:
				if symbol=="[":
					nt_IndexOrSlice()
				else:
					accept(".")
					if symbol!="(":
						nt_identifier()
					else:
						accept("(")
						if symbol!="type":
							nt_Type()
							accept(")")
			accept("type")
			accept(")")
	else:
		nt_PrimaryExpr()

# <TypeCaseClause> ::= TypeSwitchCase ":" StatementList
def nt_TypeCaseClause():
	nt_TypeSwitchCase()
	accept(":")
	nt_StatementList()

# <TypeSwitchCase> ::= "case" TypeList | "default"
def nt_TypeSwitchCase():
	if symbol=="case":
		accept("case")
		nt_TypeList()
	elif symbol=="default":
		accept("default")
	else:
		output_error_and_halt()

# <TypeList> ::= Type { "," Type }
def nt_TypeList():
	nt_Type()
	while symbol==",":
		accept(",")
		nt_Type()

# <ForStmt> ::= "for" [ Condition | ForClause | RangeClause ] Block
#	Not LL(1)
def nt_ForStmt():
	accept("for")
	after_identifier = False
	isList=False
	if symbol in set(string.ascii_letters).union({"_"}):
		nt_identifier()
		after_identifier = True
		while symbol == "," and after_identifier:
			accept(",")
			isList=True
			after_identifier = False
			if symbol in set(string.ascii_letters).union({"_"}):
				nt_identifier()
				after_identifier=True

	if symbol == ":=" and after_identifier:
		accept(":=")
		if symbol=="range":
			accept("range")
			nt_Expression()
		else:
			nt_ExpressionList()
			acceptsemicolon()
			if symbol != ";":
				nt_Condition()
			acceptsemicolon()
			if symbol != "{": #FOLLOW(ForClause)
				nt_PostStmt()
	elif symbol == "=" and after_identifier:
		accept("=")
		if symbol=="range":
			accept("range")
			nt_Expression()
		else:
			nt_Expression()
			acceptsemicolon()
			if symbol != ";":
				nt_Condition()
			acceptsemicolon()
			if symbol != "{": #FOLLOW(ForClause)
				nt_PostStmt()
	elif symbol != "{":
		if after_identifier:
			while symbol in {".", "[", "("}:
				if symbol==".":
					nt_SelectorOrTypeAssertion()
				elif symbol=="[":
					nt_IndexOrSlice()
				else: #symbol=="("
					# Arguments, also includes conversion
					nt_Arguments()
			if symbol not in {",",";","="}:
				nt_binary_op()
				nt_Expression()
		else:
			nt_Expression()
		if symbol==",":
			accept(",")
			isList=True
			nt_ExpressionList()
		elif symbol==";" and not isList: #ForClause
			acceptsemicolon()
			if symbol != ";":
				nt_Condition()
			acceptsemicolon()
			if symbol != "{": #FOLLOW(ForClause)
				nt_PostStmt()
		if symbol=="=" or isList:
			accept("=")
			accept("range")
			nt_Expression()
	nt_Block()	

# <Condition> ::= Expression
def nt_Condition():
	nt_Expression()

# <ForClause> ::= [ InitStmt ] ";" [ Condition ] ";" [ PostStmt ]
def nt_ForClause():
	if symbol != ";":
		nt_InitStmt()
	acceptsemicolon()
	if symbol != ";":
		nt_Condition()
	acceptsemicolon()
	if symbol != "{": #FOLLOW(ForClause)
		nt_PostStmt()

# <InitStmt> ::= SimpleStmt
def nt_InitStmt():
	nt_SimpleStmt()
# <PostStmt> ::= SimpleStmt
def nt_PostStmt():
	nt_SimpleStmt()
# <RangeClause> ::= [ ExpressionList "=" | IdentifierList ":=" ] "range" Expression
def nt_RangeClause():
	after_identifier = False
	if symbol in set(string.ascii_letters+"_"):
		nt_identifier()
		after_identifier = True
		while symbol == "," and after_identifier:
			accept(",")
			after_identifier = False
			if symbol in set(string.ascii_letters+"_"):
				nt_identifier()
				after_identifier=True
	if symbol == ":=" and after_identifier:
		accept(":=")
	elif symbol == "=" and after_identifier:
		accept("=")
	elif symbol != "range":
		if after_identifier:
			while symbol in {".", "[", "("}:
				if symbol==".":
					nt_SelectorOrTypeAssertion()
				elif symbol=="[":
					nt_IndexOrSlice()
				else: #symbol=="("
					# Arguments, also includes conversion
					nt_Arguments()
			if symbol==",":
				accept(",")
				nt_ExpressionList()
			elif symbol != "=":
				nt_binary_op()
				nt_ExpressionList()
		else:
			nt_ExpressionList()
		accept("=")
	accept("range")
	nt_Expression()

# <GoStmt> ::= "go" Expression
def nt_GoStmt():
	accept("go")
	nt_Expression()

# <SelectStmt> ::= "select" "{" { CommClause } "}"
def nt_SelectStmt():
	accept("select")
	accept("{")
	while symbol == "case" or symbol == "default":
		nt_CommClause()
	accept("}")

# <CommClause> ::= CommCase ":" StatementList
def nt_CommClause():
	nt_CommCase()
	accept(":")
	nt_StatementList()
# <CommCase> ::= "case" ( SendStmt | RecvStmt ) | "default"
	#this is not LL(1) because first(SendStmt) and first(RecvStmt) intersects each other
# <RecvStmt> ::= [ ExpressionList "=" | IdentifierList ":=" ] RecvExpr
	#this is not LL(1) because first(ExpressionList) contains first(IdentifierList)
	#here we first assume that it is IdentifierList ":=", but if a symbol other outside that we switch to ExpressionList "="
# This is the implementation for both <RecvStmt> and <CommCase>
def nt_CommCase():
	if symbol=="case":
		accept("case")
		after_identifier = False
		isList = False
		if symbol in set(string.ascii_letters+"_"):
			nt_identifier()
			after_identifier = True

			while symbol == "," and after_identifier:
				accept(",")
				isList = True
				after_identifier = False
				if symbol in set(string.ascii_letters+"_"):
					nt_identifier()
					after_identifier=True

		if symbol == "<-" and not isList and after_identifier:
			accept("<-")	
			nt_Expression()
		elif symbol == ":=":
			accept(":=")
			nt_RecvExpr()
		elif symbol == "=":
			accept("=")
			nt_RecvExpr()
		else:
			if after_identifier:
				while symbol in {".", "[", "("}:
					if symbol==".":
						nt_SelectorOrTypeAssertion()
					elif symbol=="[":
						nt_IndexOrSlice()
					else: #symbol=="("
						# Arguments, also includes conversion
						nt_Arguments()
				if symbol not in {",","="}:
					nt_binary_op()
					nt_Expression()
			else:
				nt_Expression()
			if symbol == "<-":
				accept("<-")
				nt_Expression()
			elif symbol=="," or symbol=="=":
				if symbol == ",":
					accept(",")
					nt_ExpressionList()
				accept("=")
				nt_RecvExpr()
			elif isList:
				output_error_and_halt()

	else:
		accept("default")

def nt_RecvExpr():
	nt_Expression()

# <ReturnStmt> ::= "return" [ ExpressionList ]
def nt_ReturnStmt():
	accept("return")
	if symbol != ";":
		nt_ExpressionList()


# <BreakStmt> ::= "break" [ Label ]
def nt_BreakStmt():
	accept("break")
	if symbol in set(string.ascii_letters).union({"_"}):
		nt_Label()

# <ContinueStmt> ::= "continue" [ Label ]
def nt_ContinueStmt():
	accept("continue")
	if symbol in set(string.ascii_letters).union({"_"}):
		nt_Label()

# <GotoStmt> ::= "goto" Label
def nt_GotoStmt():
	accept("goto")
	nt_Label()

# <FallthroughStmt> ::= "fallthrough"
def nt_FallthroughStmt():
	accept("fallthrough")

# <DeferStmt> ::= "defer" Expression
def nt_DeferStmt():
	accept("defer")
	nt_Expression()

# <SourceFile> ::= PackageClause ";" { ImportDecl ";" } { TopLevelDecl ";" }
def nt_SourceFile():
	nt_PackageClause()
	acceptsemicolon()
	while symbol=="import":
		nt_ImportDecl()
		acceptsemicolon()
	while symbol in {"const","type","var","func"}:
		nt_TopLevelDecl()
		acceptsemicolon()

# <PackageClause> ::= "package" PackageName
def nt_PackageClause():
	accept("package")
	nt_PackageName()

# <PackageName> ::= identifier
def nt_PackageName():
	nt_identifier()

# <ImportDecl> ::= "import" ( ImportSpec | "(" { ImportSpec ";" } ")" )
def nt_ImportDecl():
	accept("import")
	if symbol in set(string.ascii_letters).union({"_",".","`",'"'}):
		nt_ImportSpec()
	elif symbol=="(":
		accept("(")
		while symbol in set(string.ascii_letters).union({"_",".","`",'"'}):
			nt_ImportSpec()
			acceptsemicolon()
		accept(")")
	else:
		output_error_and_halt()

# <ImportSpec> ::= [ "." | PackageName ] ImportPath
def nt_ImportSpec():
	if symbol==".":
		accept(".")
	elif symbol in set(string.ascii_letters):
		nt_PackageName()
	nt_ImportPath()

# <ImportPath> ::= string_lit
def nt_ImportPath():
	nt_string_lit()


import sys

#END OF GRAMMAR IMPLEMENTATION
if __name__ == '__main__':
	import sys
	if len(sys.argv) != 2:
		print("to test: preprocess.py <inputfile>")
		sys.exit()

	main(sys.argv[1])