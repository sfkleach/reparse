import enum

class LexemeType( enum.Enum ):
	Symbol = enum.auto()
	StringLiteral = enum.auto()
	RegexLiteral = enum.auto()
	NumLiteral = enum.auto()
	Indentation = enum.auto()
	Keyword = enum.auto()

class Lexeme:

	def __init__( self, lexeme_type, text ):
		self._lexeme_type = lexeme_type
		self._text = text

	def __str__( self ):
		return '<lexeme {}:{}>'.format( self._lexeme_type, self._text )

	def __getitem__( self, n ):
		if n == 0:
			return self._lexeme_type
		elif n == 1:
			return self._text
		else:
			raise Exception( 'Unexpected index' )

	def lexemeType( self ):
		return self._lexeme_type

	def lexemeValue( self ):
		return self._text

	def isSymbol( self ):
		return self._lexeme_type is LexemeType.Symbol

	def isStringLiteral( self ):
		return self._lexeme_type is LexemeType.StringLiteral

	def isRegexLiteral( self ):
		return self._lexeme_type is LexemeType.RegexLiteral

	def isNumLiteral( self ):
		return self._lexeme_type is LexemeType.NumLiteral

	def isIndentation( self ):
		return self._lexeme_type is LexemeType.Indentation
