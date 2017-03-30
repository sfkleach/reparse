import enum
from tokeniserfactory import TokeniserFactory, MoveSet, Accept, Pushback, Erase

class TokenType( enum.Enum ):
	Symbol = enum.auto()
	StringLiteral = enum.auto()
	RegexLiteral = enum.auto()
	NumLiteral = enum.auto()
	Indentation = enum.auto()
	Keyword = enum.auto()

class Token:

	def __init__( self, token_type, text ):
		self._token_type = token_type
		self._text = text

	def __str__( self ):
		return '<token {}:{}>'.format( self._token_type, self._text )

	def __getitem__( self, n ):
		if n == 0:
			return self._token_type
		elif n == 1:
			return self._text
		else:
			raise Exception( 'Unexpected index' )

	def tokenType( self ):
		return self._token_type

	def tokenValue( self ):
		return self._text

	def isSymbol( self ):
		return self._token_type is TokenType.Symbol

	def isStringLiteral( self ):
		return self._token_type is TokenType.StringLiteral

	def isRegexLiteral( self ):
		return self._token_type is TokenType.RegexLiteral

	def isNumLiteral( self ):
		return self._token_type is TokenType.NumLiteral

	def isIndentation( self ):
		return self._token_type is TokenType.Indentation

ReparseTokeniserFactory = (
	TokeniserFactory(
	    { 
		    "StartLine": 
		    	MoveSet(
		            Accept( ' \t', "Indentation" ),
		            Pushback( True, lambda t: Token( TokenType.Indentation, t.collected() )  ),
		            Erase( None, lambda t: None )
		        ),
		    "Indentation":
		    	MoveSet(
		    		Accept( ' \t', "Indentation" ),
		    		Pushback( True, lambda t: Token( TokenType.Indentation, t.collected() ) ),
		    		Erase( None, lambda t: None )
		    	),
		    "StartToken": 
			    MoveSet(
			        Erase( '\n', "StartLine" ),
			        Erase( ' \t', "StartToken" ),
			        Accept( '[]:', lambda t: Token( TokenType.Keyword, t.collected() ) ),
			        Accept( lambda x: x.isalpha(), "Symbol" ),
			        Accept( lambda x: x.isnumeric() or x in '+-', "Num" ),
			        Erase( '"', "String" ),
			        Accept( '/', "Slash" ),
			        Erase( None, lambda t: None )
			    ),
			"Slash":
				MoveSet(
					Erase( '/', "Regex0", lambda t: t.clearAccepted() ),
					Pushback( True, lambda t: Token( TokenType.Symbol, t.collected() ) ),
					Erase( None, lambda t: Token( TokenType.Symbol, t.collected() ) )
				),
			"Regex0":
				MoveSet(
					Erase( '/', "Regex1" ),
					# Erase( '/', lambda t: Token( TokenType.RegexLiteral, t.collected() ) ),
					Accept( True, "Regex0" )
				),
			"Regex1":
				MoveSet(
					Erase( '/', lambda t: Token( TokenType.RegexLiteral, t.collected() ) ),
					Accept( True, "Regex0", lambda t: t.acceptOptChar( '/' ) )
				),			
			"Symbol":
				MoveSet(
			        Pushback( ' \t\n', lambda t: Token( TokenType.Symbol, t.collected() ) ),
			        Accept( lambda x: x.isalnum() or x in '_-', "Symbol" ),
			        Pushback( True, lambda t: Token( TokenType.Symbol, t.collected() ) ),
			        Erase( None, lambda t: Token( TokenType.Symbol, t.collected() ) )
				),
			"Num":
				MoveSet(
					Accept( lambda x: x.isnumeric(), "Num" ),
			        Pushback( True, lambda t: Token( TokenType.NumLiteral, t.collected() ) ),
			        Erase( None, lambda t: Token( TokenType.NumLiteral, t.collected() ) )
				),
			"String":
				MoveSet(
					Erase( '"', lambda t: Token( TokenType.StringLiteral, t.collected() ) ),
					Accept( True, "String" )
				)
	    },
	    start="StartLine",
	    reset="StartToken"
	)
)


