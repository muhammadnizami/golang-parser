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
		read_one_symbool()
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
# <Selector> ::= "." identifier
# <Index> ::= "[" Expression "]"
# <Slice> ::= "[" [ Expression ] ":" [ Expression ] "]" | "[" [ Expression ] ":" Expression ":" Expression "]"
# <TypeAssertion> ::= "." "(" Type ")"
# <Arguments> ::= "(" [ ( ExpressionList | Type [ "," ExpressionList ] ) [ "..." ] [ "," ] ] ")"
# <MethodExpr> ::= ReceiverType "." MethodName
# <ReceiverType> ::= Type
# <Expression> ::= UnaryExpr | Expression binary_op Expression
# <UnaryExpr> ::= PrimaryExpr | unary_op UnaryExpr
# <binary_op> ::= "||" | "&&" | rel_op | add_op | mul_op
# <rel_op> ::= "==" | "!=" | "<" | "<=" | ">" | ">="
# <add_op> ::= "+" | "-" | "|" | "^"
# <mul_op> ::= "*" | "/" | "%" | "<<" | ">>" | "&" | "&^"
# <unary_op> ::= "+" | "-" | "!" | "^" | "*" | "&" | "<-"
# <Conversion> ::= Type "(" Expression [ "," ] ")"
# <Statement> ::= Declaration | LabeledStmt | SimpleStmt | GoStmt | ReturnStmt | BreakStmt | ContinueStmt | GotoStmt | FallthroughStmt | Block | IfStmt | SwitchStmt | SelectStmt | ForStmt | DeferStmt
# <SimpleStmt> ::= EmptyStmt | ExpressionStmt | SendStmt | IncDecStmt | Assignment | ShortVarDecl
# <EmptyStmt> ::=
# <LabeledStmt> ::= Label ":" Statement
# <Label> ::= identifier
# <ExpressionStmt> ::= Expression
# <SendStmt> ::= Channel "<-" Expression
# <Channel> ::= Expression
# <IncDecStmt> ::= Expression ( "++" | "--" )
# <Assignment> ::= ExpressionList assign_op ExpressionList
# <assign_op> ::= [ add_op | mul_op ] "="
# <IfStmt> ::= "if" [ SimpleStmt ";" ] Expression Block [ "else" ( IfStmt | Block ) ]
# <SwitchStmt> ::= ExprSwitchStmt | TypeSwitchStmt
# <ExprSwitchStmt> ::= "switch" [ SimpleStmt ";" ] [ Expression ] "{" { ExprCaseClause } "}"
# <ExprCaseClause> ::= ExprSwitchCase ":" StatementList
# <ExprSwitchCase> ::= "case" ExpressionList | "default"
# <TypeSwitchStmt> ::= "switch" [ SimpleStmt ";" ] TypeSwitchGuard "{" { TypeCaseClause } "}"
# <TypeSwitchGuard> ::= [ identifier ":=" ] PrimaryExpr "." "(" "type" ")"
# <TypeCaseClause> ::= TypeSwitchCase ":" StatementList
# <TypeSwitchCase> ::= "case" TypeList | "default"
# <TypeList> ::= Type { "," Type }
# <ForStmt> ::= "for" [ Condition | ForClause | RangeClause ] Block
# <Condition> ::= Expression
# <ForClause> ::= [ InitStmt ] ";" [ Condition ] ";" [ PostStmt ]
# <InitStmt> ::= SimpleStmt
# <PostStmt> ::= SimpleStmt
# <RangeClause> ::= [ ExpressionList "=" | IdentifierList ":=" ] "range" Expression
# <GoStmt> ::= "go" Expression
# <SelectStmt> ::= "select" "{" { CommClause } "}"
# <CommClause> ::= CommCase ":" StatementList
# <CommCase> ::= "case" ( SendStmt | RecvStmt ) | "default"
# <RecvStmt> ::= [ ExpressionList "=" | IdentifierList ":=" ] RecvExpr
# <RecvExpr> ::= Expression
# <ReturnStmt> ::= "return" [ ExpressionList ]
# <BreakStmt> ::= "break" [ Label ]
# <ContinueStmt> ::= "continue" [ Label ]
# <GotoStmt> ::= "goto" Label
# <FallthroughStmt> ::= "fallthrough"
# <DeferStmt> ::= "defer" Expression
# <SourceFile> ::= PackageClause ";" { ImportDecl ";" } { TopLevelDecl ";" }
# <PackageClause> ::= "package" PackageName
# <PackageName> ::= identifier
# <ImportDecl> ::= "import" ( ImportSpec | "(" { ImportSpec ";" } ")" )
# <ImportSpec> ::= [ "." | PackageName ] ImportPath
# <ImportPath> ::= string_lit
# <ExprSwitchCase> ::= "case" ExpressionList | "default"
# <TypeSwitchStmt> ::= "switch" [ SimpleStmt ";" ] TypeSwitchGuard "{" { TypeCaseClause } "}"
# <TypeSwitchGuard> ::= [ identifier ":=" ] PrimaryExpr "." "(" "type" ")"
# <TypeCaseClause> ::= TypeSwitchCase ":" StatementList
# <TypeSwitchCase> ::= "case" TypeList | "default"
# <TypeList> ::= Type { "," Type }
# <ForStmt> ::= "for" [ Condition | ForClause | RangeClause ] Block
# <Condition> ::= Expression
def nt_Condition():
	nt_Expression()

# <ForClause> ::= [ InitStmt ] ";" [ Condition ] ";" [ PostStmt ]
def nt_ForClause():
	if symbol != ";":
		nt_InitStmt()
	if symbol != ";":
		nt_Condition()
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
 	while symbol == ",":
		accept(",")
		after_identifier = False
		if symbol in set(string.ascii_letters+"_"):
			nt_identifier()
			after_idetifier=True
 	if symbol == ":=":
		accept(":=")
	elif symbol == "=":
		accept("=")
	elif symbol != "range":
		if after_identifier:
			nt_binary_op()
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
		if symbol in set(string.ascii_letters+"_"):
			nt_identifier()
			after_identifier = True

		isList = False
		while symbol == ",":
			accept(",")
			isList = True
			after_identifier = False
			if symbol in set(string.ascii_letters+"_"):
				nt_identifier()
				after_idetifier=True

		if symbol == "<-" and not isList:
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
				nt_binary_op()
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