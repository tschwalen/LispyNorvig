Symbol = str
Number = (int, float)
Atom   = (Symbol, Number)
List   = list
Exp    = (Atom, List)
Env    = dict



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


program = "(begin (define r 10) (* pi (* r r)))"

print(parse(program))
			