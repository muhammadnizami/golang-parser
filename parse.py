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
	elif symbol in set({"[","struct","*","func","interface","map","chan","<-"})
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
# <ArrayLength> ::= Expression
# <ElementType> ::= Type
# <SliceType> ::= "[" "]" ElementType
# <StructType> ::= "struct" "{" { FieldDecl ";" } "}"
# <FieldDecl> ::= (IdentifierList Type | EmbeddedField) [ Tag ]
# <EmbeddedField> ::= [ "*" ] TypeName
# <Tag> ::= string_lit
# <PointerType> ::= "*" BaseType
# <BaseType> ::= Type
# <FunctionType> ::= "func" Signature
# <Signature> ::= Parameters [ Result ]
# <Result> ::= Parameters | Type
# <Parameters> ::= "(" [ ParameterList [ "," ] ] ")"
# <ParameterList> ::= ParameterDecl { "," ParameterDecl }
# <ParameterDecl> ::= [ IdentifierList ] [ "..." ] Type
# <InterfaceType> ::= "interface" "{" { MethodSpec ";" } "}"
# <MethodSpec> ::= MethodName Signature | InterfaceTypeName
# <MethodName> ::= identifier
# <InterfaceTypeName> ::= TypeName
# <MapType> ::= "map" "[" KeyType "]" ElementType
# <KeyType> ::= Type
# <ChannelType> ::= ( "chan" | "chan" "<-" | "<-" "chan" ) ElementType
# <Block> ::= "{" StatementList "}"
# <StatementList> ::= { Statement ";" }
# <Declaration> ::= ConstDecl | TypeDecl | VarDecl
# <TopLevelDecl> ::= Declaration | FunctionDecl | MethodDecl
# <ConstDecl> ::= "const" ( ConstSpec | "(" { ConstSpec ";" } ")" )
# <ConstSpec> ::= IdentifierList [ [ Type ] "::=" ExpressionList ]
# <IdentifierList> ::= identifier { "," identifier }
# <ExpressionList> ::= Expression { "," Expression }
# <TypeDecl> ::= "type" ( TypeSpec | "(" { TypeSpec ";" } ")" )
# <TypeSpec> ::= AliasDecl | TypeDef
# <AliasDecl> ::= identifier "::=" Type
# <TypeDef> ::= identifier Type
# <VarDecl> ::= "var" ( VarSpec | "(" { VarSpec ";" } ")" )
# <VarSpec> ::= IdentifierList ( Type [ "::=" ExpressionList ] | "::=" ExpressionList )
# <ShortVarDecl> ::= IdentifierList ":::=" ExpressionList
# <FunctionDecl> ::= "func" FunctionName Signature [ FunctionBody ]
# <FunctionName> ::= identifier
# <FunctionBody> ::= Block
# <MethodDecl> ::= "func" Receiver MethodName Signature [ FunctionBody ]
# <Receiver> ::= Parameters
# <Operand> ::= Literal | OperandName | "(" Expression ")"
# <Literal> ::= BasicLit | CompositeLit | FunctionLit
# <BasicLit> ::= int_lit | float_lit | imaginary_lit | rune_lit | string_lit
# <OperandName> ::= identifier | QualifiedIdent.
# <QualifiedIdent> ::= PackageName "." identifier
# <CompositeLit> ::= LiteralType LiteralValue
# <LiteralType> ::= StructType | ArrayType | "[" "..." "]" ElementType | SliceType | MapType | TypeName
# <LiteralValue> ::= "{" [ ElementList [ "," ] ] "}"
# <ElementList> ::= KeyedElement { "," KeyedElement }
# <KeyedElement> ::= [ Key ":" ] Element
# <Key> ::= FieldName | Expression | LiteralValue
# <FieldName> ::= identifier
# <Element> ::= Expression | LiteralValue
# <FunctionLit> ::= "func" Signature FunctionBody
# <PrimaryExpr> ::= Operand | Conversion | MethodExpr | PrimaryExpr Selector | PrimaryExpr Index | PrimaryExpr Slice | PrimaryExpr TypeAssertion | PrimaryExpr Arguments
#	FOLLOW(Selector) contains "." which is in FIRST(Selector)
# also FOLLOW(TypeAssertion) is the same
# <Selector> ::= "." identifier
# <Index> ::= "[" Expression "]"
# <Slice> ::= "[" [ Expression ] ":" [ Expression ] "]" | "[" [ Expression ] ":" Expression ":" Expression "]"
# <TypeAssertion> ::= "." "(" Type ")"
# TODO SelectorOrTypeAssertion
# TODO IndexOrSlice
# <Arguments> ::= "(" [ ( ExpressionList | Type [ "," ExpressionList ] ) [ "..." ] [ "," ] ] ")"
# <MethodExpr> ::= ReceiverType "." MethodName
# <ReceiverType> ::= Type
# <Expression> ::= UnaryExpr | Expression binary_op Expression
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