import preprocess
import symbol_read
import string
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
		read_one_symbol()
	else:
		output_error_and_halt()

def acceptset(Ts):
	global symbol
	if symbol in Ts:
		read_one_symbol()
	else:
		output_error_and_halt()

#all nonterminal symbols
#format: nt_<symbol_name>

# <newline> ::= /* the Unicode code point U+000A */ 
# <unicode_char> ::= /* an arbitrary Unicode code point except newline */ 
# <unicode_letter> ::= /* a Unicode code point classified as "Letter" */ 
# <unicode_digit> ::= /* a Unicode code point classified as "Number, decimal digit" */ 
# <letter> ::= unicode_letter | "_"
# <decimal_digit> ::= "0" … "9"
# <octal_digit> ::= "0" … "7"
# <hex_digit> ::= "0" … "9" | "A" … "F" | "a" … "f"

# <identifier> ::= letter { letter | unicode_digit }
def nt_identifier():
	nt_letter()
	while symbol in set(string.ascii_letters):
		nt_letter()
	while symbol in set(string.unicode_digit):
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
# <hex_lit> ::= "0" ( "x" | "X" ) hex_digit { hex_digit }
# <float_lit> ::= decimals "." [ decimals ] [ exponent ] | decimals exponent | "." decimals [ exponent ]
# <decimals> ::= decimal_digit { decimal_digit }
# <exponent> ::= ( "e" | "E" ) [ "+" | "-" ] decimals
# <imaginary_lit> ::= (decimals | float_lit) "i"

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
# <byte_value> ::= octal_byte_value | hex_byte_value
# <octal_byte_value> ::= `\` octal_digit octal_digit octal_digit
# <hex_byte_value> ::= `\` "x" hex_digit hex_digit
# <little_u_value> ::= `\` "u" hex_digit hex_digit hex_digit hex_digit
# <big_u_value> ::= `\` "U" hex_digit hex_digit hex_digit hex_digit hex_digit hex_digit hex_digit hex_digit
# <escaped_char> ::= `\` ( "a" | "b" | "f" | "n" | "r" | "t" | "v" | `\` | "'" | `"` )

# <string_lit> ::= raw_string_lit | interpreted_string_lit
# <raw_string_lit> ::= "`" { unicode_char | newline } "`"
# <interpreted_string_lit> ::= `"` { unicode_value | byte_value } `"`

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
def nt_Expression():
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
		accept(";")
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
		nt_ParameterDecl

# <ParameterDecl> ::= [ IdentifierList ] [ "..." ] Type
def nt_ParameterDecl():
	if symbol == set(string.ascii_letters).union({"_"}):
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
		accept(";")
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
		accept == "<-"
		accept == "chan"
	else:
		output_error_and_halt()

# <Block> ::= "{" StatementList "}"
def nt_Block():
	accept("{")
	nt_StatementList()
	accept("}")

# <StatementList> ::= { Statement ";" }
def nt_StatementList():
	while symbol in set(string.ascii_letters).union({"_"}):
		nt_Statement()
		accept(";")

# <Declaration> ::= ConstDecl | TypeDecl | VarDecl
def nt_Declaration():
	if symbol == "const":
		nt_ConstDecl()
	elif symbol == "type":
		nt_TypeDecl()
	elif symbol == "var":
		nt_VarDecl()

# <TopLevelDecl> ::= Declaration | FunctionDecl | MethodDecl
def nt_TopLevelDecl():
	if symbol in set({"const", "type", "var"}):
		nt_Declaration()
	elif symbol == "func":
		nt_FunctionDecl()
	elif symbol == "func":
		nt_MethodDecl()

# <ConstDecl> ::= "const" ( ConstSpec | "(" { ConstSpec ";" } ")" )
def nt_ConstDecl():
	accept("const")
	if symbol in set(string.ascii_letters).union({"_","("}):
		if symbol == "(":
			accept("(")
			nt_ConstSpec()
			accept(";")
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
			accept(";")
		accept(")")
	else:
		output_error_and_halt()

# <TypeSpec> ::= AliasDecl | TypeDef
def nt_TypeSpec():
	if symbol in set(string.ascii_letters).union({"_"}):
		nt_AliasDecl()
	elif symbol in set({"(","[","struct","*","func","interface","map","chan","<-"}):
		nt_TypeDef()
	
# <AliasDecl> ::= identifier "::=" Type
def nt_AliasDecl():
	nt_identifier()
	accept("::=")
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
			accept(";")
		accept(")")
	elif symbol in set(string.ascii_letters).union({"_"}):
		nt_VarSpec()
	else:
		output_error_and_halt()

