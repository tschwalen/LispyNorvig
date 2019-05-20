import math
import operator as op

# type declarations
Symbol = str
Number = (int, float)
Atom   = (Symbol, Number)
List   = list
Exp    = (Atom, List)
Env    = dict


##### Parser code (Should probably be separated out) #####

def tokenize(chars: str) -> list:
	"""Convert a string of characters into a list of tokens."""
	return chars.replace('(', ' ( ').replace(')', ' ) ').split()

def parse(program: str) -> Exp:
	""" Read a scheme expression from a string. """
	return read_from_tokens(tokenize(program))


def read_from_tokens(tokens: list) -> Exp:
	""" Read an expression from a sequence of tokens.

		Note:
		This is actually a recursive-descent parser, 
		but lisp only has expressions and atoms, so it
		doesn't really look like one. """


	# unterminated s-exps are a problem
	if len(tokens) == 0:
		raise SyntaxError("Unexpected EOF")

	# get the next token
	token = tokens.pop(0)


	if token == "(":
		""" Open parens means a new S-exp  """
		L = []

		while tokens[0] != ")":
			""" Very clever way by Mr. Norvig to recursively parse s-exps"""
			L.append(read_from_tokens(tokens))
		tokens.pop(0)
		return L
	elif token == ")":
		""" We shouldn't encounter a closing paren here """
		raise SyntaxError("Unexpected \')\'")
	else:
		""" if we're not reading another s-exp, then it must be an atom """
		return atom(token)

def atom(token: str) -> Atom:
	""" Numbers and symbols are the atoms of lisp """

	""" Mr. Norvig uses try-catches and python's type exceptions to
		process atoms in the language. Odd. """
	try:
		return int(token)
	except ValueError:
		try: 
			return float(token)
		except ValueError:
			return Symbol(token)


#########################################################################


# program = "(begin (define r 10) (* pi (* r r)))"

# print(parse(program))
			

def standard_env() -> Env:
	""" Standard lisp/scheme environment """

	env = Env()

	# pretty clever hack from Mr. Norvig that gets you sin, cos, sqrt, and a bunch of stuff you don't need
	env.update(vars(math))	

	# table of basic lisp functions and their corrosponding python functions
	env.update({
		'+':op.add, '-':op.sub, '*':op.mul, '/':op.truediv, 
        '>':op.gt, '<':op.lt, '>=':op.ge, '<=':op.le, '=':op.eq, 
        'abs':     abs,
        'append':  op.add,
        'apply':   lambda proc, args: proc(*args),
        'begin':   lambda *x: x[-1],
        'car':     lambda x: x[0],
        'cdr':     lambda x: x[1:],
        'cons':    lambda x,y: [x] + y,
        'eq?':     op.is_, 
        'expt':    pow,
        'equal?':  op.eq, 
        'length':  len,
        'list':    lambda *x: List(x), 
        'list?':   lambda x: isinstance(x, List),
        'map':     map,
        'max':     max,
        'min':     min,
        'not':     op.not_,
        'null?':   lambda x: x == [],
        'number?': lambda x: isinstance(x, Number),  
		'print':   print,
        'procedure?': callable,
        'round':   round,
        'symbol?': lambda x: isinstance(x, Symbol) 
	})
	return env
	
global_env = standard_env()


#eval: the heart of any lisp
def eval(x: Exp, env=global_env) -> Exp:
	""" Evaluate an expression in an environment."""

	if isinstance(x, Symbol): # reference variable
		return env[x]
	elif isinstance(x, Number): # constant number
		return x
	elif x[0] == "if": 	#conditionals
		(_, test, conseq, alt) = x  # using tuple unpacking to get condition, then, else
		exp = (conseq if eval(test, env) else alt)
		return eval(exp, env)
	elif x[0] == "define":
		(_, symbol, exp) = x
		env[symbol] = eval(exp, env)
	else:
		""" otherwise, evaluate the function on its arguments """
		proc = eval(x[0], env)
		args = [eval(arg, env) for arg in x[1:]]
		return proc(*args)


#print(eval(parse("(begin (define r 10) (* pi (* r r)))")))

def repl(prompt="lis.py>"):

	while True:
		val = eval(parse(input(prompt)))
		if val is not None:
			print(schemestr(val))

def schemestr(exp):
	""" Convert a Python object into a Scheme-readable string. """
	if isinstance(exp, List):
		return "(" + " ".join(map(schemestr, exp)) + ")"
	else:
		return str(exp)

repl()