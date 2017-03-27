import enum
from tokeniserfactory import TokeniserFactory, MoveSet, Accept, Pushback, Erase

class TokenType( enum.Enum ):
	Symbol = enum.auto()
	StringLiteral = enum.auto()
	RegexLiteral = enum.auto()
	NumLiteral = enum.auto()
	Indent = enum.auto()
	Keyword = enum.auto()

class Token:

	def __init__( self, token_type, text ):
		self._token_type = token_type
		self._text = text

	def isSymbol( self ):
		return self._token_type is Symbol

	def isStringLiteral( self ):
		return self._token_type is StringLiteral

	def isRegexLiteral( self ):
		return self._token_type is RegexLiteral

	def isNumLiteral( self ):
		return self._token_type is NumLiteral

ReparseTokeniserFactory = (
	TokeniserFactory(
	    { 
		    "StartLine": 
		    	MoveSet(
		            Accept( ' \t', "Indentation" ),
		            Pushback( True, "StartToken"  ),
		            Erase( None, lambda t: None )
		        ),
		    "Indentation":
		    	MoveSet(
		    		Accept( ' \t', "Indentation" ),
		    		Pushback( True, lambda t: ( TokenType.Indent, t.collected() ) ),
		    		Erase( None, lambda t: None )
		    	),
		    "StartToken": 
			    MoveSet(
			        Erase( '\n', "StartLine" ),
			        Erase( ' \t', "StartToken" ),
			        Accept( '[]:', lambda t: ( TokenType.Keyword, t.collected() ) ),
			        Accept( lambda x: x.isalpha(), "Symbol" ),
			        Accept( lambda x: x.isnumeric(), "Num" ),
			        Erase( '"', "String" ),
			        Accept( '/', "Slash" ),
			        Pushback( None, lambda t: None )
			    ),
			"Slash":
				MoveSet(
					Accept( '/', "Regex" ),
					Pushback( True, lambda t: ( TokenType.Symbol, t.collected() ) ),
					Pushback( None, lambda t: ( TokenType.Symbol, t.collected() ) )
				),
			"Regex":
				TO BE DONE
			"Symbol":
				MoveSet(
			        Pushback( ' \t\n', lambda t: ( TokenType.Symbol, t.collected() ) ),
			        Accept( lambda x: x.isalnum() or x == '_', "Symbol" ),
			        Pushback( True, lambda t: ( TokenType.Symbol, t.collected() ) ),
			        Pushback( None, lambda t: ( TokenType.Symbol, t.collected() ) )
				),
			"Num":
				MoveSet(
					Accept( lambda x: x.isnumeric(), "Num" ),
			        Pushback( True, lambda t: ( TokenType.NumLiteral, t.collected() ) ),
			        Pushback( None, lambda t: ( TokenType.NumLiteral, t.collected() ) )
				),
			"String":
				MoveSet(
					Erase( '"', lambda t: ( TokenType.StringLiteral, t.collected() ) ),
					Accept( True, "String" )
				)
	    },
	    start="StartLine",
	    reset="StartToken"
	)
)

import io
def test_input( text ):
	for t in ReparseTokeniserFactory( io.StringIO( text ) ):
		print( t )

