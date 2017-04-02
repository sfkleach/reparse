import re
from lexeme import LexemeType
from actions import SetHeader, Seq, Print, Repeat

import dents
import tokenise

class ReparseParser:

	def __init__( self, tokens ):
		self._tokens = dents.Dent( tokens )

	def mustReadToken( self, ttype, tvalue ):
		t = self._tokens.nextOptToken()
		if not t or t.lexemeType() != ttype or t.lexemeValue() != tvalue:
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
					return int( t.lexemeValue() )
				except ValueError:
					return float( t.lexemeValue() )
			else:
				raise Exception( 'Number needed: {}'.format( t.lexemeValue() ) )
		else:
			raise Exception( 'Unexpected end of file' )

	def readStringLiteral( self ):
		t = self._tokens.nextOptToken()
		if t:
			if t.isStringLiteral():
				return t.lexemeValue()
			else:
				raise Exception( 'String needed: {}'.format( t.lexemeValue() ) )
		else:
			raise Exception( 'Unexpected end of file' )

	def readRegexLiteral( self, with_newline=True ):
		t = self._tokens.nextOptToken()
		if t:
			if t.isRegexLiteral():
				return re.compile( t.lexemeValue() + ( '\\n' if with_newline else '' ) )
			else:
				raise Exception( 'String needed: {}'.format( t.lexemeValue() ) )
		else:
			raise Exception( 'Unexpected end of file' )

	def readCommand( self ):
		t = self._tokens.nextOptToken()
		if t:
			if t.isSymbol():
				v = t.lexemeValue()
				if v in PREFIX_TABLE:
					return PREFIX_TABLE[ v ]( self )
				else:
					raise Exception( 'Not implemented yet: {}'.format( v ) )
			else:
				raise Exception( 'Not implemented yet: {}'.format( t.LexemeType() ) )
		else:
			return None

	def readHeader( self ):
		self.mustReadToken( LexemeType.Keyword, '[' )
		num = self.readNumLiteral()
		self.mustReadToken( LexemeType.Keyword, ']' )
		self.mustReadToken( LexemeType.Keyword, ':' )
		title = self.readStringLiteral()
		return SetHeader( title, num )

	def readPrintRepeat( self ):
		# self.mustReadToken( LexemeType.Keyword, ':' )		
		regex = self.readRegexLiteral()
		return Repeat( regex, Print() )

	def readPass( self ):
		return Seq()

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
	'Pass': ReparseParser.readPass,
	'Print-Repeat': ReparseParser.readPrintRepeat
}

def scriptParser( src ):
	return ReparseParser( tokenise.ReparseLexerFactory( src ) )