# <VarSpec> ::= IdentifierList ( Type [ "::=" ExpressionList ] | "::=" ExpressionList )
def nt_VarSpec():
	nt_IdentifierList()
	if symbol == "::=":
		accept("::=")
		nt_ExpressionList()
	elif symbol in set(string.ascii_letters).union({"_"}):
		nt_Type()
		if symbol == "::=":
			accept("::=")
			nt_ExpressionList()
	else:
		output_error_and_halt()

# <ShortVarDecl> ::= IdentifierList ":::=" ExpressionList
def nt_ShortVarDecl():
	nt_IdentifierList()
	accept(":::=")
	nt_ExpressionList()

# <FunctionDecl> ::= "func" FunctionName Signature [ FunctionBody ]
def nt_FunctionDecl():
	accept("func")
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
def MethodDecl():
	accept("func")
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
		nt_Expression()
	else:
		nt_Literal()

# <Literal> ::= BasicLit | CompositeLit | FunctionLit
# <BasicLit> ::= int_lit | float_lit | imaginary_lit | rune_lit | string_lit
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
#	NOT LL(1)

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
def Expression():
	nt_UnaryExpr()
	while symbol not in {",",";","}","]",")",":"}:
		nt_UnaryExpr()

# <UnaryExpr> ::= PrimaryExpr | unary_op UnaryExpr
def nt_UnaryExpr():
	if symbol in nt_unary_op_set:
		unary_op()
	else:
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

# <Conversion> ::= Type "(" Expression [ "," ] ")"
def nt_Conversion():
	nt_Type()
	accept("(")
	nt_Expression()
	if symbol==",":
		accept(",")
	accept(")")

# <Statement> ::= Declaration | LabeledStmt | SimpleStmt | GoStmt | ReturnStmt | BreakStmt | ContinueStmt | GotoStmt | FallthroughStmt | Block | IfStmt | SwitchStmt | SelectStmt | ForStmt | DeferStmt
#	NOT LL(1)
# <SimpleStmt> ::= EmptyStmt | ExpressionStmt | SendStmt | IncDecStmt | Assignment | ShortVarDecl
#	NOT LL(1)

# <EmptyStmt> ::=
def EmptyStmt():
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
def nt_assign_op():
	if symbol in {"+", "-", "|", "^"}:
		nt_add_op()
	elif symbol in {"*", "/", "%", "<<", ">>", "&", "&^"}:
		nt_mul_op()
	accept("=")

# <IfStmt> ::= "if" [ SimpleStmt ";" ] Expression Block [ "else" ( IfStmt | Block ) ]
# 	FIRST(SimpleStmt) also contains FIRST(Expression)

# <SwitchStmt> ::= ExprSwitchStmt | TypeSwitchStmt
# maybe ExprSwitchStmt and TypeSwitchStmt needs to be merged

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
	if symbol in set(string.ascii_letters+"_"):
		nt_identifier()
		after_identifier = True
	 	while symbol == "," and after_identifier:
			accept(",")
			isList=True
			after_identifier = False
			if symbol in set(string.ascii_letters+"_"):
				nt_identifier()
				after_identifier=True

	if symbol == ":=" and after_identifier:
		accept(":=")
	 	accept("range")
	 	nt_Expression()
	elif symbol == "=" and after_identifier:
		accept("=")
	 	accept("range")
	 	nt_Expression()
	elif symbol != "{":
		if after_identifier:
			if symbol=="(": #Conversion, identifier is type, then follows "(" Expression [ "," ] ")"
							#TODO implement Arguments
				accept("(")
				nt_Expression()
				if symbol==",":
					nt_Expression()
				accept(")")
			while symbol=="." or symbol=="[":
				if symbol=="[":
					nt_IndexOrSlice()
				else:
					nt_SelectorOrTypeAssertion()
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
			accept(";")
			if symbol != ";":
				nt_Condition()
			accept(";")
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
	accept(";")
	if symbol != ";":
		nt_Condition()
	accept(";")
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
			if symbol=="(": #Conversion, identifier is type, then follows "(" Expression [ "," ] ")"
				accept("(")
				nt_Expression()
				if symbol==",":
					nt_Expression()
				accept(")")
			while symbol=="." or symbol=="[":
				if symbol==".":
					nt_IndexOrSlice()
				else:
					nt_SelectorOrTypeAssertion()
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
				if symbol=="(": #Conversion, identifier is type, then follows "(" Expression [ "," ] ")"
					accept("(")
					nt_Expression()
					if symbol==",":
						nt_Expression()
					accept(")")
				while symbol=="." or symbol=="[":
					if symbol==".":
						nt_IndexOrSlice()
					else:
						nt_SelectorOrTypeAssertion()
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
	accept(";")
	while symbol=="import":
		nt_ImportDecl()
		accept(";")
	while symbol in {"const","type","var","func"}:
		nt_TopLevelDecl()
		accept(";")

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
			accept(";")
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




#END OF GRAMMAR IMPLEMENTATION
if __name__ == 'main':
	main(filename)