import re
from tokenise import TokenType
from actions import SetHeader, Seq, Print, Repeat
import dents

class ReparseParser:

	def __init__( self, tokens ):
		self._tokens = dents.Dent( tokens )

	def mustReadToken( self, ttype, tvalue ):
		t = self._tokens.nextOptToken()
		if not t or t[0] != ttype or t[1] != tvalue:
			raise Exception( 'Expected token "{}" but got "{}"'.format( tvalue, t[1] ) )
 
	def readToken( self ):
		t = self._tokens.nextOptToken()
		if t:
			return t
		else:
			raise Exception( 'Unexpected end of file' )

	def readNumLiteral( self ):
		t = self._tokens.nextOptToken()
		if t:
			if t.isNumLiteral():
				try:
					return int( t.tokenValue() )
				except ValueError:
					return float( t.tokenValue() )
			else:
				raise Exception( 'Number needed: {}'.format( t.tokenValue() ) )
		else:
			raise Exception( 'Unexpected end of file' )

	def readStringLiteral( self ):
		t = self._tokens.nextOptToken()
		if t:
			if t.isStringLiteral():
				return t.tokenValue()
			else:
				raise Exception( 'String needed: {}'.format( t.tokenValue() ) )
		else:
			raise Exception( 'Unexpected end of file' )

	def readRegexLiteral( self, with_newline=True ):
		t = self._tokens.nextOptToken()
		if t:
			if t.isRegexLiteral():
				return re.compile( t.tokenValue() + ( '\\n' if with_newline else '' ) )
			else:
				raise Exception( 'String needed: {}'.format( t.tokenValue() ) )
		else:
			raise Exception( 'Unexpected end of file' )

	def readCommand( self ):
		t = self._tokens.nextOptToken()
		if t:
			if t.isSymbol():
				v = t.tokenValue()
				if v in PREFIX_TABLE:
					return PREFIX_TABLE[ v ]( self )
				else:
					raise Exception( 'Not implemented yet: {}'.format( v ) )
			else:
				raise Exception( 'Not implemented yet' )
		else:
			return None

	def readHeader( self ):
		self.mustReadToken( TokenType.Keyword, '[' )
		num = self.readNumLiteral()
		self.mustReadToken( TokenType.Keyword, ']' )
		self.mustReadToken( TokenType.Keyword, ':' )
		title = self.readStringLiteral()
		return SetHeader( title, num )

	def readPrintRepeat( self ):
		self.mustReadToken( TokenType.Keyword, ':' )		
		regex = self.readRegexLiteral()
		return Repeat( regex, Print() )

	def readStatements( self ):
		sofar = []
		while True:
			e = self.readCommand()
			# print( 'Command', e )
			if not e:
				break
			sofar.append( e )
		return Seq( *sofar )

PREFIX_TABLE = {
	'Header': ReparseParser.readHeader,
	'Print-Repeat': ReparseParser.readPrintRepeat,
}