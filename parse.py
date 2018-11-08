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
# <int_lit> ::= decimal_lit | octal_lit | hex_lit
# <decimal_lit> ::= ( "1" … "9" ) { decimal_digit }
# <octal_lit> ::= "0" { octal_digit }
# <hex_lit> ::= "0" ( "x" | "X" ) hex_digit { hex_digit }
# <float_lit> ::= decimals "." [ decimals ] [ exponent ] | decimals exponent | "." decimals [ exponent ]
# <decimals> ::= decimal_digit { decimal_digit }
# <exponent> ::= ( "e" | "E" ) [ "+" | "-" ] decimals
# <imaginary_lit> ::= (decimals | float_lit) "i"

# <rune_lit> ::= " ' " ( unicode_value | byte_value ) " ' "
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
# <TypeName> ::= identifier | QualifiedIdent
# <TypeLit> ::= ArrayType | StructType | PointerType | FunctionType | InterfaceType | SliceType | MapType | ChannelType
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
# <ForClause> ::= [ InitStmt ] ";" [ Condition ] ";" [ PostStmt ]
# <InitStmt> ::= SimpleStmt
# <PostStmt> ::= SimpleStmt
# <RangeClause> ::= [ ExpressionList "=" | IdentifierList ":=" ] "range" Expression
# <GoStmt> ::= "go" Expression
# <SelectStmt> ::= "select" "{" { CommClause } "}"
# <CommClause> ::= CommCase ":" StatementList
# <CommCase> ::= "case" ( SendStmt | RecvStmt ) | "default"
	#this is not LL(1) because first(SendStmt) and first(RecvStmt) intersects each other
# <RecvStmt> ::= [ ExpressionList "=" | IdentifierList ":=" ] RecvExpr
	#this is not LL(1) because first(ExpressionList) contains first(IdentifierList)
	#here we first assume that it is IdentifierList ":=", but if a symbol other outside that we switch to ExpressionList "="
# This is the implementation for both <RecvStmt> and <CommCase>
def CommCase():
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
			else:
				if symbol == ",":
					accept(",")
					nt_ExpressionList()
				accept("=")
				nt_RecvExpr()

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