# Lexer
tokens = ['ASSIGN','LEFTPARAN','RIGHTPARAN','INT','NAME','PLUS', 'UNARYSUB', 'LEFTBRACKET', 'RIGHTBRACKET', 'LEFTDICTBRACKET', 'RIGHTDICTBRACKET']
reserved = {'print' : 'PRINT',
			'input' : 'INPUT'}
tokens += reserved.values()

t_ASSIGN = r'='
t_PLUS = r'\+'
t_UNARYSUB = r'\-'
t_LEFTPARAN = r'\('
t_RIGHTPARAN = r'\)'
t_LEFTBRACKET = r'\['
t_RIGHTBRACKET = r'\]'
t_LEFTDICTBRACKET = r'\{'
t_RIGHTDICTBRACKET = r'\}'
#t_COMPARE = " !=, ==, is"  

t_ignore = ' \t\r'
t_ignore_COMMENT = r'(\#[^\n]*)'

def t_INT(t):
	r'\d+'
	try:
		t.value = int(t.value)
	except ValueError:
		print "integer value too large", t.value
		t.value = 0
	return t

def t_NAME(t):
	r'[_a-zA-Z]\w*'
	if t.value in reserved:
		t.type = reserved[ t.value ]
	return t

def t_newline(t):
	r'\n+'
	t.lexer.lineno += t.value.count("\n")

def t_comment(t):
	r'\#[^\n]*'

def t_error(t):
	print "Illegal character '%s'" % t.value[0]
	t.lexer.skip(1)

import ply_3_4.lex as lex
lexer = lex.lex()

# Parser
from compiler.ast import Module, Stmt, Printnl, Add, Const, Name, Discard, CallFunc, UnarySub, AssName, Assign
precedence = (
	('nonassoc','PRINT'),
	('nonassoc','INPUT'),
	('left','PLUS'),
	('nonassoc','UNARYSUB'),
	('nonassoc','LEFTPARAN','RIGHTPARAN'),
	('nonassoc','INT','NAME'),
)

start = 'program'

def p_program(t):
	'program : module'
	t[0] = Module(None, t[1])
def p_module(t):
	'module : statement'
	#print t[0], t[1]
	t[0] = Stmt(t[1])
def p_empty(t):
	'module :'
	t[0] = Stmt([])
def p_mult_statement(t):
	'statement : statement statement'
	t[0] = t[1]+t[2]
def p_print_statement(t):
	'statement : PRINT expression'
	t[0] = [Printnl([t[2]], None)]
def p_assign_statement(t):
	'statement : NAME ASSIGN expression'
	t[0] = [Assign([AssName(t[1], 'OP_ASSIGN')],t[3])]

def p_assign_subscript_statement(t):
	'statement : expression LEFTBRACKET expression RIGHTBRACKET ASSIGN expression'
	t[0] = [Assign([Subscript(t[1], 'OP_ASSIGN', [t[3]])], t[6])]

def p_expression_statement(t):
	'statement : expression'
	t[0] = [Discard(t[1])]
def p_name_expression(t):
	'expression : NAME'
	t[0] = Name(t[1])
def p_int_expression(t):
	'expression : INT'
	t[0] = Const(t[1])
def p_plus_expression(t):
	'expression : expression PLUS expression'
	t[0] = Add((t[1], t[3]))
def p_neg_expression(t):
	'expression : UNARYSUB expression'
	t[0] = UnarySub(t[2])
def p_paren_expression(t):
	'expression : LEFTPARAN expression RIGHTPARAN'
	t[0] = t[2]
def p_input_expression(t):
	'expression : INPUT  LEFTPARAN RIGHTPARAN'
	t[0] = CallFunc(Name('input'),[])

def p_subscript_expression(t):
	'expression : expression LEFTBRACKET expression RIGHTBRACKET'
	t[0] = Subscript(t[1], 'OP_APPLY', t[3])

def p_not_expression(t):
	'expression: not expression'
	t[0] = Not(t[2])

def p_or_expression(t):
	'expression: expression or expression'
	t[0] = Or([t[1], t[3])

def p_and_expression(t):
	'expression: expression and expression'
	t[0] = And([t[1], t[3])
	
def p_compare_expression(t):
	'expression: expression COMPARE expression'	
	t[0] = Compare(t[1], [(t[2], t[3])])

def p_if_single_expression(t):
	'expression: expression if expression else expression'
	t[0] = IfExp(t[1], t[3], t[5])

##TODO: Define expr_list and key_datum_list base case behavior
def p_list_expression(t):
	'expression: LEFTBRACKET key_datum_list RIGHTBRACKET'
	t[0] = List([t[2]]) 
		#List([element1, element2])

def p_dict_expression(t):
	'expression: LEFTDICTBRACKET expr_list RIGHTDICTBRACKET'
	t[0] = Dict([t[2]])
	


def p_error(t):
	print "Syntax error at '%s'" % t.value
import ply_3_4.yacc as yacc
yacc.yacc()
