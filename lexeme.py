import enum
import sys

# TODO remove the conditional when 3.6+ becomes the default.
class LexemeType( enum.Enum ):
	Symbol = enum.auto() if sys.hexversion >= 0x30600f0 else 0
	StringLiteral = enum.auto() if sys.hexversion >= 0x30600f0 else 1
	RegexLiteral = enum.auto() if sys.hexversion >= 0x30600f0 else 2
	NumLiteral = enum.auto() if sys.hexversion >= 0x30600f0 else 3
	Indentation = enum.auto() if sys.hexversion >= 0x30600f0 else 4
	Keyword = enum.auto() if sys.hexversion >= 0x30600f0 else 5

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

	def isSymbol( self, value = None ):
		if value != None and value != self._text:
			return False
		return self._lexeme_type is LexemeType.Symbol

	def isKeyword( self, value = None ):
		if value != None and value != self._text:
			return False
		return self._lexeme_type is LexemeType.Keyword

	def isStringLiteral( self, value = None ):
		if value != None and value != self._text:
			return False
		return self._lexeme_type is LexemeType.StringLiteral

	def isRegexLiteral( self ):
		return self._lexeme_type is LexemeType.RegexLiteral

	def isNumLiteral( self, value = None ):
		if value != None and value != self._text:
			return False		
		return self._lexeme_type is LexemeType.NumLiteral

	def numValue( self ):
		return int( self._text )

	def toInt( self ):
		return int( self._text )

	def isIndentation( self ):
		return self._lexeme_type is LexemeType.Indentation
