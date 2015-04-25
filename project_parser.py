# Lexer
tokens = ['ASSIGN','LEFTPARAN','RIGHTPARAN','INT','NAME','PLUS', 'UNARYSUB', 'LEFTBRACK', 'RIGHTBRACK', 'LEFTCURL', 'RIGHTCURL', 'COMMA', 'COLON']

reserved = {}
reserved_p0 = {'print' : 'PRINT',
			'input' : 'INPUT'}
reserved.update(reserved_p0)
tokens += reserved_p0.values()

reserved_compare = {'not' : 'NOT',
			'==' : 'EQUALS',
			'!=': 'NEQUALS',
			'and' : 'AND',
			'or' : 'OR',
			'is' : 'IS',
			'if' : 'IF',
			'else' : 'ELSE'}
reserved.update(reserved_compare)
tokens += reserved_compare.values()


t_ASSIGN = r'(?<![!=])=(?!=)'
t_PLUS = r'\+'
t_UNARYSUB = r'\-'
t_LEFTPARAN = r'\('
t_RIGHTPARAN = r'\)'
t_LEFTBRACK = r'\['
t_RIGHTBRACK = r'\]'
t_LEFTCURL = r'\{'
t_RIGHTCURL = r'\}'
t_COMMA = r'\,'
t_COLON = r'\:'

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

# Parser
from compiler.ast import Module, Stmt, Printnl, Add, Const, Name, Discard, CallFunc, UnarySub, AssName, Assign, And, Not, IfExp, Compare, Or, List, Dict, Subscript
precedence = (
	('nonassoc','PRINT'),
	('nonassoc','INPUT'),
	('left','PLUS'),
	('left', 'COMMA'),
	('left', 'LEFTBRACK'),
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

def p_sub_assign_statement(t):
	'statement : expression LEFTBRACK expression RIGHTBRACK ASSIGN expression'
	t[0] = [Assign([Subscript(t[1], 'OP_ASSIGN', [t[3]])], t[6])]

def p_assign_statement(t):
	'statement : NAME ASSIGN expression'
	t[0] = [Assign([AssName(t[1], 'OP_ASSIGN')],t[3])]
def p_expression_statement(t):
	'statement : expression'
	t[0] = [Discard(t[1])]
def p_name_expression(t):
	'expression : NAME'
	t[0] = Name(t[1])
def p_int_expression(t):
	'expression : INT'
	t[0] = Const(t[1])

#TODO: Allow nested subscripts (a[0][1])
def p_sub_expression(t):
	'expression : expression LEFTBRACK expression RIGHTBRACK'
	t[0] = Subscript(t[1], 'OP_APPLY', [t[3]])

def p_plus_expression(t):
	'expression : expression PLUS expression'
	t[0] = Add((t[1], t[3]))
def p_neg_expression(t):
	'expression : UNARYSUB expression'
	t[0] = UnarySub(t[2])
def p_paren_expression(t):
	'expression : LEFTPARAN expression RIGHTPARAN'
	t[0] = t[2]

def p_if_expression(t):
	'expression : expression IF expression ELSE expression'
	t[0] = IfExp(t[3], t[1], t[5])

def p_not_expression(t):
	'expression : NOT expression'
	t[0] = Not(t[2])

def p_and_expression(t):
	'expression : expression AND expression'
	t[0] = And([t[1], t[3]])

def p_or_expression(t):
	'expression : expression OR expression'
	t[0] = Or([t[1], t[3]])

def p_is_expression(t):
	'expression : expression IS expression'
	t[0] = Compare(t[1], [('is', t[3])])
	
#TODO: Fix the conflict with the ASSIGN token
def p_equals_expression(t):
	'expression : expression EQUALS expression'
	t[0] = Compare(t[1], [('==',t[3])])

def p_input_expression(t):
	'expression : INPUT  LEFTPARAN RIGHTPARAN'
	t[0] = CallFunc(Name('input'),[])

#SPECIAL CASIN UP IN THIS HIZZLE	
def p_list_empty(t):
	'expression : LEFTBRACK RIGHTBRACK'
	t[0] = List(())

def p_list(t):
	'expression : LEFTBRACK expr_list RIGHTBRACK'
	if not isinstance(t[2],list):
		t[0] = List([t[2]])
	else:
		t[0] = List(t[2])

def p_term_list(t):
	'expr_list : expression'
	t[0] = t[1]

def p_list_expression(t):
	'expr_list : expr_list COMMA expression'	
	if isinstance(t[1], list):
		t[0] = t[1] + [t[3]]		 
	else: 
		t[0] = [t[1]] + [t[3]]

def p_empty_dict(t):
	'expression : LEFTCURL RIGHTCURL'	
	t[0] = Dict(())
	
def p_dict(t):
	'expression : LEFTCURL pair_list RIGHTCURL'
	if not isinstance(t[2],list):
		t[0] = Dict([t[2]])
	else:
		t[0] = Dict(t[2])

def p_pair_base(t):
	'pair : expression COLON expression'
	t[0] = (t[1],t[3])

def p_term_dict(t):
	'pair_list : pair'
	t[0] = t[1]

def p_dict_expression(t):
	'pair_list : pair_list COMMA pair'
	if isinstance(t[1], list):
		t[0] = t[1] + [t[3]]		 
	else: 
		t[0] = [t[1]] + [t[3]]
	
def p_error(t):
	print "Syntax error at '%s'" % t.value
import ply_3_4.yacc as yacc

def parse(code):
	import ply.lex as lex
	lex.lex()
	import ply.yacc as yacc
	import re
	parser = yacc.yacc()
	statements = []
	statements = parser.parse(code)
	return statements
